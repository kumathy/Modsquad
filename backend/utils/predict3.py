"""
This script is to run the real time audio transcription feature, still realtively slow
but its a start
This is a test file for all the functionlity before i add it to predict 2 on my local system
"""
import sounddevice as sd
import numpy as np
import queue
import time
from faster_whisper import WhisperModel
import re


SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_DURATION = 0.3   # seconds per audio chunk
BUFFER_DURATION = 2.0  # rolling buffer size
DEVICE = None          # default mic
MODEL_SIZE = "small"   # tiny / base / small / medium
BANNED = {"fuck", "shit", "damn"}
MAX_LEN= max(len(w) for w in BANNED)

audio_queue = queue.Queue()
timestamps = queue.Queue()
rolling_buffer = np.zeros(int(SAMPLE_RATE * BUFFER_DURATION), dtype=np.float32)
file= open("transcript.txt", "a")
model = WhisperModel(
    MODEL_SIZE,
    device="auto",      # for gpu change this to "cuda"    
    compute_type="int8" # for gpu change this to float16
)

def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())
    timestamps.put(time.perf_counter())

def normalize_audio(audio):
    return audio / max(0.01, np.max(np.abs(audio)))

def flagging(text):
    keywords = {"fuck", "shit", "damn"}
    token= text.split()
    censor=[w if w.lower() not in keywords else "*"*len(w) for w in token]
    return " ".join(censor)

class ProfanityFilter:
    def __init__(self, banned):
        self.banned = banned
        self.buffer = ""

    def process(self, text):
        text = text.lower()
        combined = self.buffer + text

        censored = combined
        for w in self.banned:
            censored = re.sub(w, "*" * len(w), censored)

        # keep only the tail to catch cross-chunk swears
        self.buffer = combined[-MAX_LEN:]

        return censored[len(self.buffer):]

print("Press Ctrl+C to stop")
filter= ProfanityFilter(BANNED)

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
            capture_time = timestamps.get()
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
            for seg in segments:
                print_time = time.perf_counter()
                latency = print_time - capture_time
                file.write(f"[{latency*1000:.1f} ms]"+"amount of ms taken for this line\n")
                clean = filter.process(seg.text)
                file.write(clean+"\n")
            """
            text = " ".join(seg.text.strip() for seg in segments)
            

            
            if text and text != last_transcript:
                text2=flagging(text)
                ##print("\r📝", text2, end="", flush=True)
                file.write(text2+"\n")
                last_transcript = text
            """

            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\nStopped.")
