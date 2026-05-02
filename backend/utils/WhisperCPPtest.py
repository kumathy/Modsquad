import subprocess

WHISPER_EXE = "backend/utils/whisper.cpp/build/bin/whisper-stream"
MODEL_PATH = "backend/utils/whisper.cpp/models/ggml-base.en.bin"

command = [
    WHISPER_EXE,
    "-m", MODEL_PATH,
    "-t", "8",
    "--step", "500",
    "--length", "500",
    "-vth", "0.6"
]

process = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

print("Listening...")

for line in process.stdout:
    text = line.strip()

    if not text:
        continue

    # Ignore noisy internal logs if needed
    if text.startswith("whisper_") or text.startswith("main:"):
        continue

    print("Transcript:", text)