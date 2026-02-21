from src.services.ats_service import ATSservice
from src.services.document_service import DocumentService

class Pipeline:
    def __init__(self):
        self.document_service = DocumentService()
        self.ats_service = ATSservice()

    def process_resume(self, file_path):
        try:    
            ocr_text = self.document_service.extract_text(file_path)
            if ocr_text:
                subheadings = self.ats_service.extract_subheadings(ocr_text)
                return subheadings
            else:
                return "No text extracted from the resume."
        except Exception as e:
            return f"Error processing resume: {e}"
        
if __name__ == "__main__":
    pipeline = Pipeline()
    result = pipeline.process_resume("C:/Users/Ishaa/Downloads/Ishaan_Ansari_ML_Engineer_2026_V4.pdf") # Update with actual file path
    print(result)