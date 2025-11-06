from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path

from .quote_model import Quote

class IngestorException(Exception):
    """Custom exception for Ingestor errors."""

    def __init__(self, ingestor_type: str, reason: str):
        msg = f"\n\t- Ingestor: {ingestor_type}\n\t- Reason: {reason}"
        super().__init__(msg)


class IngestorInterface(ABC):
    """An abstract base class for quote ingestors."""

    extension: str = ""

    @classmethod
    @abstractmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from file at given path."""
        pass

    # --- helper class methods ---
    @classmethod
    def can_ingest(cls, path: Path) -> bool:
        """Check if the ingestor can handle the file at the given path."""
        return path.suffix.lower() == cls.extension

    @classmethod
    def _extension_exception(cls, path: Path) -> None:
        """Raise an IngestorException if the file extension is not supported."""
        if not cls.can_ingest(path):
            raise IngestorException(
                cls.__name__,
                f"Cannot ingest file type: '{path.suffix.lower()}'. Expected file type: '{cls.extension}'",
            )

    @classmethod
    def _exception_handler(cls, e: Exception) -> None:
        """Handle exceptions raised during ingestion. Re-raise as IngestorException if not already."""
        if isinstance(e, IngestorException):
            raise e
        raise IngestorException(cls.__name__, str(e))

    @staticmethod
    def _parse_quote_line(line: str) -> Quote | None:
        """Parse a line of text into a Quote object if possible."""
        line = line.strip()
        if not line or " - " not in line:
            return None
        body, author = line.split(" - ", maxsplit=1)
        body = body.strip().strip('"').strip("'")
        author = author.strip().strip('"').strip("'")
        return Quote(body.strip(), author.strip())




if __name__ == "__main__":
    pass