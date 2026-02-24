from faster_whisper import WhisperModel
import logging

logger = logging.getLogger(__name__)
MODEL_SIZE="medium.en"

logger.info("Loading Whisper model...")
model = WhisperModel(
    MODEL_SIZE,
    device="auto",      # for gpu change this to "cuda"    
    compute_type="auto" # for gpu change this to float16
)
logger.info("Whisper model loaded successfully")


def transcribe_audio(audio_path: str) -> dict:
    temp = []
    logger.info(f"Transcribing: {audio_path}")

    segments,info = model.transcribe(audio_path,
                                        word_timestamps=True,
                                        beam_size=5,
                                        vad_filter=False)
    segments = list(segments)
    full_text=[]
    temp=[]
    for segment in segments:
        full_text.append(segment.text)
        for word in segment.words:
            temp.append([word.start, word.end, word.word])
                  
    logger.info(f"Transcription complete: {len(segments)} segments")
    return {
        "text": "".join(full_text),
        "language": info.language,
        "segments": [
            {"text": s.text} 
            for s in segments
        ],
        "timestamp":temp
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