import whisper
import logging

logger = logging.getLogger(__name__)

logger.info("Loading Whisper model...")
model = whisper.load_model("medium.en")
logger.info("Whisper model loaded successfully")
model = whisper.load_model("medium.en")  # This is the standard static file input
result = model.transcribe("Beautiful_Now(256k).mp3") # This is the transcribed output
keywords = ["moment"]
for word in keywords:
    if word in result["text"].lower():
        print ("Bad words detected")

def transcribe_audio(audio_path: str) -> dict:
    logger.info(f"Transcribing: {audio_path}")

    segments, result = model.transcribe(audio_path, word_timestamps=True)
    for segment in result.get("segments", []):
       for word in segments.get("words",[]):
           if word["segment"] == segment["id"]:
               start = format_time(word["start"])
               end = format_time(word["end"])
               print(f"[{start} --> {end}] {word['text']}")

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