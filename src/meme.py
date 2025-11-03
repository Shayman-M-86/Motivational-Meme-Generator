
import os
import random
from pathlib import Path

# @TODO Import your Ingestor and MemeEngine classes
from QuoteEngine import Ingestor, Quote
from MemeEngine import MemeEngine

class MemeGenerator:

    def __init__(self):
        self.quotes = set()

    def choice_imgs(self, images_path):
        """ Choose a random image from the given directory """
        imgs = []
        for root, dirs, files in os.walk(images_path):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
        return img
    
    def load_quotes(self):
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
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    meme_gen = MemeGenerator()
    for i in range(2):
        meme_gen.generate_meme()
