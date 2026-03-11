from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import shutil
from pathlib import Path
import logging

from utils.transcribe import transcribe_audio
from utils.settings import router as settings_router
from utils.bleep_alg import bleep_video
from utils.find_words import updated_find_word_matches
from utils.store_filter_words import load_words




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

app.include_router(settings_router, prefix="/settings")

@app.post("/process-video")
async def process_vod(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException (
            status_code=400,
            detail=f"File type {file_extension} not allowed. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    file_path = UPLOAD_DIR / file.filename

    try:
        # Save uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_size_mb = round(file_path.stat().st_size / (1024 * 1024), 2)
        logger.info(f"[Upload] {file.filename} ({file_size_mb} MB)")

        # Transcribe
        logger.info("[Transcribe] Starting...")
        result = transcribe_audio(str(file_path))
        logger.info(f"[Transcribe] Done - {len(result['segments'])} segments")

        # Filter words and censor video
        filtered_words = load_words()
        matches, timestamps = updated_find_word_matches(result['timestamp'], filtered_words)
        logger.info(f"[Filter] {len(matches)} words matched from {len(filtered_words)} filter words")

        output_path = file_path.with_suffix(".censored.mp4")
        logger.info("[Censor] Generating censored video...")
        bleep_video(str(file_path), str(output_path), timestamps, use_bleep=True)
        logger.info(f"[Censor] Done - saved to {output_path.name}")

        # Return results
        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "file_size_mb": file_size_mb,
            "transcript": {
                "text": result["text"],
                "language": result["language"],
                "segment_count": len(result["segments"])
            },
            "download_url": f"/download/{output_path.name}",
        })

    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    finally:
        file.file.close()

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=str(file_path), filename=filename, media_type="video/mp4")