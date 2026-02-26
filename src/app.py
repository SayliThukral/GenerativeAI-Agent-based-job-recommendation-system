import asyncio
import sys
from src.services.ats_service import ATSservice
from src.services.document_service import DocumentService


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Pipeline:
    def __init__(self):
        self.document_service = DocumentService()
        self.ats_service = ATSservice()

    async def process_resume(self, file_path, jd_path):
        try:
            ocr_text = self.document_service.extract_text(file_path)
            if not ocr_text:
                return "No text extracted from resume."

            jd_text = self.document_service.extract_text(jd_path)
            if not jd_text:
                return "No text extracted from job description."

            cv_items = await self.ats_service.extract_cv_items(ocr_text)
            jd_items = await self.ats_service.extract_jd_items(jd_text)
           
            ats_score = await self.ats_service.generate_ats_score(cv_items, jd_items)

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