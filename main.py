"""import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",  # fast & cost-effective
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain FastAPI in simple terms."}
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)
"""
from dotenv import load_dotenv
import json
import re
from src.services.ocr_service import OCRService

load_dotenv()


# -----------------------------
# SECTION SYNONYMS
# -----------------------------
SECTION_SYNONYMS = {
    "education": [
        "education",
        "qualification",
        "academic background",
        "academics",
        "studies",
        "degree"
    ],
    "technical_skills": [
        "technical skills",
        "skills",
        "tech stack",
        "expertise",
        "technologies",
        "programming languages"
    ],
    "work_experience": [
        "work experience",
        "professional experience",
        "employment",
        "career history",
        "experience",
        "currently working",
        "presently working"
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects"
    ]
}


# -----------------------------
# COMMON TECH SKILLS LIST
# -----------------------------
COMMON_SKILLS = [
    "python", "java", "c++", "c", "javascript", "typescript",
    "sql", "mysql", "postgresql",
    "aws", "azure", "gcp",
    "machine learning", "deep learning", "nlp",
    "react", "node", "django", "flask",
    "html", "css",
    "docker", "kubernetes",
    "git", "github"
]


# -----------------------------
# EMAIL + PHONE REGEX
# -----------------------------
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEX = r'\b\d{10}\b'


# -----------------------------
# MAIN VALIDATION FUNCTION
# -----------------------------
def validate_and_extract_keywords(ocr_text: str):

    if not ocr_text or len(ocr_text.strip()) < 50:
        return {
            "is_resume": False,
            "score": 0,
            "detected_sections": {},
            "keywords": [],
            "error": "Text too short or empty"
        }

    text_lower = ocr_text.lower()

    detected_sections = {}
    score = 0

    # -----------------------------
    # Detect sections using synonyms
    # -----------------------------
    for section, keywords in SECTION_SYNONYMS.items():
        found = any(keyword in text_lower for keyword in keywords)
        detected_sections[section] = found
        if found:
            score += 10

    # -----------------------------
    # Detect Email
    # -----------------------------
    email_found = re.search(EMAIL_REGEX, ocr_text) is not None
    detected_sections["email"] = email_found
    if email_found:
        score += 10

    # -----------------------------
    # Detect Phone Number
    # -----------------------------
    phone_found = re.search(PHONE_REGEX, ocr_text) is not None
    detected_sections["phone_number"] = phone_found
    if phone_found:
        score += 10

    # -----------------------------
    # Determine Resume Status
    # -----------------------------
    is_resume = score >= 40

    # -----------------------------
    # Extract Technical Skills
    # -----------------------------
    extracted_skills = []

    if is_resume:
        for skill in COMMON_SKILLS:
            if skill in text_lower:
                extracted_skills.append(skill.title())

    return {
        "is_resume": is_resume,
        "score": score,
        "detected_sections": detected_sections,
        "keywords": extracted_skills
    }


# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":

    ocr_service = OCRService()

    file_path = r"C:\Users\ASUS\Downloads\Mt.pdf"

    print(f"Processing: {file_path}...")
    ocr_result = ocr_service.extract_text(file_path)

    if not ocr_result:
        print("❌ OCR extraction failed.")
    else:
        print("✅ OCR SUCCESS")

        if isinstance(ocr_result, dict):
            ocr_text = ocr_result.get("text", "")
        else:
            ocr_text = str(ocr_result)

        result = validate_and_extract_keywords(ocr_text)

        print("\n--- FINAL RESULT ---\n")
        print(json.dumps(result, indent=4))

    