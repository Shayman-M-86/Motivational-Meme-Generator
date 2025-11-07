from ..ingestor_interface import IngestorInterface
from ..quote_model import Quote

from pathlib import Path
import re

from pypdf import PdfReader


class PdfIngestor(IngestorInterface):
    """Ingestor for PDF files using pypdf."""

    extension: str = ".pdf"

    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from a PDF file."""
        cls._extension_exception(path)

        quotes: list[Quote] = []

        try:
            # Extract text from all pages
            reader = PdfReader(str(path))
            text_parts: list[str] = []
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
            text_content: str = "\n".join(text_parts).strip()

            # Find lines like: "Quote body" - Author
            # (keeps it close to your existing parse logic)
            lines: list[str] = re.findall(r'"[^"\n]+"\s*-\s*[^\n"]+', text_content)

            for raw_line in lines:
                quote: Quote | None = cls._parse_quote_line(raw_line)
                if quote:
                    quotes.append(quote)

        except Exception as e:
            cls._exception_handler(e)

        return quotes
