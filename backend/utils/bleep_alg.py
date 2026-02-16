from moviepy import *
import numpy as np
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent


def make_silence(duration):
    return AudioClip(lambda t: 0 * t, duration=duration, fps=44100)

def make_censor_bleep(duration=0.3, freq=1000, volume=0.8, fps=44100):
    t = np.linspace(0, duration, int(duration * fps), endpoint=False)
    val = volume * np.sin(2 * np.pi * freq * t)
    stereo = np.column_stack((val, val))   # shape (n_samples, 2)
    return AudioArrayClip(stereo, fps=fps)

def bleep_video(input_path, output_path, start_time, end_time, use_bleep=True, bleep_duration=None):
    video = VideoFileClip(input_path)
    original_audio = video.audio

    if original_audio is None:
        raise ValueError("Video has no audio track")
    
    duration = original_audio.duration
    fps = original_audio.fps

    if start_time < 0 or end_time > duration or start_time >= end_time:
        raise ValueError("Invalid time rnage")
    
    segment_dration = end_time - start_time

    if use_bleep:
        bleep_len = bleep_duration if bleep_duration is not None else segment_dration
        censor_sound = make_censor_bleep(duration=bleep_len)
    else:
        censor_sound = make_silence(segment_dration)
    
    pieces = []

    if start_time > 0:
        pieces.append(original_audio.subclipped(0, start_time))

    pieces.append(censor_sound)

    if end_time < duration:
        pieces.append(original_audio.subclipped(end_time, duration))

    for i, p in enumerate(pieces):
        print(f"Piece {i}: duration={p.duration:.2f}s, nchannels={p.nchannels if hasattr(p,'nchannels') else 'unknown'}")

    final_audio = concatenate_audioclips(pieces)

    final_video = video.with_audio(final_audio)

    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        preset="medium",
        threads=4
    )

    video.close()
    final_video.close()

input_video = SCRIPT_DIR / "TestClip01.mp4"
output_video = SCRIPT_DIR / "output_beep_test01.mp4"

bleep_video(
    str(input_video),
    str(output_video),
    start_time=27,
    end_time=29,
    use_bleep=True,
    bleep_duration=2.0
)