import whisper
import logging

logger = logging.getLogger(__name__)

logger.info("Loading Whisper model...")
model = whisper.load_model("medium.en")
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

# For testing purposes
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    result = transcribe_audio(audio_file)
    
    print("\n" + "="*60)
    print("TRANSCRIPTION RESULT")
    print("="*60)
    print(f"Language: {result['language']}")
    print(f"Segments: {len(result['segments'])}")
    print(f"\nTranscript:\n{result['text']}")
    print("="*60)