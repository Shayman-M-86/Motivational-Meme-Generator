from ..ingestor_interface import IngestorInterface, IngestorException
from ..quote_model import Quote

from pathlib import Path
import re
import subprocess


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
