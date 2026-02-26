from src.models.cv_models import CVParsedData
from src.utilities.text_extractor import TextExtractor
from src.utilities.skills_prompt import build_skills_prompt
from src.services.skills_extraction import extract_skills
import re

class DocumentService:
    def __init__(self):
        pass

    def extract_text(self, file_path):
        """Extract text from a document using OCR."""
        try:
            text_extractor = TextExtractor()
            raw_text = text_extractor.extract_text(file_path)
            #jd_text=text_extractor.extract_text(jd_path)
            return raw_text
            
        except Exception as e:
            print(f"Error in DocumentService: {e}")
            return None
        
    

    def convert_raw_text_to_structured_data(self, raw_text):
        """Convert raw text to structured CV data."""
        try:
            # Extract email
            #import pdb; pdb.set_trace()
            email_match = re.search(r'\S+@\S+', raw_text)
            email = email_match.group() if email_match else None

            # Extract phone number (basic pattern)
            phone_match = re.search(r'\b\d{10}\b', raw_text)
            phone = phone_match.group() if phone_match else None

            # Extract name (simple assumption: first line is name)
            lines = raw_text.strip().split("\n")
            name = lines[0] if lines else None

            skills = extract_skills(raw_text)
            # Create structured object
         
            arr=[email,phone,name,skills]
            return arr 

        except Exception as e:
            print(f"Error converting raw text: {e}")
            return None
    
if __name__ == "__main__":
    
    service = DocumentService()
    raw_text = service.extract_text("C:/Users/ASUS/OneDrive/Desktop/Sayli_Thukral_resume.pdf")
    structured_data = service.convert_raw_text_to_structured_data(raw_text)
    print(structured_data)
    
        
        
