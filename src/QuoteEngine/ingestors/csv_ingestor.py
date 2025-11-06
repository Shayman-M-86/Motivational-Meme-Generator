from ..ingestor_interface import IngestorInterface
from ..quote_model import Quote

from pathlib import Path
import pandas as pd


class CsvIngestor(IngestorInterface):
    """Ingestor for CSV files."""

    extension: str = ".csv"

    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from a CSV file."""
        cls._extension_exception(path)

        quotes: list[Quote] = []
        try:
            df = pd.read_csv(path)
            for _, row in df.iterrows():
                body = row["body"]
                author = row["author"]
                quotes.append(Quote(body, author))
        except Exception as e:
            cls._exception_handler(e)

        return quotes
