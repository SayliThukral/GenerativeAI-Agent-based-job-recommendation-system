import asyncio
import sys
import json
from database import get_db
from test_serper_api import get_youtube_tutorials_for_gaps
from src.services.prompts.summarise_missing_items_prompts import SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_PROMPT

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from src.services.ats_service import ATSservice
from src.services.document_service import DocumentService
from src.services.job_agent_service import get_job_recommendations


# ── Helpers ───────────────────────────────────────────────────────────────────

def safe_list(val):
    """Always return a list — never null / None."""
    if isinstance(val, list):
        return val
    return []


def clean_youtube_titles(recommendations: dict) -> dict:
    """Strip ' - YouTube' suffix that Serper appends to video titles."""
    for category in recommendations.values():
        if isinstance(category, list):
            for video in category:
                if isinstance(video, dict) and "title" in video:
                    video["title"] = video["title"].replace(" - YouTube", "").strip()
    return recommendations


def strip_category_prefixes(items: list) -> list:
    """
    Remove 'Skill: ', 'Experience: ', 'Education: ' prefixes from mismatched_items
    before passing to the gap-analysis prompt.
    Doing this in Python avoids wasting LLM tokens on prefix-stripping instructions.
    """
    prefixes = ("skill:", "experience:", "education:")
    cleaned = []
    for item in items:
        s = item.strip()
        lower = s.lower()
        for prefix in prefixes:
            if lower.startswith(prefix):
                s = s[len(prefix):].strip()
                break
        cleaned.append(s)
    return cleaned


# ── Pipeline ──────────────────────────────────────────────────────────────────

class Pipeline:
    def __init__(self):
        self.document_service = DocumentService()
        self.ats_service = ATSservice()

    
    async def process_resume(self, cv_path: str, jd_path: str, email: str) -> dict:
        try:
            # ── 0. Fetch User Plan from Database ──────────────────────────────
            conn = get_db()
            cursor = conn.cursor()
            user_record = cursor.execute("SELECT user_plan FROM users WHERE email = ?", (email,)).fetchone()
            conn.close()

            # Agar record milta hai toh plan lo, nahi toh default 'basic' rakh lo
            user_plan = user_record["user_plan"].lower() if user_record else "basic"
            print(f"Plan fetched directly from DB in app.py: {user_plan}")


            # ── 1. Extract raw text ───────────────────────────────────────────
            cv_text = self.document_service.extract_text(cv_path)
            if not cv_text:
                return {"error": "No text could be extracted from the resume. Please upload a readable PDF or DOCX."}

            jd_text = self.document_service.extract_text(jd_path)
            if not jd_text:
                return {"error": "No text could be extracted from the job description. Please upload a readable PDF or DOCX."}

            # ── 2. Parse CV + JD into structured data ─────────────────────────
            cv_items = await self.ats_service.extract_cv_items(cv_text)
            jd_items = await self.ats_service.extract_jd_items(jd_text)

            # ── 3. Extract domain ──────────────────────
            domain = "Professional"
            if isinstance(cv_items, dict):
                domain = cv_items.get("Domain") or "Professional"

            # ── 4. Generate ATS score + mismatched_items ──────────────────────
            ats_score = await self.ats_service.generate_ats_score(cv_items, jd_items)
            
            if not isinstance(ats_score, dict):
                return {"error": "ATS scoring failed. Please try again."}

            ats_score.setdefault("ats_score",                  0)
            ats_score.setdefault("skills_match_percentage",    0)
            ats_score.setdefault("experience_match_percentage", 0)
            ats_score.setdefault("education_match_percentage", 0)
            ats_score.setdefault("matched_skills",             [])
            ats_score.setdefault("mismatched_items",           [])
            ats_score.setdefault("analysis", "Analysis unavailable for this submission.")

            ats_score["matched_skills"]   = safe_list(ats_score["matched_skills"])
            ats_score["mismatched_items"] = safe_list(ats_score["mismatched_items"])

            if not ats_score["analysis"] or not str(ats_score["analysis"]).strip():
                ats_score["analysis"] = "Analysis unavailable for this submission."

            # ── 5. Gap analysis ───────────────────────────────────────────────
            raw_missing   = ats_score["mismatched_items"]
            clean_missing = strip_category_prefixes(raw_missing)

            gap_response = await self.ats_service.summarise_missing_items(
                SUMMARY_SYSTEM_PROMPT,
                SUMMARY_USER_PROMPT.format(domain=domain, missing_keywords=clean_missing)
            )

            if isinstance(gap_response, dict):
                gap_data = gap_response
            elif isinstance(gap_response, str):
                try:
                    clean = gap_response.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
                    gap_data = json.loads(clean)
                except json.JSONDecodeError as e:
                    gap_data = {}
            else:
                gap_data = {}

            ats_score["gap_analysis"] = {
                "skills":     safe_list(gap_data.get("skills")),
                "experience": safe_list(gap_data.get("experience")),
                "education":  safe_list(gap_data.get("education")),
            }

            # ── 6. YouTube recommendations (Fixed Indentation) ────────────────
            if user_plan in ["standard", "premium"]:
                raw_youtube = get_youtube_tutorials_for_gaps(domain)
                ats_score["youtube_recommendations"] = clean_youtube_titles(
                    raw_youtube if isinstance(raw_youtube, dict) else {}
                )
            else:
                ats_score["youtube_recommendations"] = {}
            
            # ── 7. Job recommendations ────────────────────────────────────────
            if user_plan == "premium":
                skills = ats_score.get("matched_skills", [])
                experience = ats_score.get("Experience", [])
                job_recommendations = get_job_recommendations(domain, skills, experience)
                ats_score["job_recommendations"] = job_recommendations
            else:
                ats_score["job_recommendations"] = []

            return ats_score

        except Exception as e:
            print(f"Pipeline error: {e}")
            return {"error": f"An unexpected error occurred: {str(e)}"}

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pipeline = Pipeline()

    cv_path = "C:/Users/ishaa/OneDrive/Desktop/ml-prfl/GenerativeAI-Agent-based-job-recommendation-system/temp/karan_resume.pdf"
    jd_path = "C:/Users/ishaa/OneDrive/Desktop/ml-prfl/GenerativeAI-Agent-based-job-recommendation-system/temp/FW-SWE-I-JD-2.pdf"

    result = asyncio.run(pipeline.process_resume(cv_path, jd_path))

    print("\nFINAL ATS RESULT:")
    print(json.dumps(result, indent=2))