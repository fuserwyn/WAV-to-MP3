from pathlib import Path

from PIL import Image

TARGET_SIZE = 3000
COVER_SIZES = (3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000)


def resize_to_square(input_path: Path, output_path: Path, size: int = TARGET_SIZE) -> None:
    with Image.open(input_path) as img:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        scale = min(size / img.width, size / img.height)
        new_width = max(1, round(img.width * scale))
        new_height = max(1, round(img.height * scale))
        fitted = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", (size, size), (255, 255, 255))
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        if fitted.mode == "RGBA":
            canvas.paste(fitted, (x, y), fitted)
        else:
            canvas.paste(fitted, (x, y))

        canvas.save(output_path, format="JPEG", quality=95)
