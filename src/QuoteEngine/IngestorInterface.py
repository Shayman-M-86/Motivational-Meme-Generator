from __future__ import annotations
from abc import ABC, abstractmethod
from quote_model import Quote
from pathlib import Path
import pandas as pd
from docx import Document



class IngestorException(Exception):
    """Custom exception for Ingestor errors."""
    def __init__(self, ingestor_type: str, reason: str):
        msg = f"Ingestor: {ingestor_type} invalid: {reason}"
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
    def ingest_exception(cls, path: Path) -> None:
        """Raise an IngestorException indicating invalid ingestion."""
        if not cls.can_ingest(path):
            raise IngestorException(cls.__name__, "Cannot ingest file type")
    
    
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


class TextIngestor(IngestorInterface):
    """Ingestor for text files."""
    extension: str = '.txt'
    
    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from a text file."""
        cls.ingest_exception(path)

        quotes: list[Quote] = []
        try:
            with open(path, 'r', encoding='utf-8') as file:
                for raw_line in file:
                    quote = cls._parse_quote_line(raw_line)
                    if quote:
                        quotes.append(quote)
        except Exception as e:
            raise IngestorException('TextIngestor', str(e))

        return quotes

class CSVIngestor(IngestorInterface):
    """Ingestor for CSV files."""
    extension: str = '.csv'
    
    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from a CSV file."""
        cls.ingest_exception(path)

        quotes: list[Quote] = []
        try:
            df = pd.read_csv(path)
            for _, row in df.iterrows():
                body = row['body']
                author = row['author']
                quotes.append(Quote(body, author))
        except Exception as e:
            raise IngestorException('CSVIngestor', str(e))

        return quotes


class DocxIngestor(IngestorInterface):
    """Ingestor for DOCX files."""
    extension: str = '.docx'
    
    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from a DOCX file."""
        cls.ingest_exception(path)

        quotes: list[Quote] = []
        try:
            doc = Document(str(path))
            for para in doc.paragraphs:
                quote = cls._parse_quote_line(para.text)
                if quote:
                    quotes.append(quote)
        except Exception as e:
            raise IngestorException('DocxIngestor', str(e))

        return quotes






if __name__ == "__main__":
    # Simple test cases to verify the functionality of IngestorInterface and TextIngestor
    test_path = Path('./src/_data/DogQuotes/DogQuotesDOCX.docx')
    try:
        if DocxIngestor.can_ingest(test_path):
            quotes: list[Quote] = DocxIngestor.ingest(test_path)
            for quote in quotes:
                print(quote)
        else:
            print(f"Cannot ingest file: {test_path}")
    except IngestorException as e:
        print(e)