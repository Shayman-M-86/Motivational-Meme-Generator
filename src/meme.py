import os
import random
from pathlib import Path

# @TODO Import your Ingestor and MemeEngine classes
from QuoteEngine import Ingestor, Quote
from MemeEngine import MemeEngine

def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./src/_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = ['./src/_data/DogQuotes/DogQuotesTXT.txt',
                       './src/_data/DogQuotes/DogQuotesDOCX.docx',
                       './src/_data/DogQuotes/DogQuotesPDF.pdf',
                       './src/_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            q = Ingestor.ingest(Path(f))
            print(f'\nIngested {len(q)} quotes from {f} ')
            for quote in q:
                print(quote)
            quotes.extend(q)
        # for quote in quotes:
            # print(quote)
        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = Quote(body, author)

    meme = MemeEngine('./src/.tmp')
    path = meme.make_meme(img, quote.body, quote.author, 500)
    return path


if __name__ == "__main__":
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    for i in range(1):
        generate_meme()
