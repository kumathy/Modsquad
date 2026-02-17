import whisper
import logging

logger = logging.getLogger(__name__)

logger.info("Loading Whisper model...")
model = whisper.load_model("base.en")
logger.info("Whisper model loaded successfully")


def transcribe_audio(audio_path: str) -> dict:
    logger.info(f"Transcribing: {audio_path}")

    result = model.transcribe(audio_path)

    logger.info(f"Transcription complete: {len(result.get('segments', []))} segments")
    
    return {
        "text": result["text"],
        "language": result.get("language", "unknown"),
        "segments": result.get("segments", [])
    }