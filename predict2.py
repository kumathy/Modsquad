"""
This script is to run the real time audio transcription feature, still realtively slow
but its a start
Will also add more in this
"""
import sounddevice as sd
import numpy as np
import queue
import time
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_DURATION = 0.5   # seconds per audio chunk
BUFFER_DURATION = 2.0  # rolling buffer size
DEVICE = None          # default mic
MODEL_SIZE = "tiny"   # tiny / base / small / medium



audio_queue = queue.Queue()
rolling_buffer = np.zeros(int(SAMPLE_RATE * BUFFER_DURATION), dtype=np.float32)

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",          
    compute_type="int8"
)

def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

def normalize_audio(audio):
    return audio / max(0.01, np.max(np.abs(audio)))

print("Press Ctrl+C to stop")

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    callback=audio_callback,
    blocksize=int(SAMPLE_RATE * BLOCK_DURATION),
    device=DEVICE
):
    try:
        last_transcript = ""
        while True:

            while not audio_queue.empty():
                chunk = audio_queue.get().flatten()
                rolling_buffer = np.roll(rolling_buffer, -len(chunk))
                rolling_buffer[-len(chunk):] = chunk

            audio_input = normalize_audio(rolling_buffer)


            segments, info = model.transcribe(
                audio_input,
                language="en",
                vad_filter=True,
                beam_size=1
            )

            text = " ".join(seg.text.strip() for seg in segments)


            if text and text != last_transcript:
                print("\r📝", text, end="", flush=True)
                last_transcript = text

            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\nStopped.")
