# Pepkio Journal Club Shuffle

Python client for the Pepkio `journal-club-shuffle` tool — fair presenter and paper rotation for recurring lab journal clubs with weighted shuffle, skip dates, and CSV/iCal/Markdown export.

## Installation

```bash
pip install pepkio-journal-club-shuffle
```

## Quick Start

```python
from pepkio_journal_club_shuffle import PepkioClient

with PepkioClient() as client:
    result = client.run({
        "action": "shuffle",
        "members_text": "Alex Chen\nJordan Lee\n",
        "papers_text": "Paper Title 1\nPaper Title 2\n",
        "settings": {
            "startDate": "2026-10-05",
            "time": "10:00",
            "durationMin": 60,
            "frequency": "weekly",
            "sessionCount": 2,
            "weightingMode": "equal"
        }
    })
    print(result.result)
```

## CLI Usage

```bash
pepkio-journal-club-shuffle manifest
pepkio-journal-club-shuffle run --example shuffle_example_lab
```

Web application: https://www.pepkio.com/tools/journal-club-shuffle
