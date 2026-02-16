import pytesseract
from PIL import Image

class OCRService:
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
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return None
        
        
if __name__ == "__main__":
    ocr_service = OCRService()
    text = ocr_service.extract_text('C:/Users/ASUS/Downloads/Mt.pdf')
    print(text)