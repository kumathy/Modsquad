from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import logging

from utils.transcribe import transcribe_audio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ModSquad API", version="1.0.0")

origins = [
    "http://localhost:5173",
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

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mp3", ".wav", ".m4a"}

@app.get("/")
async def root():
    return {"message": "Modsquad backend is running"}


@app.post("/process-video")
async def process_video(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException (
            status_code=400,
            detail=f"File type {file_extension} not allowed. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    file_path = UPLOAD_DIR / file.filename

    try:
        # Save uploaded file
        logger.info(f"Processing video: {file.filename}")
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size_mb = round(file_path.stat().st_size / (1024 * 1024), 2)
        logger.info(f"File size: {file_size_mb} MB")
        
        # Transcribe
        logger.info("Transcribing audio...")
        transcript_result = transcribe_audio(str(file_path))
        logger.info(f"Transcription complete: {len(transcript_result["segments"])} segments")

        # Log full transcript (for demo purposes, will remove later)
        logger.info("=" * 80)
        logger.info("FULL TRANSCRIPT:")
        logger.info("=" * 80)
        logger.info(transcript_result["text"])
        logger.info("=" * 80)

        # Return results
        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "file_size_mb": file_size_mb,
            "transcript": {
                "text": transcript_result["text"],
                "language": transcript_result["language"],
                "segment_count": len(transcript_result["segments"])
            },
        })
    
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    
    finally:
        file.file.close()
