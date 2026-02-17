from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path

app = FastAPI()

origins = [
    "https://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Modsquad backend is running"}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    allowed_extensions = {".mp4", ".mov", ".avi"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException (
            status_code=400,
            detail=f"File type {file_extension} not allowed. Allowed: {allowed_extensions}"
        )
    
    # Save uploaded video
    file_path = UPLOAD_DIR / file.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse({
            "message": "File uploaded successfully",
            "filename": file.filename,
            "path": str(file_path),
            "size_mb": round(file_path.stat().st_size / (1024 * 1024), 2)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Upload failed: {str(e)}")
    
    finally:
        file.file.close()