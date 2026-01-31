
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
from urllib.parse import quote
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, HTTPException
import logging
import httpx
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize database on startup
def init_database():
    """Initialize the analytics database if it doesn't exist"""
    try:
        conn = sqlite3.connect("analytics.db")
        cursor = conn.cursor()
        
        # Create visits table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          page TEXT,
          referrer TEXT,
          device TEXT,
          duration INTEGER,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create contacts table for storing messages
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL,
          message TEXT NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

# Initialize database when app starts
@app.on_event("startup")
async def startup_event():
    init_database()
# Enable CORS..
# CORS: allow frontend from localhost and from Render env (e.g. your Vercel/Netlify URL)
_cors_origins_env = os.getenv("CORS_ORIGINS", "").strip()
_default_origins = ["http://localhost:5173", "http://localhost:3000"]
if _cors_origins_env == "*":
    allow_origins = ["*"]
elif _cors_origins_env:
    allow_origins = [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
    allow_origins = list(dict.fromkeys(allow_origins + _default_origins))
else:
    allow_origins = _default_origins
logger.info(f"CORS allowed origins: {allow_origins}")


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173", "http://localhost:3000"],  # {{Or ["*"] for testing}}
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to check Do Not Track header..
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
    """Save visit to database with error handling"""
    try:
        device = get_device(user_agent)
        
        # Ensure database is initialized
        conn = sqlite3.connect("analytics.db")
        cursor = conn.cursor()
        
        # Create table if it doesn't exist (safety check)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          page TEXT,
          referrer TEXT,
          device TEXT,
          duration INTEGER,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute(
            """
            INSERT INTO visits (page, referrer, device, duration)
            VALUES (?, ?, ?, ?)
            """,
            (page, referrer, device, duration)
        )

        conn.commit()
        conn.close()
        logger.info(f"Visit saved: page={page}, device={device}, duration={duration}")
    except Exception as e:
        logger.error(f"Failed to save visit: {e}", exc_info=True)

@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI backend!"}

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


# Email configuration
EMAIL_FROM = os.getenv("EMAIL_FROM", "donalduko69@gmail.com")
EMAIL_TO = os.getenv("EMAIL_TO", "donaldstephenuko@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "Drealstar@205")  # Use environment variable in production

# WhatsApp configuration (using CallMeBot API - free alternative)
# Get your API key from: https://www.callmebot.com/blog/free-api-whatsapp-messages/
# Or use Twilio for more reliable service
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")  # Set this in environment variables
WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "+2348143405610")  # Your WhatsApp number with country code

class Contact(BaseModel):
    name: str
    email: str
    message: str

def save_contact_message(name: str, email: str, message: str):
    """Save contact message to database"""
    try:
        conn = sqlite3.connect("analytics.db")
        cursor = conn.cursor()
        
        # Ensure table exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL,
          message TEXT NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute(
            """
            INSERT INTO contacts (name, email, message)
            VALUES (?, ?, ?)
            """,
            (name, email, message)
        )
        
        conn.commit()
        conn.close()
        logger.info(f"Contact message saved: {name} ({email})")
    except Exception as e:
        logger.error(f"Failed to save contact message: {e}", exc_info=True)

def send_email_notification(name: str, email: str, message: str):
    """Send email notification about new contact message"""
    try:
        msg = EmailMessage()
        msg["Subject"] = "📩 New Portfolio Contact"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        msg.set_content(f"""
New message from your portfolio:

Name: {name}
Email: {email}

Message:
{message}
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        logger.info(f"Email notification sent for contact from {name}")
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}", exc_info=True)

def send_whatsapp_notification(name: str, email: str, message: str):
    """Send WhatsApp notification using CallMeBot API"""
    if not WHATSAPP_API_KEY:
        logger.warning("WhatsApp API key not configured, skipping WhatsApp notification")
        return
    
    try:
        # Format message for WhatsApp
        whatsapp_message = f"📩 New Portfolio Contact\n\nName: {name}\nEmail: {email}\n\nMessage: {message[:200]}..."  # Limit message length
        
        # CallMeBot API endpoint
        url = f"https://api.callmebot.com/whatsapp.php?phone={WHATSAPP_PHONE}&text={quote(whatsapp_message)}&apikey={WHATSAPP_API_KEY}"
        
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
        
        if response.status_code == 200:
            logger.info(f"WhatsApp notification sent for contact from {name}")
        else:
            logger.warning(f"WhatsApp notification failed with status {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to send WhatsApp notification: {e}", exc_info=True)

@app.post("/api/contact")
async def contact(data: Contact, background_tasks: BackgroundTasks):
    """Handle contact form submission"""
    try:
        # Save to database
        background_tasks.add_task(
            save_contact_message,
            name=data.name,
            email=data.email,
            message=data.message
        )
        
        # Send email notification
        background_tasks.add_task(
            send_email_notification,
            name=data.name,
            email=data.email,
            message=data.message
        )
        
        # Send WhatsApp notification
        background_tasks.add_task(
            send_whatsapp_notification,
            name=data.name,
            email=data.email,
            message=data.message
        )
        
        return {"success": True, "message": "Your message has been sent successfully!"}

    except Exception as e:
        logger.error(f"Contact form error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process contact form. Please try again later."
        )

@app.get("/api/contacts")
def get_contacts():
    """Get all saved contact messages"""
    try:
        conn = sqlite3.connect("analytics.db")
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, name, email, message, created_at
        FROM contacts
        ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        contacts = []
        for row in rows:
            contacts.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "message": row[3],
                "created_at": row[4]
            })
        
        return {"contacts": contacts, "count": len(contacts)}
    except Exception as e:
        logger.error(f"Failed to fetch contacts: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch contact messages"
        )