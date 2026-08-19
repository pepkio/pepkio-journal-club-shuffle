import os

import pytest

from pepkio_journal_club_shuffle import PepkioClient, RunResult


@pytest.fixture
def client():
    base_url = os.environ.get("PEPKIO_API_BASE_URL", "https://tools.pepkio.com")
    api_key = os.environ.get("PEPKIO_API_KEY") or os.environ.get("LOCAL_PEPKIO_API_KEY")
    if not api_key:
        pytest.skip("Neither PEPKIO_API_KEY nor LOCAL_PEPKIO_API_KEY environment variable is set.")

    with PepkioClient(api_key=api_key, base_url=base_url) as c:
        yield c


def test_integration_manifest(client):
    manifest = client.get_manifest()
    assert manifest.get("tool_id") == "journal-club-shuffle"
    assert "input" in manifest
    assert "examples" in manifest


def test_integration_run_shuffle(client):
    paper1 = "Spatial transcriptomics [10.1126/science.aaf2403]"
    paper2 = "CRISPR screening [10.1038/nature23270]"
    paper3 = "Melanoma Anti-PD-1 Therapy"
    payload = {
        "action": "shuffle",
        "members_text": "Dr. Martinez (0.5x)\nAlex Chen\nJordan Lee\nSam Patel\n",
        "papers_text": f"{paper1}\n{paper2}\n{paper3}\n",
        "settings": {
            "startDate": "2026-10-05",
            "time": "10:00",
            "durationMin": 60,
            "frequency": "weekly",
            "sessionCount": 3,
            "weightingMode": "seniority",
        },
        "seed": 42,
    }
    result = client.run(payload)
    assert isinstance(result, RunResult)
    assert result.status == "completed"
    assert result.result is not None
    assert result.run_id is not None

    # Test get_run
    run_info = client.get_run(result.run_id)
    assert run_info.run_id == result.run_id
    assert run_info.status == "completed"


def test_integration_run_export_csv(client):
    payload = {
        "action": "export",
        "format": "csv",
        "sessions": [
            {
                "sessionNumber": 1,
                "date": "2026-10-05",
                "time": "10:00",
                "durationMin": 60,
                "presenter": "Alex Chen",
                "paper": "Single-cell RNA-seq reveals immune landscape in melanoma",
            }
        ],
    }
    result = client.run(payload)
    assert isinstance(result, RunResult)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("mime_type") == "text/csv"
    assert "content" in result.result


def test_integration_run_resolve_doi(client):
    payload = {"action": "resolve_doi", "doi": "10.1126/science.aaf2403"}
    result = client.run(payload)
    assert isinstance(result, RunResult)
    assert result.status == "completed"
    assert result.result is not None
    assert "resolved_title" in result.result
