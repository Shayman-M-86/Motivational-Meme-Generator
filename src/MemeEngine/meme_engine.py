"""Utilities for rendering memes with dynamically scaled text overlays."""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ImageType = Image.Image


class MemeEngine:
    """Create captioned images using Pillow."""

    def __init__(self, output_dir: str | None = None):
        """Initialize MemeEngine with the output directory."""
        if output_dir is None:
            raise ValueError("output_dir must be provided")
        self.output_dir: Path = Path(output_dir)
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)

    @staticmethod
    def scale_image(img: ImageType, width: int) -> ImageType:
        """Resize image to the specified width while maintaining aspect ratio."""
        ratio = width / float(img.width)
        height = int(ratio * float(img.height))
        return img.resize((width, height))

    @staticmethod
    def text_scale(
        draw: ImageDraw.ImageDraw,
        text: str,
        font_path: str,
        img_width: int,
        img_height: int,
    ) -> ImageFont.FreeTypeFont:
        """Return a font sized so text fits within 80% width and 15% height of the image."""
        target_width = img_width * 0.8
        max_height = img_height * 0.15
        spacing = 5

        lo, hi = 20, max(33, img_width // 13)
        best_font = ImageFont.truetype(font_path, size=lo)
        while lo <= hi:
            mid = (lo + hi) // 2
            font = ImageFont.truetype(font_path, size=mid)
            bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            # Check both width and height constraints
            if text_w <= target_width and text_h <= max_height:
                best_font = font  # fits; try bigger
                lo = mid + 1
            else:
                hi = mid - 1  # too big; shrink
        return best_font

    def make_meme(self, img_path: str, quote: str, author: str, width: int = 500) -> str:
        """Create a meme with the given image and quote.

        Args:
            img_path (str): Source image path.
            quote (str): Body text to render.
            author (str): Author attribution.
            width (int, optional): Target width for the output image. Defaults to 500.

        Returns:
            str: Filename of the generated meme relative to the output directory.
        """
        with Image.open(img_path) as img:
            img = MemeEngine.scale_image(img, width)
            draw = ImageDraw.Draw(img)

            text = f"{quote}\n- {author}"
            x = img.width / 2
            y = img.height / 2
            font = MemeEngine.text_scale(draw, text, "arial.ttf", img.width, img.height)

            draw.multiline_text(
                (x + 2, y + 2),
                text,
                font=font,
                fill="black",
                align="center",
                spacing=5,
                anchor="ma",
            )
            draw.multiline_text(
                (x, y),
                text,
                font=font,
                fill="white",
                align="center",
                spacing=5,
                anchor="ma",
            )
            file_name: str = f"temp_meme_{random.randint(1, 1_000_000)}.jpg"
            output_path: Path = self.output_dir / file_name
            img.save(output_path)
            return file_name


if __name__ == "__main__":
    meme = MemeEngine("./src/.tmp")
    print(
        meme.make_meme(
            "./src/_data/photos/dog/xander_1.jpg",
            "Tis",
            "Author Name",
            500,
        )
    )
