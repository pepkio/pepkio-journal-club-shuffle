# Pepkio Journal Club Shuffle

Python client for the Pepkio `journal-club-shuffle` tool — fair presenter and paper rotation for recurring lab journal clubs with weighted shuffle, skip dates, and CSV/iCal/Markdown export.

## Installation

```bash
pip install pepkio-journal-club-shuffle
```

Or using `uv`:

```bash
uv add pepkio-journal-club-shuffle
```

## Quick Start

### Python API

Set your Pepkio API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_pepkio_api_key"
```

Run shuffle in Python:

```python
from pepkio_journal_club_shuffle import PepkioClient

with PepkioClient() as client:
    # 1. Fetch manifest metadata
    manifest = client.get_manifest()
    print("Tool Title:", manifest["title"])

    # 2. Run shuffle action
    result = client.run({
        "action": "shuffle",
        "members_text": "Dr. Martinez (0.5x)\nAlex Chen\nJordan Lee\nSam Patel\nRiley Kim\n",
        "papers_text": "Visualization and analysis of gene expression in tissue sections by spatial transcriptomics [10.1126/science.aaf2403]\nIn vivo CRISPR screening identifies Ptpn2 as a cancer immunotherapy target [10.1038/nature23270]\n",
        "settings": {
            "startDate": "2026-10-05",
            "time": "10:00",
            "durationMin": 60,
            "frequency": "weekly",
            "sessionCount": 2,
            "weightingMode": "seniority"
        },
        "seed": 42
    })

    print("Status:", result.status)
    print("Result:", result.result)
    print("Permalink:", result.permalink)
```

### Command Line Interface (CLI)

```bash
# Print tool manifest
pepkio-journal-club-shuffle manifest

# Run built-in manifest example
pepkio-journal-club-shuffle run --example shuffle_example_lab

# Run custom JSON payload
pepkio-journal-club-shuffle run --input-json '{"action": "resolve_doi", "doi": "10.1126/science.aaf2403"}'

# Fetch run result by ID
pepkio-journal-club-shuffle get-run <run_id>
```

## API Base URL Override

For local development or testing against custom environments, set `PEPKIO_API_BASE_URL`:

```bash
export PEPKIO_API_BASE_URL="https://tools.localtest.me"
export PEPKIO_API_KEY="your_local_key"
```

## Web Application

Web UI available at: https://www.pepkio.com/tools/journal-club-shuffle

## License

MIT License
