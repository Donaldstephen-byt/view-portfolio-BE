
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os
from starlette.middleware.base import BaseHTTPMiddleware
import sqlite3
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # {{Or ["*"] for testing}}
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to check Do Not Track header
class DNTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.dnt = request.headers.get("DNT") == "1"
        return await call_next(request)

app.add_middleware(DNTMiddleware)

def get_device(user_agent: str):
    if not user_agent:
        return "unknown"
    ua = user_agent.lower()
    if "mobile" in ua:
        return "mobile"
    return "desktop"

def save_visit(page, referrer, duration, user_agent):
    device = get_device(user_agent)

    conn = sqlite3.connect("analytics.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO visits (page, referrer, device, duration)
        VALUES (?, ?, ?, ?)
        """,
        (page, referrer, device, duration)
    )

    conn.commit()
    conn.close()



@app.post("/track")
async def track(request: Request, background_tasks: BackgroundTasks):
    # Respect Do Not Track
    if request.state.dnt:
        return {"tracked": False}

    body = await request.body()
    if not body:
        return {"tracked": False}

    try:
        data = json.loads(body)
    except Exception:
        return {"tracked": False}

    background_tasks.add_task(
        save_visit,
        page=data.get("page"),
        referrer=data.get("referrer"),
        duration=data.get("duration"),
        user_agent=request.headers.get("user-agent")
    )

    return {"tracked": True}

# for profile data (avatar, fullName, role, email, phone, location, social links) for first card (sidebar..)
@app.get("/profile")
def get_profile():
    profile_data = {
        "avatar": "https://i.pravatar.cc/150?img=10",
        "fullName": "Donald Stephen",
        "role": "Frontend Developer",
        "email": "Donalduko69@.com",
        "phone": "+234 814 340 5610 ",
        "location": "lagose, Nigiria",
        "github": "https://github.com/",
        "linkedin": "https://linkedin.com/in/johndoe",
        "twitter": "https://twitter.com/johndoe",
        "instagram": "https://instagram.com/johndoe",
        "facebook": "https://facebook.com/johndoe",
    }
    return JSONResponse(content=profile_data)

@app.get("/skills")
def get_skills():
    skills_data = {
        "title": "My Skills 💻",
        "description": "🟢 Proficient: React, JavaScript (ES6+), Python (FastAPI),\nHTML, CSS, Tailwind\n🔵 Familiar: TypeScript, Redux, Node.js\n🟡 Exploring: Web3, Next.js, GSAP for animations",
        "full_name": "Donald Stephen",
        "role": "Software Engineer",
        "email": "donalduko69@gmail.com",
        "phone": "+234 814 340 5610",
        "location": "Abuja, Nigeria",
        "hobbies": ["Problem Solving", "Football", "UI Design", "Listening to Music"],
        "dislikes": ["Bugs", "Slow Internet", "Bad UI", "Noisy Environment"],
    }
    return JSONResponse(content=skills_data)

@app.get("/about/skills")
def get_aboutSkills():
    aboutSkills_data = {
        "title": "Skills",
        "brief": "Proficient in full-stack web development with strong expertise in JavaScript, React, TypeScript, Python, and FastAPI. Experienced in building REST APIs, integrating frontend and backend systems, and designing efficient database structures. Knowledgeable in scalable architecture, clean code principles, and software engineering best practices.",
        "titleforsubcard_1": "Frontend Development",
        "contenforsubcard_1": "HTML5, CSS3, JavaScript (ES6+), TypeScript, React.js, Tailwind CSS",
        "titleforsubcard_2": "Backend Basics",
        "contenforsubcard_2": "Node.js (Express), REST APIs, JSON, Authentication, MVC basics",
        "titleforsubcard_3": "IT & Networking",
        "contenforsubcard_3": "Computer hardware basics, OS installation, LAN/WAN,",
        "titleforsubcard_4": "Databases",
        "contenforsubcard_4": "MySQL, MongoDB, Database design, CRUD operations",
        "titleforsubcard_5": "Tools & Workflow",
        "contenforsubcard_5": "Git & GitHub, VS Code, Postman, npm, Agile workflow",
        "titleforsubcard_6": "Soft Skills",
        "contenforsubcard_6": "Problem solving, Team collaboration, Communication, Time management",
    }
    return JSONResponse(content=aboutSkills_data)


@app.get("/about/me")
def get_about_me():
    about_me_data = {
        # Section Title
        "title": "About Me",
        "content": "Hi, welcome! I’m Donald Stephen, a university student studying Information Systems and Technology and a software engineer. I am passionate about building efficient, scalable, and maintainable software applications, and I enjoy exploring modern technologies to solve real-world problems.",
        "manner": "My Approach",
        "core_principles": {
            "manner_1": "Clean, readable, and maintainable code.",
            "manner_2": "Scalable architecture with thoughtful system design.",
            "manner_3": "Modern, innovative problem–solving with precision.",
            "manner_4": "Detail-oriented and structured engineering mindset."
        },
    }
    # Return JSON response with structured data
    return JSONResponse(content=about_me_data)

    # focus to be used in focus card
    # and to be worked on later for more details
    # more details to be added later

@app.get("/focus")
def get_focus():
    focus_data = {
        "title": "Philosophy & Focus",
        "text": "I am committed to creating software that is efficient, maintainable, and adaptable. I prioritize learning and applying best practices, exploring modern technologies, and ensuring every solution is thoughtfully designed for both users and developers. My focus is on continuous improvement, technical literacy, and problem-solving with clarity and precision.",
    }
    return JSONResponse(content=focus_data)
