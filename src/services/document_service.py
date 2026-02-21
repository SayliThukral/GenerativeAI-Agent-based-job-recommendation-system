from src.models.cv_models import CVParsedData
from src.utilities.text_extractor import TextExtractor

class DocumentService:
    def __init__(self):
        pass

    def extract_text(self, file_path):
        """Extract text from a document using OCR."""
        try:
            text_extractor = TextExtractor()
            raw_text = text_extractor.extract_text(file_path)
            return raw_text
        except Exception as e:
            print(f"Error in DocumentService: {e}")
            return None
        
    def convert_raw_text_to_structured_data(self, raw_text):
        """Convert raw text to JSON format."""
        raise NotImplementedError
    
        
        
