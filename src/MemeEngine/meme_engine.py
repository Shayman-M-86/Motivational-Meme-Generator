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
        i = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            font = ImageFont.truetype(font_path, size=mid)
            bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            # Check both width and height constraints
            if text_w <= target_width and text_h <= max_height:
                best_font = font   # fits; try bigger
                lo = mid + 1
            else:
                hi = mid - 1       # too big; shrink
            i += 1
        return best_font


    def make_meme(self, img_path: str, quote: str, author: str, width: int) -> str:
        """Create a meme with the given image and quote."""
        with Image.open(img_path) as img:
            img = MemeEngine.scale_image(img, width)
            draw = ImageDraw.Draw(img)

            text = f"{quote}\n- {author}"
            x = (img.width / 2)
            y = (img.height / 2)
            font = MemeEngine.text_scale(draw, text, "arial.ttf", img.width , img.height)

            draw.multiline_text(
                (x + 2, y + 2), text, font=font, fill="black", align="center", spacing=5, anchor="ma"
            )
            draw.multiline_text(
                (x, y), text, font=font, fill="white", align="center", spacing=5, anchor="ma"
            )

            output_path = os.path.join(
                self.output_dir, f".temp_meme_{random.randint(1, 1000000)}.jpg"
            )
            img.save(output_path)
            return output_path
    
    
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
