import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
POPPLER_PATH = r"C:\Program Files\poppler\poppler-24.02.0\Library\bin"
# POINT TO YOUR TESSERACT EXECUTABLE (Windows specific)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(file_path):
    try:
        text = ""
        
        # Check if the file is a PDF
        if file_path.lower().endswith('.pdf'):
            # Convert PDF to a list of images (one image per page)
            # Note: You might need to specify poppler_path if it's not in your system PATH
            images = convert_from_path(file_path,poppler_path=POPPLER_PATH)
            
            for i, img in enumerate(images):
                print(f"Processing page {i+1}...")
                text += pytesseract.image_to_string(img) + "\n"
                
        # Handle standard image files (JPG, PNG)
        else:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)

        return text

    except Exception as e:
        return f"An error occurred: {e}"

# --- Test It ---
image_file = r'C:\Users\ASUS\OneDrive\Desktop\Sayli_Thukral_resume.pdf' 
result = extract_text(image_file)

print("--- Extracted Text ---")
print(result)