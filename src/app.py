"""Flask routes for generating and rendering motivational memes."""

import glob
import os
import random
from io import BytesIO
from pathlib import Path

import requests
from flask import Flask, abort, render_template, request, url_for
from PIL import Image

from MemeEngine import MemeEngine
from QuoteEngine import Ingestor, Quote


app = Flask(__name__)

# Use the static directory so generated memes are directly accessible by templates.
meme = MemeEngine(app.static_folder)


# Helper utilities -----------------------------------------------------------------
def setup() -> tuple[list[Quote], list[str]]:
    """Load quote and image resources required by the application.

    Returns:
        tuple[list[Quote], list[str]]: A tuple containing a list of quotes and a list of
            image paths discovered within the data directories.
    """
    quote_files = [
        "./src/_data/DogQuotes/DogQuotesTXT.txt",
        "./src/_data/DogQuotes/DogQuotesDOCX.docx",
        "./src/_data/DogQuotes/DogQuotesPDF.pdf",
        "./src/_data/DogQuotes/DogQuotesCSV.csv",
    ]

    quotes: list[Quote] = []
    # Aggregate quotes from every supported source file.
    for file_path in quote_files:
        quotes.extend(Ingestor.ingest(Path(file_path)))

    images_path = "./src/_data/photos/dog/"

    images: list[str] = []
    # Traverse the image directory tree to catalog every available image.
    for root, _, files in os.walk(images_path):
        images.extend(os.path.join(root, name) for name in files)

    return quotes, images


def image_verification(response: requests.Response) -> None:
    """Verify that the HTTP response contains a valid image payload.

    Args:
        response (requests.Response): The response returned from fetching the image URL.

    Raises:
        werkzeug.exceptions.HTTPException: When the response does not represent
            a valid image or cannot be decoded by Pillow.
    """
    is_image_header = response.headers.get("Content-Type", "").startswith("image/")
    if not is_image_header:
        abort(400, description="Not an image (content-type mismatch)")

    try:
        Image.open(BytesIO(response.content)).verify()
    except Exception:  # noqa: BLE001 - surface as HTTP error
        abort(400, description="Invalid image content received")


def verify_format_request_form(
    requested_image_url: str | None,
    body: str | None,
    author: str | None,
) -> tuple[str, str, str]:
    """Validate the incoming meme form data.

    Args:
        requested_image_url (str | None): URL pointing to the image to download.
        body (str | None): Quote body supplied by the user.
        author (str | None): Quote author supplied by the user.

    Returns:
        tuple[str, str, str]: The verified URL, body text, and author string in order.

    Raises:
        werkzeug.exceptions.HTTPException: When validation fails for any field.
    """
    if not requested_image_url:
        abort(400, description="Image URL is required")

    if not body or not author:
        abort(400, description="Both body and author are required")

    if not requested_image_url.lower().startswith(("http://", "https://")):
        abort(400, description="Invalid URL format")

    return requested_image_url, body, author


def render_meme(img_path: Path | str, body: str, author: str):
    """Render a meme given an image path and quote metadata.

    Args:
        img_path (Path | str): The path to the source image.
        body (str): The quote text to render on the image.
        author (str): The author of the quote.

    Returns:
        flask.Response: A rendered meme page with a generated image URL.
    """
    # Clear previous generated artifacts so the static folder only holds the newest meme.
    for file_path in glob.glob("./src/static/temp_meme_*.jpg"):
        os.remove(file_path)

    output_path = meme.make_meme(str(img_path), body, author, 500)
    meme_url = url_for("static", filename=output_path)
    return render_template("meme.html", meme_url=meme_url)


# Preload the core resources once Flask starts.
quotes, imgs = setup()


# Flask routes ---------------------------------------------------------------------
@app.route("/")
def meme_rand():
    """Generate a random meme from the preloaded resources."""

    img = random.choice(imgs)
    quote = random.choice(quotes)
    return render_meme(img, quote.body, quote.author)


@app.route("/create", methods=["GET"])
def meme_form():
    """Display the meme creation form for user-supplied content."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user-defined meme using data submitted from the form."""
    requested_image_url: str | None = request.form.get("image_url")
    body: str | None = request.form.get("body")
    author: str | None = request.form.get("author")

    verified_url, verified_body, verified_author = verify_format_request_form(
        requested_image_url,
        body,
        author,
    )

    response = requests.get(verified_url, timeout=4)
    image_verification(response)

    temp_image_path = Path(f"src/.tmp/temp_image_{random.randint(0, 10000)}")
    # Persist the fetched image locally so MemeEngine can read it from disk.
    with open(temp_image_path, "wb") as temp_file:
        temp_file.write(response.content)

    # Render first, then clean up the temp file to avoid leaving stray artifacts.
    render = render_meme(temp_image_path, verified_body, verified_author)
    os.remove(temp_image_path)
    return render


if __name__ == "__main__":
    app.run()
