"""Command-line utilities for generating motivational memes."""

import argparse
import os
import random
import sys
from pathlib import Path

try:  # pragma: no cover - enable execution both as module and script
    from .MemeEngine import MemeEngine
    from .QuoteEngine import Ingestor, Quote
except ImportError:  # pragma: no cover
    from MemeEngine import MemeEngine  # type: ignore
    from QuoteEngine import Ingestor, Quote  # type: ignore


class MemeGenerator:
    """Generate memes from random or user-supplied inputs."""

    def __init__(self) -> None:
        self.quotes: set[Quote] = set()

    # Helper utilities ---------------------------------------------------------
    def choice_imgs(self, images_path: str) -> str:
        """Choose a random image from the provided directory tree."""
        images: list[str] = []
        for root, _, files in os.walk(images_path):
            images.extend(os.path.join(root, name) for name in files)

        return random.choice(images)

    def load_quotes(self) -> set[Quote]:
        """Load all quotes from the various supported file types."""
        quote_files = [
            "./src/_data/DogQuotes/DogQuotesTXT.txt",
            "./src/_data/DogQuotes/DogQuotesDOCX.docx",
            "./src/_data/DogQuotes/DogQuotesPDF.pdf",
            "./src/_data/DogQuotes/DogQuotesCSV.csv",
        ]
        for file_path in quote_files:
            ingested_quotes = Ingestor.ingest(Path(file_path))
            self.quotes.update(ingested_quotes)
        return self.quotes

    def generate_meme(
        self, path: tuple[str, ...] | None = None, body_author: tuple[str, str] | None = None
    ) -> str:
        """Generate a meme from a random or provided image and quote data."""
        if path is None:
            images_path = "./src/_data/photos/dog/"
            img = self.choice_imgs(images_path)
        else:
            img = path[0]

        if not self.quotes:
            self.quotes = self.load_quotes()
        quote: Quote = random.choice(list(self.quotes))

        if body_author and (not isinstance(body_author, tuple) or len(body_author) != 2):
            raise ValueError("body_author must be a tuple of (body, author) or None")

        if body_author:
            quote = Quote(body_author[0], body_author[1])

        meme_engine = MemeEngine("./src/.tmp")
        meme_path = meme_engine.make_meme(img, quote.body, quote.author, 500)
        return meme_path


# CLI entry point ---------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a meme")
    parser.add_argument("-p", "--path", help="Path to an image file")
    parser.add_argument("-b", "--body", help="Quote body text")
    parser.add_argument("-a", "--author", help="Quote author")
    args = parser.parse_args()

    if (args.body and not args.author) or (args.author and not args.body):
        print("Error: --body and --author must be provided together.", file=sys.stderr)
        sys.exit(2)

    if args.path and not os.path.isfile(args.path):
        print(f"Error: Image path not found: {args.path}", file=sys.stderr)
        sys.exit(2)

    if args.path or args.body or args.author:
        meme_generator = MemeGenerator()
        body_author = (args.body, args.author) if args.body and args.author else None
        path_arg = (args.path,) if args.path else None
        try:
            result = meme_generator.generate_meme(path=path_arg, body_author=body_author)
            print(result)
            sys.exit(0)
        except Exception as exc:  # noqa: BLE001 - surface as CLI error
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)


    # meme_gen = MemeGenerator()
    # for _ in range(5):
    #     print(meme_gen.generate_meme())
