import asyncio
import sys

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
            cv_text = self.document_service.extract_text(cv_path)
            if not cv_text:
                return "No text extracted from resume."

            jd_text = self.document_service.extract_text(jd_path)
            if not jd_text:
                return "No text extracted from job description."
            
            cv_items = await self.ats_service.extract_cv_items(cv_text)
            jd_items = await self.ats_service.extract_jd_items(jd_text)

            ats_score = await self.ats_service.generate_ats_score(cv_items, jd_items)

            return ats_score

        except Exception as e:
            return f"Error processing resume: {e}"


if __name__ == "__main__":
    pipeline = Pipeline()

    cv_path = "C:/Users/ishaa/Downloads/Ishaan_Ansari_ML_Engineer_2026_V4.pdf"
    jd_path = "C:/Users/ishaa/Downloads/DevOps Requirements.pdf"

    result = asyncio.run(pipeline.process_resume(cv_path, jd_path))

    print("\nFINAL ATS RESULT:")
    print(result)