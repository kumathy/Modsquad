import whisperx
import logging
import torch
logger = logging.getLogger(__name__)
def get_best_device():
    if torch.cuda.is_available():
        return "cuda"   
    else:
        return "cpu"
DEVICE=get_best_device()
COMPUTE_TYPE="float16" if DEVICE!="cpu" else "int8"
MODEL_SIZE="medium.en"
logger.info("Loading Whisper model...")
model = whisperx.load_model(
    MODEL_SIZE,
    device=DEVICE,      # for gpu change this to "cuda"    
    compute_type=COMPUTE_TYPE # for gpu change this to float16
)

align_model, align_metadata = whisperx.load_align_model(
    language_code="en",
    device=DEVICE
)
logger.info("Whisper models loaded successfully")
def process_timestamps(ts_list):
    print("Processing timestamps:")
    for ts in ts_list:
        print(ts)

def transcribe_audio(audio_path: str) -> dict:
    audio=whisperx.load_audio(audio_path)
    logger.info(f"Transcribing: {audio_path}")
    result = model.transcribe(audio)
    result = whisperx.align(result["segments"], align_model, align_metadata, audio, device=DEVICE)
    logger.info(f"Transcription complete: {len(result['segments'])} segments")

    temp = []
    for segment in result["segments"]:
        for word in segment.get("words", []):
            if "start" in word and "end" in word:
                temp.append([float(word["start"]), float(word["end"]), word["word"]])
    process_timestamps(temp)

    return {
        "text": "".join([s["text"] for s in result["segments"]]),
        "language": "en",
        "segments": [
            {"text": s["text"], "start": s["start"], "end": s["end"]}
            for s in result["segments"]
        ],
        "timestamp": temp
    }
"""
def format_time(t):
    hrs, rem = divmod(t, 3600)
    mins, secs = divmod(rem, 60)
    ms = int((t - int(t)) * 1000)
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02},{ms:03}"
"""
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
    #print(f"Language: {result['language']}")
    print(f"Segments: {len(result['segments'])}")
    print(f"\nTranscript:\n{result['text']}")
    print("="*60)