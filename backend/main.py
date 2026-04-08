import multiprocessing
multiprocessing.freeze_support()

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from sse_starlette.sse import EventSourceResponse
import shutil
import subprocess
import json
import uuid
from pathlib import Path
import logging
import os
import sys

# When running as a PyInstaller bundle, add the bundle dir to PATH
# so that bundled ffmpeg and other binaries are found.
if getattr(sys, "frozen", False):
    bundle_dir = Path(sys._MEIPASS)
    os.environ["PATH"] = str(bundle_dir) + os.pathsep + os.environ.get("PATH", "")
    import certifi
    os.environ["SSL_CERT_FILE"] = certifi.where()

from utils.transcribe import transcribe_audio
from utils.settings import router as settings_router
from utils.settings import get_audio_buffer_seconds
from utils.bleep_alg import bleep_video
from utils.find_words import updated_find_word_matches
from utils.store_filter_words import load_words




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ModSquad API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mp3", ".wav", ".m4a"}

@app.get("/")
async def root():
    return {"message": "Modsquad backend is running"}

app.include_router(settings_router, prefix="/settings")

_jobs = {}

@app.post("/process-video")
async def process_vod(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_extension} not allowed. Allowed: {ALLOWED_EXTENSIONS}"
        )

    job_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / file.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_size_mb = round(file_path.stat().st_size / (1024 * 1024), 2)
        logger.info(f"[Upload] {file.filename} ({file_size_mb} MB)")

        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=index", "-of", "csv=p=0", str(file_path)],
            capture_output=True, text=True,
        )
        if not probe.stdout.strip():
            raise HTTPException(status_code=400, detail="This file has no audio track to transcribe.")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        file.file.close()

    _jobs[job_id] = {"filename": file.filename, "file_path": str(file_path), "file_size_mb": file_size_mb}
    return JSONResponse({"job_id": job_id, "filename": file.filename})


@app.get("/process-video/{job_id}/progress")
async def process_progress(job_id: str):
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = _jobs.pop(job_id)
    file_path = Path(job["file_path"])
    filename = job["filename"]
    file_size_mb = job["file_size_mb"]

    async def event_stream():
        try:
            yield {"event": "progress", "data": json.dumps({"stage": "transcribing", "progress": 20})}

            logger.info("[Transcribe] Starting...")
            result = transcribe_audio(str(file_path))
            logger.info(f"[Transcribe] Done - {len(result['segments'])} segments")

            yield {"event": "progress", "data": json.dumps({"stage": "filtering", "progress": 60})}

            filtered_words = load_words()
            matches, timestamps = updated_find_word_matches(result['timestamp'], filtered_words)
            logger.info(f"[Filter] {len(matches)} words matched from {len(filtered_words)} filter words")

            yield {"event": "progress", "data": json.dumps({"stage": "censoring", "progress": 75})}

            output_path = file_path.with_suffix(".censored.mp4")
            buffer_seconds = get_audio_buffer_seconds()
            logger.info("[Censor] Generating censored video...")
            bleep_video(
                str(file_path),
                str(output_path),
                timestamps,
                use_bleep=True,
                buffer=buffer_seconds,
            )
            logger.info(f"[Censor] Done - saved to {output_path.name}")

            yield {"event": "complete", "data": json.dumps({
                "success": True,
                "filename": filename,
                "file_size_mb": file_size_mb,
                "transcript": {
                    "text": result["text"],
                    "language": result["language"],
                    "segment_count": len(result["segments"])
                },
                "profanity": {
                    "total_flagged": len(matches),
                    "words_replaced": len(timestamps),
                    "matched_words": [word for word, start, end in matches],
                },
                "download_url": f"/download/{output_path.name}",
            })}

        except Exception as e:
            logger.error(f"Processing failed: {e}")
            yield {"event": "error", "data": json.dumps({"detail": str(e)})}

    return EventSourceResponse(event_stream())

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=str(file_path), filename=filename, media_type="video/mp4")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("MODSQUAD_PORT", "8000"))
    uvicorn.run(app, host="127.0.0.1", port=port)