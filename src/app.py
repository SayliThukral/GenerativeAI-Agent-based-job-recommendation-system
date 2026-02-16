from src.services.ats_service import ATSservice
from src.services.ocr_service import OCRService
obj =ATSservice()

obj2=OCRService()
var=obj2.extract_text("C:\Users\ASUS\OneDrive\Desktop\Sayli_Thukral_resume.pdf")
#print(var)
var2=obj.extract_subheadings(var)
print(var2)

