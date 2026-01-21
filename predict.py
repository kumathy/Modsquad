"""
This is to run the transcription model with an uploaded audio file
Can be Mp3, Wav, etc
"""
import whisper

model = whisper.load_model("tiny.en")
result = model.transcribe("Beautiful_Now(256k).mp3")

print(type(result))
