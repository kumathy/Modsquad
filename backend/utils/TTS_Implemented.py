from kokoro import KPipeline
import soundfile as sf
import numpy as np
import librosa

pipeline = KPipeline(lang_code="a")  

def gather_text(text_input, start_time, end_time, output_file="output.wav"):
    target_sr = 44100
    target_duration = end_time - start_time

    chunks = []
    for _, _, audio in pipeline(text_input, voice="af_heart", speed=1):
        chunks.append(np.array(audio, dtype=np.float32))

    if not chunks:
        raise ValueError("No audio was generated.")

    wav = np.concatenate(chunks)

    wav = librosa.resample(wav, orig_sr=24000, target_sr=target_sr)

    original_duration = len(wav) / target_sr
    if target_duration > 0 and original_duration > 0:
        rate = original_duration / target_duration
        wav = librosa.effects.time_stretch(wav, rate=rate)


    target_samples = int(target_duration * target_sr)
    if len(wav) < target_samples:
        wav = np.concatenate(
            [wav, np.zeros(target_samples - len(wav), dtype=np.float32)]
        )
    else:
        wav = wav[:target_samples]


    wav_int16 = np.int16(np.clip(wav, -1.0, 1.0) * 32767)
    wav_stereo = np.stack([wav_int16, wav_int16], axis=1)

    sf.write(output_file, wav_stereo, target_sr, subtype="PCM_16")
    return wav_stereo


#example usage
gather_text("Flak this", 0, 2)