import asyncio
import sys
import json
from test_serper_api import get_youtube_tutorials_for_gaps
from src.services.prompts.summarise_missing_items_prompts import SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_PROMPT

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
from src.services.ats_service import ATSservice
from src.services.document_service import DocumentService


class Pipeline:
    def __init__(self):
        self.document_service = DocumentService()
        self.ats_service = ATSservice()

    async def process_resume(self, cv_path, jd_path):
        try:
            # 1. Extract text
            cv_text = self.document_service.extract_text(cv_path)
            if not cv_text:
                return "No text extracted from resume."

            jd_text = self.document_service.extract_text(jd_path)
            if not jd_text:
                return "No text extracted from job description."
            
            # 2. Extract structured items
            cv_items = await self.ats_service.extract_cv_items(cv_text)
            jd_items = await self.ats_service.extract_jd_items(jd_text)

            # 3. Extract domain FIRST ✅
            domain = cv_items.get("Domain", "Professional") if isinstance(cv_items, dict) else "Professional"
            print("DOMAIN:", domain)

            # 4. Generate ATS score
            ats_score = await self.ats_service.generate_ats_score(cv_items, jd_items)

            # 5. GAP ANALYSIS CALL 🔥
            gap_response = await self.ats_service.summarise_missing_items(
                SUMMARY_SYSTEM_PROMPT,
                SUMMARY_USER_PROMPT.format(
                    domain=domain,
                    missing_keywords=ats_score.get("mismatched_items", [])
                )
            )

            print("RAW GAP RESPONSE:", gap_response)  # Debug

            # 6. Ensure JSON format ✅
            gap_data = gap_response if isinstance(gap_response, dict) else json.loads(gap_response)

            # 7. Extract structured fields
            skills = gap_data.get("skills", [])
            education = gap_data.get("education", [])
            experience = gap_data.get("experience", [])

            # 8. Add structured gap analysis to result
            if isinstance(ats_score, dict):
                ats_score["gap_analysis"] = {
                    "skills": skills,
                    "education": education,
                    "experience": experience
                }

            # 9. YouTube recommendations
            youtube_recommendations = get_youtube_tutorials_for_gaps(domain)

            if isinstance(ats_score, dict):
                ats_score["youtube_recommendations"] = youtube_recommendations

            return ats_score

        except Exception as e:
            return f"Error processing resume: {e}"


if __name__ == "__main__":
    pipeline = Pipeline()

    cv_path = "C:/Users/ASUS/OneDrive/Desktop/Sayli_Thukral_resume.pdf"
    jd_path = "C:/Users/ASUS/Downloads/Machine_Learning_Engineer_Job_Description.pdf"

    result = asyncio.run(pipeline.process_resume(cv_path, jd_path))

    print("\nFINAL ATS RESULT:")
    print(result)