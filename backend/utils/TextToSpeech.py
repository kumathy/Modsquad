from TTS.api import TTS
import soundfile as sf
import numpy as np
import librosa

tts = TTS(
    model_name="tts_models/en/ljspeech/glow-tts",
    progress_bar=False,
    gpu=False
)

text = "Hello. This is a test of the Glow TTS model running locally."

# Generate audio
wav = tts.tts(text)

# Convert list → numpy
wav = np.array(wav)

# Resample to Mac-friendly 44.1kHz
wav_44k = librosa.resample(wav, orig_sr=22050, target_sr=44100)

# Convert to PCM16
wav_int16 = np.int16(wav_44k * 32767)

# Force stereo (Mac safest)
wav_stereo = np.stack([wav_int16, wav_int16], axis=1)

sf.write("output.wav", wav_stereo, 44100, subtype='PCM_16')

print("Saved Mac-compatible audio.")