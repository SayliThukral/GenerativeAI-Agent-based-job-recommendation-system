import asyncio
import sys
from test_serper_api import get_youtube_tutorials_for_gaps

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
            #import pdb;pdb.set_trace()
            cv_text = self.document_service.extract_text(cv_path)
            if not cv_text:
                return "No text extracted from resume."

            jd_text = self.document_service.extract_text(jd_path)
            if not jd_text:
                return "No text extracted from job description."
            
            cv_items = await self.ats_service.extract_cv_items(cv_text)
            jd_items = await self.ats_service.extract_jd_items(jd_text)

            ats_score = await self.ats_service.generate_ats_score(cv_items, jd_items)
            
            # 1. Safely extract the domain and mismatched items from your existing variables
            domain = cv_items.get("Domain", "Professional") if isinstance(cv_items, dict) else "Professional"
            print (domain)
            # FIXED: Changed 'ats_score_result' to 'ats_score' to match your variable from line 4
            mismatched_items = ats_score.get("mismatched_items", []) if isinstance(ats_score, dict) else []

            # 2. Call the search function
            youtube_recommendations = get_youtube_tutorials_for_gaps(domain)

            # 3. Add the YouTube links to your final ATS result so the frontend can see them
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