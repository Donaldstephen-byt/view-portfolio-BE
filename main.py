# # from fastapi import FastAPI

# # app = FastAPI()

# # @app.get("/")
# # def read_root():
# #     return {"message": "Hello Donald, your backend is live!"}

# # from turtle import *
# # from colorsys import *
# # setpos(40, 50)
# # tracer(30)
# # bgcolor('black')
# # h = 0
# # for i in range(225):
# #     color(hsv_to_rgb(h, 1, 1))
# #     h+=0.01
# #     for j in range(4):
# #         circle(30+j+4, -90)
# #         fd(300)
# #         rt(90)
# #         circle(10)
# #     rt(10)
# # done()
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI
# from fastapi.responses import FileResponse
# from turtle import Screen, circle, fd, rt, color, tracer
# from colorsys import hsv_to_rgb
# from PIL import Image

# def generate_turtle_image():
#     screen = Screen()
#     screen.setup(width=800, height=600)
#     screen.bgcolor("black")
#     tracer(30)
#     h = 0
#     for i in range(225):
#         color(hsv_to_rgb(h, 1, 1))
#         h += 0.01
#         for j in range(4):
#             circle(30 + j + 4, -90)
#             fd(300)
#             rt(90)
#             circle(10)
#             rt(10)
#     screen.update()
#     canvas = screen.getcanvas()
#     canvas.postscript(file="output.ps", colormode="color")
#     img = Image.open("output.ps")
#     img.save("output.png")

# # Generate image before starting FastAPI
# generate_turtle_image()

# app = FastAPI()

# # Allow requests from your frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Or specify your frontend URL like ["http://localhost:8080"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def read_root():
#     return {"message": "Hello, your FastAPI backend is live!"}

# @app.get("/background")
# def get_background_image():
#     return FileResponse("output.png")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++
# _________________________________________________________________


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        # Personal Introduction
        "content": (
            "Hi, I’m Donald Stephen, a university student in Information Systems and Technology and a passionate software engineer. I enjoy building efficient, scalable digital solutions and exploring modern technologies that solve real-world problems."
        ),
        # Approach / Philosophy Section
        "manner": "My Approach",
        "core_principles": {
            "manner_1": "Clean, readable, and maintainable code.",
            "manner_2": "Scalable architecture with thoughtful system design.",
            "manner_3": "Modern, innovative problem–solving with precision.",
            "manner_4": "Detail-oriented and structured engineering mindset."
        },
    }

    
    return JSONResponse(content=about_me_data)

@app.get("/focus")
def get_focus():
    focus_data = {
        "title": "Philosophy & Focus",
        "text": "I am committed to creating software that is efficient, maintainable, and adaptable. I prioritize learning and applying best practices, exploring modern technologies, and ensuring every solution is thoughtfully designed for both users and developers. My focus is on continuous improvement, technical literacy, and problem-solving with clarity and precision.",
    }
    return JSONResponse(content=focus_data)
