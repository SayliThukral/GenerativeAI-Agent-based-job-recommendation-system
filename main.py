import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.app import Pipeline

app = FastAPI()

# Create temp folder
os.makedirs("temp", exist_ok=True)

# Static folder (CSS + JS)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates folder (HTML)
templates = Jinja2Templates(directory="frontend/templates")


# Home route
@app.get("/")
def home():
    return {"message": "Welcome to the Job recommendation system!"}


@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# Dashboard page
@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/login")
def login(request: Request):
    messages = []  
    return templates.TemplateResponse("login.html", {"request": request, "messages": messages})

@app.get("/signup")
def signup(request: Request):
    messages = []
    return templates.TemplateResponse("signup.html", {"request": request, "messages": messages})

@app.get("/forgot-password")
def forgot_password(request: Request):
    messages = []
    return templates.TemplateResponse("forgot_password.html", {"request": request, "messages": messages})



# Upload API
@app.post("/upload")
async def upload_files(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
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
        result["message"] = "Resume uploaded successfully"
        print(result)

        return {
            "message": "Resume uploaded successfully",
            "ats_score": result.get("ats_score"),

            # --- ADD THESE MISSING KEYS ---
            "skills_match_percentage": result.get("skills_match_percentage"),
            "experience_match_percentage": result.get("experience_match_percentage"),
            "education_match_percentage": result.get("education_match_percentage"),
            "matched_skills": result.get("matched_skills"),
            "analysis": result.get("analysis"),
            "gap_analysis": result.get("gap_analysis"),
            
            "mismatched_items": result.get("mismatched_items"),
            "youtube_recommendations": result.get("youtube_recommendations")
        }

    except Exception as e:
        return {"error": str(e)}