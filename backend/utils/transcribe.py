import whisper
import logging

logger = logging.getLogger(__name__)

logger.info("Loading Whisper model...")
model = whisper.load_model("medium.en")
logger.info("Whisper model loaded successfully")


def transcribe_audio(audio_path: str) -> dict:
    logger.info(f"Transcribing: {audio_path}")

    segments, result = model.transcribe(audio_path, word_timestamps=True)
    for segment in segments:
        for word in segment.words:
            print(f"{word.start:.2f}s → {word.end:.2f}s  {word.word}")

    logger.info(f"Transcription complete: {len(result.get('segments', []))} segments")
    
    return {
        "text": result["text"],
        "language": result.get("language", "unknown"),
        "segments": result.get("segments", [])
    }

def format_time(t):
    hrs, rem = divmod(t, 3600)
    mins, secs = divmod(rem, 60)
    ms = int((t - int(t)) * 1000)
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02},{ms:03}"

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