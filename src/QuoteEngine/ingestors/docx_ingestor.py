from ..ingestor_interface import IngestorInterface
from ..quote_model import Quote

from pathlib import Path
from docx import Document


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
