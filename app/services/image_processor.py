from pathlib import Path

from PIL import Image

TARGET_SIZE = 3000


def resize_to_square(input_path: Path, output_path: Path, size: int = TARGET_SIZE) -> None:
    with Image.open(input_path) as img:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        fitted = img.copy()
        fitted.thumbnail((size, size), Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", (size, size), (255, 255, 255))
        x = (size - fitted.width) // 2
        y = (size - fitted.height) // 2
        if fitted.mode == "RGBA":
            canvas.paste(fitted, (x, y), fitted)
        else:
            canvas.paste(fitted, (x, y))

        canvas.save(output_path, format="JPEG", quality=95)
