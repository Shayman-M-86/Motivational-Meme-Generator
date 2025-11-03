from PIL import Image, ImageDraw, ImageFont
import os
import random


ImageType = Image.Image


class MemeEngine:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    @staticmethod
    def scale_image(img: ImageType, width: int) -> ImageType:
        ratio = width / float(img.width)
        height = int(ratio * float(img.height))
        return img.resize((width, height))

    def make_meme(self, img_path: str, quote: str, author: str, width: int) -> str:
        """Create a meme with the given image and quote."""
        with Image.open(img_path) as img:
            img = MemeEngine.scale_image(img, width)
            draw = ImageDraw.Draw(img)

            text = f"{quote}\n- {author}"
            font_length_scale = 0.05 / (len(quote) / 40)  # Adjust scaling factor as needed
            print(font_length_scale)
            font_size = int(img.width * font_length_scale)
            font = ImageFont.truetype("arial.ttf", font_size)

            # Measure text size (modern Pillow)
            bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=5)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            
            x = ((img.width - text_width) / 2) + (
                img.width * random.uniform(-0.08, 0.08)
            )  # Centered horizontally
            y = (
                img.height - text_height - (img.height * random.uniform(0.15, 0.85))
            )  # 15% to 85% from bottom

            # Draw text with subtle shadow
            draw.multiline_text(
                (x + 2, y + 2), text, font=font, fill="black", align="center", spacing=5
            )
            draw.multiline_text(
                (x, y), text, font=font, fill="white", align="center", spacing=5
            )

            output_path = os.path.join(
                self.output_dir, f"meme_{random.randint(1, 10000)}.jpg"
            )
            img.save(output_path)
            return output_path


if __name__ == "__main__":
    meme = MemeEngine("./src/tmp")
    print(
        meme.make_meme(
            "./src/_data/photos/dog/xander_1.jpg",
            "This is a quote",
            "Author Name",
            random.randint(200, 800),
        )
    )
