import subprocess
from pathlib import Path

# key -> (sample_rate_hz, ffmpeg_codec, human label, filename suffix)
PCM_FORMATS: dict[str, tuple[int, str, str, str]] = {
    "44100_16": (44100, "pcm_s16le", "44.1 kHz / 16-bit PCM", "44k1_16bit"),
    "44100_24": (44100, "pcm_s24le", "44.1 kHz / 24-bit PCM", "44k1_24bit"),
    "48000_24": (48000, "pcm_s24le", "48 kHz / 24-bit PCM", "48k_24bit"),
    "96000_24": (96000, "pcm_s24le", "96 kHz / 24-bit PCM", "96k_24bit"),
}


def convert_pcm(
    input_path: Path,
    output_path: Path,
    sample_rate: int,
    codec: str,
) -> subprocess.CompletedProcess:
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-c:a",
        codec,
        "-ar",
        str(sample_rate),
        str(output_path),
    ]
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
