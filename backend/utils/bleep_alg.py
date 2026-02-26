from moviepy import *
import numpy as np
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent


def make_silence(duration, fps=44100):
    return AudioClip(lambda t: 0 * t, duration=duration, fps=fps)

def make_censor_bleep(duration=0.3, freq=1000, volume=0.8, fps=44100):
    t = np.linspace(0, duration, int(duration * fps), endpoint=False)
    val = volume * np.sin(2 * np.pi * freq * t)
    stereo = np.column_stack((val, val))   # shape (n_samples, 2)
    return AudioArrayClip(stereo, fps=fps)

def bleep_video(input_path,
                output_path,
                intervals,
                use_bleep=True):
    
    video = VideoFileClip(input_path)
    original_audio = video.audio

    if original_audio is None:
        raise ValueError("Video has no audio track")
    
    total_duration = original_audio.duration
    audio_fps = original_audio.fps

    if not intervals:
        print("No intervals provided -> copying original video")
        video.write_videofile(
            str(output_path),
            codec="lidx264",
            audio_codec="aac",
            preset="medium",
            threads=4
        )
        video.close()
        return
    ivals = sorted([list(pair) for pair in intervals])

    merged = []
    for curr in ivals:
        if not merged or merged[-1][1] < curr[0]:
            merged.append(curr)
        else:
            merged[-1][1] = max(merged[-1][1], curr[1])
    
    pieces = []
    last_end = 0.0

    for start, end in merged:
        if start < 0 or end > total_duration or start >= end:
            print(f"Warning: skipping invalid interval [{start}, {end}]")
            continue
        if start > last_end:
            pieces.append(original_audio.subclipped(last_end, start))
        segment_duration = end - start

        if use_bleep:
            censor = make_censor_bleep(duration=segment_duration, fps=audio_fps)
            pieces.append(censor)
        else:
            pieces.append(make_silence(segment_duration, fps=audio_fps))
        last_end = end
    
    if last_end < total_duration:
        pieces.append(original_audio.subclipped(last_end, total_duration))
    
    for i, p in enumerate(pieces):
        ch = p.nchannels if hasattr(p, 'nchannels') else '?'
        print(f"Piece {i:2d}: duration={p.duration:6.2f}s channels={ch}")\
        
    final_audio = concatenate_audioclips(pieces)
    final_video = video.with_audio(final_audio)

    final_video.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        preset="medium",
        threads=4
    )

    video.close()
    final_video.close()

input_video = SCRIPT_DIR / "fixed_input.mp4"
output_video = SCRIPT_DIR / "output_beep_test02.mp4"

censor_intervals = [
    (19.0, 19.5),
    (23.0, 23.5)
]

bleep_video(
    str(input_video),
    str(output_video),
    intervals=censor_intervals,
    use_bleep=True,
)