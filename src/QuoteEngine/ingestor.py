from . import ingestor_interface as II
from pathlib import Path
from .quote_model import Quote


class Ingestor:
    """Ingestor for multiple file types.
    This class selects the appropriate ingestor based on the file extension
    and uses it to ingest quotes from the file.
    """

    ingestors = {
        ".csv": II.CsvIngestor,
        ".docx": II.DocxIngestor,
        ".pdf": II.PdfIngestor,
        ".txt": II.TxtIngestor,
    }

    @classmethod
    def _get_ingestor(cls, path: Path) -> II.IngestorInterface | None:
        """Check if any ingestor can ingest the given file."""

        extension = path.suffix.lower()
        return cls.ingestors.get(extension)

    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from the given file using the appropriate ingestor."""
        ingestor = cls._get_ingestor(path)
        if ingestor:
            return ingestor.ingest(path)
        raise II.IngestorException(
            cls.__name__,
            f"No ingestor found for file type: '{path.suffix.lower()}'. Supported file types: {list(cls.ingestors.keys())}",
        )




if __name__ == "__main__":
    test_path = Path("./src/_data/DogQuotes/DogQuotesPNG.png")

    quotes: list[Quote] = Ingestor.ingest(test_path)
    for quote in quotes:
        print(quote)
    pass
