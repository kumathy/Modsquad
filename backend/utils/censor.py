"""
This is just a test script to make sure that the fastapi script works locally atleast
"""
from transcribe import transcribe_audio
from bleep_alg import bleep_video
from find_words import find_word_matches
def censor_video(input_path, output_path):
    result = transcribe_audio(input_path)
    matches, timestamps = find_word_matches(result, "wordlist.txt")
    bleep_video(input_path,output_path,timestamps,use_bleep=True)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_path = sys.argv[2]
    censor_video(audio_file, output_path)


