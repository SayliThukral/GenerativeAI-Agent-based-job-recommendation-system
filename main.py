import os
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.app import Pipeline
from database import create_table, get_db
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key-change-this-later")
create_table()

# Create temp folder
os.makedirs("temp", exist_ok=True)

# Static folder (CSS + JS)
app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")

# Templates folder (HTML)
templates = Jinja2Templates(directory="Frontend/templates")

@app.get("/")
def home():
    return RedirectResponse(url="/about", status_code=303)

@app.get("/about")
def about(request: Request):
    # Check karte hain ki user session mein hai ya nahi
    is_logged_in = "user" in request.session
    
    return templates.TemplateResponse("about.html", {
        "request": request, 
        "is_logged_in": is_logged_in  # Ye flag hum HTML mein use karenge
    })

# Dashboard page
@app.get("/dashboard")
def dashboard(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)
        
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "messages": []
    })

@app.get("/logout")
def logout(request: Request):
    request.session.clear() # This deletes the cookie!
    return RedirectResponse(url="/login", status_code=303)

@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    conn = get_db()
    cursor = conn.cursor()

    user = cursor.execute("""
        SELECT * FROM users WHERE email = ?
    """, (email,)).fetchone()

    if user and user["password"] == password:
        request.session["user"] = user["email"] 
        return RedirectResponse("/dashboard", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "messages": [("error", "Invalid email or password")]
        })

@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "messages": []
    })

@app.post("/signup")
def signup(
    request: Request,
    username: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(None),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "messages": [("error", "Passwords do not match")]
        })

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, name, email, mobile, password)
        VALUES (?, ?, ?, ?, ?)
        """, (username, name, email, mobile, password))

        conn.commit()

        return templates.TemplateResponse("login.html", {
            "request": request,
            "messages": [("success", "Account created! Please login.")]
        })

    except:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "messages": [("error", "Email already exists")]
        })
    
@app.get("/pricing")
def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

@app.get("/forgot-password")
def forgot_password(request: Request):
    messages = []
    return templates.TemplateResponse("forgot_password.html", {"request": request, "messages": messages})

# Upload API
# Add 'request: Request' to the parameters so we can check the session
@app.post("/upload")
async def upload_files(
    request: Request,
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    # 1. Check if user is actually logged in before processing!
    if "user" not in request.session:
        return {"error": "Unauthorized access. Please login first."}

    try:
        # Save Resume
        resume_path = f"temp/{resume.filename}"
        with open(resume_path, "wb") as buffer:
            buffer.write(await resume.read())

        # Save Job Description
        jd_path = f"temp/{jd.filename}"
        with open(jd_path, "wb") as buffer:
            buffer.write(await jd.read())

        # Run Pipeline
        pipeline = Pipeline()
        result = await pipeline.process_resume(resume_path, jd_path)
        
        # Keep the exact return dictionary you had before
        return {
            "message": "Resume uploaded successfully",
            "ats_score": result.get("ats_score"),
            "skills_match_percentage": result.get("skills_match_percentage"),
            "experience_match_percentage": result.get("experience_match_percentage"),
            "education_match_percentage": result.get("education_match_percentage"),
            "matched_skills": result.get("matched_skills"),
            "analysis": result.get("analysis"),
            "gap_analysis": result.get("gap_analysis"),
            "mismatched_items": result.get("mismatched_items"),
            "youtube_recommendations": result.get("youtube_recommendations"),
            "job_recommendations": result.get("job_recommendations")
        }

    except Exception as e:
        return {"error": str(e)}