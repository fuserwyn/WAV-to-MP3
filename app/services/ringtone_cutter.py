import subprocess
from pathlib import Path

ALLOWED_DURATIONS = {30, 45, 60}


def parse_timecode(value: str) -> float:
    value = value.strip().replace(",", ".")
    if ":" in value:
        parts = value.split(":")
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        raise ValueError("Invalid time format")
    return float(value)


def parse_ringtone_input(text: str) -> tuple[float, int | None]:
    parts = text.split()
    if len(parts) == 1:
        return parse_timecode(parts[0]), None
    if len(parts) == 2:
        duration = int(parts[1])
        if duration not in ALLOWED_DURATIONS:
            raise ValueError("Duration must be 30, 45 or 60 seconds")
        return parse_timecode(parts[0]), duration
    raise ValueError("Use format: 1:30 45 or 90 60")


def cut_ringtone(
    input_path: Path,
    output_path: Path,
    start_sec: float,
    duration_sec: int,
    output_format: str = "mp3",
) -> subprocess.CompletedProcess:
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start_sec),
        "-i",
        str(input_path),
        "-t",
        str(duration_sec),
    ]
    if output_format == "wav":
        command.extend(["-c:a", "pcm_s24le"])
    else:
        command.extend(["-codec:a", "libmp3lame", "-q:a", "2"])
    command.append(str(output_path))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
