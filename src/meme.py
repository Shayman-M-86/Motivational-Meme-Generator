
import os
import random
from pathlib import Path
import argparse
import sys

# @TODO Import your Ingestor and MemeEngine classes
from QuoteEngine import Ingestor, Quote
from MemeEngine import MemeEngine

class MemeGenerator:

    def __init__(self):
        self.quotes = set()

    def choice_imgs(self, images_path) -> str:
        """ Choose a random image from the given directory """
        imgs = []
        for root, dirs, files in os.walk(images_path):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
        return img

    def load_quotes(self) -> set[Quote]:
        """ Load all quotes from the various file types """
        quote_files = ['./src/_data/DogQuotes/DogQuotesTXT.txt',
                       './src/_data/DogQuotes/DogQuotesDOCX.docx',
                       './src/_data/DogQuotes/DogQuotesPDF.pdf',
                       './src/_data/DogQuotes/DogQuotesCSV.csv']
        for f in quote_files:
            q = Ingestor.ingest(Path(f))
            self.quotes.update(q)
        return self.quotes

    def generate_meme(self, path=None, body_author: tuple[str, str] | None = None):
        """ Generate a meme given an path and a quote """
        img = None

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
            quote: Quote = Quote(body_author[0], body_author[1])

        meme = MemeEngine('./src/.tmp')
        
        path = meme.make_meme(img, quote.body, quote.author, 500)
        return path


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
        mg = MemeGenerator()
        body_author = (args.body, args.author) if args.body and args.author else None
        path_arg = (args.path,) if args.path else None
        try:
            result = mg.generate_meme(path=path_arg, body_author=body_author)
            print(result)
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    # meme_gen = MemeGenerator()
    # for i in range(10):
    #     print(meme_gen.generate_meme()) 
