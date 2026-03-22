"""
This is just a test script to make sure that the fastapi script works locally atleast
"""
from transcribe import transcribe_audio
from bleep_alg import bleep_video
from find_words import updated_find_word_matches,find_word_matches
import subprocess
def normalize_video(input_path, output_path):
    subprocess.run([
        "ffmpeg",
        "-i", input_path,
        "-vf", "fps=30",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        output_path
    ])
def censor_video(input_path, output_path):
    if input_path != output_path:
        result = transcribe_audio(input_path)
        normalize_video(input_path, input_path)
        print(result['text'])
        matches, timestamps = updated_find_word_matches(result['timestamp'], "words.txt")
        bleep_video(input_path,output_path,timestamps,use_bleep=True)
    else:
        print("Using the same input output path will cause issues with saving the video"
        "They cannot be the same")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_path = sys.argv[2]
    censor_video(audio_file, output_path)


