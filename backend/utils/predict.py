import whisperx
import gc
from whisperx.diarize import DiarizationPipeline

device = "auto"
audio_file = "backend/utils/song.mp3"
batch_size = 2 
compute_type = "auto"


model = whisperx.load_model("medium.en", device, compute_type=compute_type)


audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)

model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device)

print(result["segments"]) # after alignment