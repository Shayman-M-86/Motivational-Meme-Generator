from PIL import Image, ImageDraw, ImageFont
import os
import random



class MemeEngine:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path: str, quote: str, author: str) -> str:
        """Create a meme with the given image and quote."""
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)

        # Load a font
        font = ImageFont.truetype("arial.ttf", 36)

        # Draw the quote and author on the image
        draw.text((10, 10), f"{quote}\n- {author}", font=font, fill="white")

        # Save the meme
        output_path = os.path.join(self.output_dir, f"meme_{random.randint(1, 10000)}.jpg")
        img.save(output_path)
        return output_path
