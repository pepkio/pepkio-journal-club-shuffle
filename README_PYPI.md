# Pepkio Journal Club Shuffle

Automate fair presenter rotations, exclude holiday skip dates, and resolve DOI paper metadata for academic literature reviews using the Pepkio journal-club-shuffle API.

# What It Does

Organizing recurring academic journal clubs and departmental seminars requires balancing presenter frequency, managing holiday skip dates, matching paper reading lists, and generating accessible calendar files. Doing this manually in spreadsheets is time-consuming and often introduces presenter selection bias or scheduling conflicts.

This package connects to the Pepkio Tools API to generate balanced presentation schedules using stochastic weighting algorithms. It accepts lab member rosters, paper DOIs or titles, session start dates, and holiday blackout lists, returning structured rotation schedules, Markdown tables, and iCalendar (.ics) export files.

Programmatic calls require an active network connection and a Pepkio API key (`PEPKIO_API_KEY`).

# Features

- **Weighted Presenter Shuffling**: Balance selection probabilities using equal-weight or seniority-adjusted inverse-history sampling.
- **Skip Date Exclusions**: Automatically bypass institutional holidays, conference dates, and academic breaks.
- **Automated DOI Resolution**: Query Crossref and PubMed APIs to pull article titles, author lists, and journal metadata.
- **Multi-Format Output**: Receive structured JSON, Markdown tables, CSV spreadsheets, and RFC 5545 iCalendar (`.ics`) streams.
- **Reproducible Seeds**: Use integer random seeds for reproducible schedule previews and lab consensus.
- **Python SDK & CLI**: Programmatic access via `PepkioClient` and terminal CLI (`pepkio-journal-club-shuffle`).

# Installation

Install the package via pip:

```bash
pip install pepkio-journal-club-shuffle
```

Set your API key before making API calls:

```bash
export PEPKIO_API_KEY="your_pepkio_api_key"
```

Keys can be generated in your [Pepkio Account API Keys](https://www.pepkio.com/account/api-keys) dashboard.

# Quick Example

```python
from pepkio_journal_club_shuffle import PepkioClient

with PepkioClient() as client:
    payload = {
        "action": "shuffle",
        "members_text": "Alex Chen\nJordan Lee\nSam Patel\nDr. Elena Rostova (0.5x)",
        "papers_text": "10.1126/science.aaf2403\n10.1038/nature23270",
        "settings": {
            "startDate": "2026-09-07",
            "time": "10:00",
            "durationMin": 60,
            "frequency": "weekly",
            "sessionCount": 4,
            "weightingMode": "seniority",
            "skipDates": ["2026-10-12"]
        },
        "seed": 42
    }

    result = client.run(payload)
    print("Status:", result.status)
    print("Permalink:", result.permalink)
    print("\nSchedule Table:\n", result.result.get("markdown_table"))
```

Command-line interface usage:

```bash
pepkio-journal-club-shuffle run --example shuffle_example_lab
```

# Typical Use Cases

- Generating semester-long presenter rotation schedules for academic research groups.
- Coordinating joint departmental literature review series across multiple laboratories.
- Building graduate seminar paper presentation calendars with holiday skip dates.
- Resolving paper titles and author metadata automatically from DOI lists for reading queues.
- Recalibrating remaining unassigned presenter slots when lab members join or defend mid-term.

# Scientific Background

To prevent consecutive presenter assignment clustering, selection probabilities utilize inverse-history weighting:

$$w_i = \frac{r_i}{n_i + 1}, \quad P(i) = \frac{w_i}{\sum_{j=1}^M w_j}$$

where $r_i$ represents the member's academic seniority factor (e.g. $0.5$ for PIs, $1.0$ for full rotation) and $n_i$ is their prior presentation count. Presenter equity across the group is quantified using the Gini coefficient:

$$G = \frac{\sum_{i=1}^M \sum_{j=1}^M |n_i - n_j|}{2 M \sum_{i=1}^M n_i}$$

Input DOIs are validated via regex matching (`10.\d{4,9}/...`) and resolved asynchronously against open bibliometric endpoints (Crossref and PubMed E-utilities). Session dates are recursively calculated using RFC 5545 calendar recurrence logic while skipping defined blackout sets.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/journal-club-shuffle

The web application provides visual schedule editing, instant shareable permalinks, printable meeting worksheets, and interactive calendar previews.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-journal-club-shuffle

Web Application: https://www.pepkio.com/tools/journal-club-shuffle

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro). See https://www.pepkio.com for additional tools and services.

# Keywords

journal club shuffle, journal club generator, lab meeting scheduler, presenter rotation generator, academic paper presentation schedule, weighted presenter shuffle, journal club calendar generator, lab literature review planner, skip date journal club scheduler, DOI paper scheduler, iCal journal club exporter, fair presenter rotation algorithm, stochastic lab meeting scheduler, academic seminar rotation generator, research lab meeting planner, inverse history presenter weighting, Gini coefficient presenter equity, Crossref DOI metadata resolution, PubMed paper title lookup, conference blackout date scheduler, ICS calendar export journal club, python journal club client, pepkio journal club shuffle, bioinformatics lab scheduler, how to schedule lab journal club fairly, how to generate a fair presenter rotation for research lab, how to calculate presenter selection probability in journal club, how to exclude holiday dates from lab meeting schedule, how to resolve paper title from DOI automatically, how to export journal club schedule to google calendar, how to export lab presentation rotation to iCal ics file, how to balance presentation frequency between graduate students and postdocs, how to randomize paper assignment to lab members, how to create a journal club schedule in markdown for notion, how to handle skip dates during conference season in lab meetings, how to compute Gini index of presentation fairness in lab group, how to automate journal club schedule generation with python
