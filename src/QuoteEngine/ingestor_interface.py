from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from docx import Document
import subprocess
import re

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



# ---------- Ingestors for different file types


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


class DocxIngestor(IngestorInterface):
    """Ingestor for DOCX files."""

    extension: str = ".docx"

    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from a DOCX file."""
        cls._extension_exception(path)

        quotes: list[Quote] = []
        try:
            doc = Document(str(path))
            for para in doc.paragraphs:
                quote = cls._parse_quote_line(para.text)
                if quote:
                    quotes.append(quote)
        except Exception as e:
            cls._exception_handler(e)

        return quotes


class PdfIngestor(IngestorInterface):
    """Ingestor for PDF files."""

    extension: str = ".pdf"

    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from a PDF file."""
        cls._extension_exception(path)

        quotes: list[Quote] = []
        try:
            # Convert PDF to text using pdftotext command-line tool
            result = subprocess.run(
                ["pdftotext", str(path), "-"], capture_output=True, text=True
            )
            if result.returncode != 0:
                raise IngestorException(
                    cls.__name__,
                    "Failed to convert PDF to text using pdftotext. Ensure pdftotext is installed and accessible.",
                )

            text_content: str = result.stdout.strip()
            lines: list[str] = re.findall(r'"[^"]+" - [^"]+', text_content)

            for raw_line in lines:
                quote: Quote | None = cls._parse_quote_line(raw_line)
                if quote:
                    quotes.append(quote)

        except Exception as e:
            cls._exception_handler(e)

        return quotes


if __name__ == "__main__":
    # Simple test cases to verify the functionality of IngestorInterface and TextIngestor
    test_path = Path("./src/_data/DogQuotes/DogQuotesTXT.txt")

    quotes: list[Quote] = PdfIngestor.ingest(test_path)
    for quote in quotes:
        print(quote)
