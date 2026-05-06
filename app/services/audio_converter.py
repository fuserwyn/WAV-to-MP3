import subprocess
from pathlib import Path


def convert_wav_to_mp3(input_path: Path, output_path: Path) -> subprocess.CompletedProcess:
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-codec:a",
        "libmp3lame",
        "-q:a",
        "2",
        str(output_path),
    ]
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )


def convert_audio(input_path: Path, output_path: Path) -> subprocess.CompletedProcess:
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        str(output_path),
    ]
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
