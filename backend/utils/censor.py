
from transcribe import transcribe_audio
from bleep_alg import bleep_video
from wordList_Loader import find_timestamp_matches
def censor_video(input_path, output_path):
    result = transcribe_audio(input_path)
    timestamps=find_timestamp_matches(result, "wordlist.txt")
    bleep_video(input_path,output_path,timestamps,use_bleep=True,bleep_duration=None)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_path = sys.argv[3]
    censor_video(audio_file, output_path)


