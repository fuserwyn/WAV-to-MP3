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


def convert_mp3_to_wav(input_path: Path, output_path: Path) -> subprocess.CompletedProcess:
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-c:a",
        "pcm_s24le",
        str(output_path),
    ]
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )


def convert_audio(input_path: Path, output_path: Path) -> subprocess.CompletedProcess:
    output_ext = output_path.suffix.lower()
    if output_ext == ".mp3":
        return convert_wav_to_mp3(input_path, output_path)
    if output_ext == ".wav":
        return convert_mp3_to_wav(input_path, output_path)
    raise ValueError(f"Unsupported output format: {output_ext}")
