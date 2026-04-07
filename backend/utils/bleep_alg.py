import subprocess
import shutil

def _probe_audio(input_path):
    """Get audio sample rate and channel count from the input file."""
    result = subprocess.run(
        ["ffprobe", "-v", "error",
         "-select_streams", "a:0",
         "-show_entries", "stream=sample_rate,channels",
         "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1", str(input_path)],
        capture_output=True, text=True, check=True,
    )
    info = {}
    for line in result.stdout.strip().splitlines():
        key, val = line.split("=")
        info[key] = val
    return int(info["sample_rate"]), int(info["channels"]), float(info["duration"])


def bleep_video(input_path,
                output_path,
                intervals,
                use_bleep=True,
                buffer=0.0):

    if not intervals:
        print("No intervals provided -> copying original video")
        shutil.copy2(str(input_path), str(output_path))
        return

    sample_rate, channels, total_duration = _probe_audio(input_path)
    print(f"Audio: {sample_rate}Hz, {channels}ch, {total_duration:.2f}s")

    # Apply buffer and merge overlapping intervals
    buffered = [
        [max(0.0, s - buffer), min(total_duration, e + buffer)]
        for s, e in intervals
    ]

    ivals = sorted(buffered)
    merged = []
    for curr in ivals:
        if not merged or merged[-1][1] < curr[0]:
            merged.append(curr)
        else:
            merged[-1][1] = max(merged[-1][1], curr[1])

    # Build ffmpeg enable expression for censored regions
    between_parts = []
    for start, end in merged:
        if start >= end:
            print(f"Warning: skipping zero-length interval [{start}, {end}]")
            continue
        print(f"Censor: {start:.3f}s - {end:.3f}s")
        between_parts.append(f"between(t\\,{start:.6f}\\,{end:.6f})")

    if not between_parts:
        print("No valid intervals after merging -> copying original video")
        shutil.copy2(str(input_path), str(output_path))
        return

    enable_expr = "+".join(between_parts)

    if use_bleep:
        # Mute original during intervals, generate matching sine bleep, mix together
        chan_layout = "mono" if channels == 1 else "stereo"
        audio_filter = (
            f"[0:a]volume=0:enable='{enable_expr}'[muted];"
            f"sine=frequency=1000:sample_rate={sample_rate}:duration={total_duration:.6f},"
            f"volume=0.8:enable='{enable_expr}',"
            f"volume=0:enable='not({enable_expr})',"
            f"aformat=channel_layouts={chan_layout}[bleep];"
            f"[muted][bleep]amix=inputs=2:duration=first:normalize=0[out]"
        )
    else:
        # Just mute original audio during intervals
        audio_filter = f"[0:a]volume=0:enable='{enable_expr}'[out]"

    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "warning",
            "-i", str(input_path),
            "-filter_complex", audio_filter,
            "-map", "0:v:0",
            "-map", "[out]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-movflags", "+faststart",
            str(output_path),
        ],
        check=True,
    )
