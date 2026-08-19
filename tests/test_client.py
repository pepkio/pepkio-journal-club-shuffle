import httpx
import pytest

from pepkio_journal_club_shuffle import (
    PepkioAPIError,
    PepkioAuthError,
    PepkioClient,
    RunResult,
)


def test_client_init_and_config():
    client = PepkioClient(api_key="test_key", base_url="https://custom.pepkio.com/")
    assert client.base_url == "https://custom.pepkio.com"
    assert client.api_key == "test_key"


def test_get_manifest_mocked(monkeypatch):
    mock_manifest = {
        "schema_version": "1.0",
        "tool_id": "journal-club-shuffle",
        "title": "Journal Club Shuffle",
    }

    def mock_get(url, headers):
        return httpx.Response(200, json=mock_manifest)

    client = PepkioClient(api_key="test_key")
    monkeypatch.setattr(client._client, "get", mock_get)

    manifest = client.get_manifest()
    assert manifest["tool_id"] == "journal-club-shuffle"


def test_run_mocked(monkeypatch):
    mock_run_response = {
        "run_id": "test_run_123",
        "status": "completed",
        "result": {"seed": 42, "sessions": []},
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/test_run_123",
        "permalink": "https://tools.pepkio.com/r/test_run_123",
    }

    def mock_post(url, json=None, headers=None):
        assert url == "/api/tools/v1/tools/journal-club-shuffle/run"
        assert json["input"]["action"] == "shuffle"
        assert headers["Authorization"] == "Bearer test_key"
        return httpx.Response(200, json=mock_run_response)

    client = PepkioClient(api_key="test_key")
    monkeypatch.setattr(client._client, "post", mock_post)

    res = client.run({"action": "shuffle", "seed": 42})
    assert isinstance(res, RunResult)
    assert res.run_id == "test_run_123"
    assert res.status == "completed"
    assert res.result["seed"] == 42


def test_get_run_mocked(monkeypatch):
    mock_run_response = {
        "run_id": "test_run_123",
        "status": "completed",
        "result": {"sessions": []},
        "error": None,
    }

    def mock_get(url, headers=None):
        assert url == "/api/tools/v1/runs/test_run_123"
        return httpx.Response(200, json=mock_run_response)

    client = PepkioClient(api_key="test_key")
    monkeypatch.setattr(client._client, "get", mock_get)

    res = client.get_run("test_run_123")
    assert isinstance(res, RunResult)
    assert res.run_id == "test_run_123"


def test_auth_error_handling(monkeypatch):
    def mock_post(url, json=None, headers=None):
        return httpx.Response(
            401, json={"error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}}
        )

    client = PepkioClient(api_key="invalid_key")
    monkeypatch.setattr(client._client, "post", mock_post)

    with pytest.raises(PepkioAuthError) as exc_info:
        client.run({"action": "shuffle"})
    assert "Invalid API key" in str(exc_info.value)


def test_body_error_handling(monkeypatch):
    def mock_post(url, json=None, headers=None):
        return httpx.Response(
            200, json={"run_id": "123", "status": "failed", "error": "Invalid action parameter"}
        )

    client = PepkioClient(api_key="test_key")
    monkeypatch.setattr(client._client, "post", mock_post)

    with pytest.raises(PepkioAPIError) as exc_info:
        client.run({"action": "invalid"})
    assert "Invalid action parameter" in str(exc_info.value)
