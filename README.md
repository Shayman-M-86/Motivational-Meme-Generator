# Motivational Meme Generator

Generate captioned images from curated quote sources or user-supplied content. The project bundles a command-line generator alongside a Flask web interface so you can create memes in bulk or on demand.

## Features

- Parse quotes from TXT, CSV, DOCX, and PDF sources via the Quote Engine ingestors.
- Overlay quotes onto images with automatic scaling and contrast-aware text rendering.
- Command-line workflow for batch meme creation or scripted use.
- Flask UI that lets users submit their own quote and image URL.

## Project Structure & Module Roles

| Module | Responsibility | Key Dependencies |
| --- | --- | --- |
| `src/QuoteEngine` | Abstract and concrete ingestors plus the `Quote` model. Handles parsing quotes from multiple file formats. | `pandas`, `python-docx`, `subprocess` + `pdftotext` CLI |
| `src/MemeEngine` | Renders quotes onto images and exports the meme to the configured output directory. | `Pillow` |
| `src/meme.py` | Command-line interface that stitches the Quote and Meme engines together. | Standard library + project modules |
| `src/app.py` | Flask web server, random meme endpoint, and create-your-own form handler. | `Flask`, `requests`, project modules |
| `src/_data` | Sample quotes and images used by the default configuration. | n/a |

## Getting Started

1. **Clone and enter the repo**

   ```bash
   git clone https://github.com/your-user/Motivational-Meme-Generator.git
   cd Motivational-Meme-Generator
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install system dependency for PDF ingestion**
   - Ensure [`pdftotext`](https://www.xpdfreader.com/pdftotext-man.html) from Xpdf is installed and available on your `PATH`. On macOS you can use `brew install xpdf`; Linux distributions usually ship it via the package manager.

## Usage

### CLI

Generate a meme with optional quote and image overrides:

```bash
python src/meme.py \
  --path ./src/_data/photos/dog/xander_1.jpg \
  --body "Adventure is out there" \
  --author "Charles Muntz"
```

Omit any flag to let the tool pick a random fallback. The script prints the path to the generated meme within `src/.tmp`.

### Flask App

1. Start the server:

   ```bash
   flask --app src.app run
   ```

2. Browse to [http://localhost:5000](http://localhost:5000) for a random meme.
3. Visit `/create` to submit an image URL, quote body, and author for custom generation.

## Development Tips

- Set `FLASK_ENV=development` to enable auto-reload while iterating on the web interface.
- When adding new ingestors, register them in `QuoteEngine.ingestor.py` so they participate in the dispatcher.
- Regenerate `requirements.txt` with `pip freeze > requirements.txt` after upgrading packages.

## License

MIT © Shayman-M.
