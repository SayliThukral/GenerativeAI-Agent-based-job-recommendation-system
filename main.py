import fastapi
from fastapi import FastAPI, File, UploadFile
from src.app import Pipeline

app = FastAPI()

@app.get("/")
def read_main():
    return {"message": "Welcome to the Job recommendation system!"}



@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    try:
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        
        pipeline = Pipeline()
        result = pipeline.process_resume(file_location)
        return {"subheadings": result}
    except Exception as e:
        return {"error": str(e)}