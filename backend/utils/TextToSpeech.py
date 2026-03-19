from TTS.api import TTS
import soundfile as sf
import numpy as np
import librosa

tts = TTS(
    model_name="tts_models/en/ljspeech/glow-tts",
    progress_bar=False,
    gpu=False
)

def gather_text(text_input, start_time, end_time):
    target_sr = 44100
    target_duration = end_time - start_time

    # Generate TTS
    wav = tts.tts(text_input)

    # Keep as floating point
    wav = np.array(wav, dtype=np.float32)

    # Resample to 44.1 kHz
    wav = librosa.resample(wav, orig_sr=22050, target_sr=target_sr)

    # Measure duration using correct sample rate
    original_duration = librosa.get_duration(y=wav, sr=target_sr)

    # Stretch while still mono float
    rate = original_duration / target_duration
    wav = librosa.effects.time_stretch(y=wav, rate=rate)

    # Force exact final length
    target_samples = int(target_duration * target_sr)

    if len(wav) < target_samples:
        padding = np.zeros(target_samples - len(wav), dtype=np.float32)
        wav = np.concatenate([wav, padding])
    else:
        wav = wav[:target_samples]

    # Convert to PCM16
    wav_int16 = np.int16(np.clip(wav, -1.0, 1.0) * 32767)

    # Make stereo after stretching
    wav_stereo = np.stack([wav_int16, wav_int16], axis=1)

    # Save
    sf.write("output.wav", wav_stereo, target_sr, subtype="PCM_16")
    return wav_stereo

#example usage
gather_text("Flak this", 0, 2)