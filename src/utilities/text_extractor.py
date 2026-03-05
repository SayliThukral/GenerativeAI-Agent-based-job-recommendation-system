import pytesseract
from PIL import Image

class TextExtractor:
    def __init__(self):
        pass

    def extract_text(self, file_path):
        if file_path.lower().endswith('.pdf'):
            return self.extract_text_from_image_pdf(file_path)
        else:
            return self.extract_text_from_image(file_path)

    def extract_text_from_image(image_path):
        try:
            # Open the image file
            image = Image.open(image_path)
            # Use pytesseract to do OCR on the image
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    def extract_text_from_image_pdf(self, pdf_path):
        try: 
            # Convert PDF to images
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)
            text = ""
            for page in range(num_pages):
                page_obj = reader.pages[page]
                text += page_obj.extract_text()
            return text
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return None
        
        
if __name__ == "__main__":
    text_extractor = TextExtractor()
    text = text_extractor.extract_text('C:/Users/ASUS/Downloads/Mt.pdf')
    print(text)