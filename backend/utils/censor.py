
from transcribe import process_timestamps, transcribe_audio
from bleep_alg import bleep_video

def censor_video(input_path, output_path):
    result = transcribe_audio(input_path)
    timestamps = result["timestamp"]
    bleep_video(input_path,output_path,timestamps,use_bleep=True,bleep_duration=None)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_path = sys.argv[3]
    censor_video(audio_file, output_path)


