from __future__ import annotations

from . import ingestors as ingestors_pkg
from .ingestor_interface import IngestorException, IngestorInterface
from .quote_model import Quote

from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules



def _discover_ingestors() -> dict[str, type[IngestorInterface]]:
    """Import every module in the ingestors package and collect concrete ingestors."""
    registry: dict[str, type[IngestorInterface]] = {}

    for module_info in iter_modules(ingestors_pkg.__path__):
        module = import_module(f"{ingestors_pkg.__name__}.{module_info.name}")
        for candidate in vars(module).values():
            if not (isclass(candidate) and issubclass(candidate, IngestorInterface)):
                continue
            if candidate is IngestorInterface:
                continue
            extension = getattr(candidate, "extension", "")
            if not extension:
                continue
            registry[extension.lower()] = candidate

    return registry


class Ingestor:
    """Ingestor for multiple file types.
    This class selects the appropriate ingestor based on the file extension
    and uses it to ingest quotes from the file.
    """

    ingestors = _discover_ingestors()

    @classmethod
    def _get_ingestor(cls, path: Path) -> type[IngestorInterface] | None:
        """Check if any ingestor can ingest the given file."""

        extension = path.suffix.lower()
        return cls.ingestors.get(extension)

    @classmethod
    def ingest(cls, path: Path) -> list[Quote]:
        """Ingest quotes from the given file using the appropriate ingestor."""
        ingestor = cls._get_ingestor(path)
        if ingestor:
            return ingestor.ingest(path)
        raise IngestorException(
            cls.__name__,
            f"No ingestor found for file type: '{path.suffix.lower()}'. Supported file types: {list(cls.ingestors.keys())}",
        )


if __name__ == "__main__":
    test_path = Path("./src/_data/DogQuotes/DogQuotesPNG.png")

    quotes: list[Quote] = Ingestor.ingest(test_path)
    for quote in quotes:
        print(quote)
