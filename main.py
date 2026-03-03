import os
from fastapi import FastAPI, File, UploadFile
from src.app import Pipeline

app = FastAPI()

# Create temp folder if not exists
os.makedirs("temp", exist_ok=True)

@app.get("/")
def read_main():
    return {"message": "Welcome to the Job recommendation system!"}


@app.post("/upload-files")
async def upload_files(
    cv: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    try:
        # Save CV file
        cv_location = f"temp/{cv.filename}"
        with open(cv_location, "wb") as buffer:
            buffer.write(await cv.read())

        # Save JD file
        jd_location = f"temp/{jd.filename}"
        with open(jd_location, "wb") as buffer:
            buffer.write(await jd.read())

        # Process both files
        pipeline = Pipeline()
        result = pipeline.process_resume(cv_location, jd_location)

        return {
            "cv_filename": cv.filename,
            "jd_filename": jd.filename,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}
    
#if __name__ == "__main__":

    #uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)