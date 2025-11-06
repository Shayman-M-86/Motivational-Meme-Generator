from ..quote_model import Quote
from ..ingestor_interface import IngestorInterface

from pathlib import Path


class TxtIngestor(IngestorInterface):
    """Ingestor for text files."""

    extension: str = ".txt"

    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from a text file."""
        cls._extension_exception(path)

        quotes: list[Quote] = []
        try:
            with open(path, "r", encoding="utf-8") as file:
                for raw_line in file:
                    quote = cls._parse_quote_line(raw_line)
                    if quote:
                        quotes.append(quote)
        except Exception as e:
            cls._exception_handler(e)

        return quotes
