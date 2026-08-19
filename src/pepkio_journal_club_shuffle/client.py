from typing import Any, Dict, Optional, Union

import httpx
from pydantic import BaseModel

from .config import get_api_key, get_default_base_url
from .exceptions import PepkioAPIError, PepkioAuthError, PepkioNotFoundError
from .models import RunResult

TOOL_ID = "journal-club-shuffle"


class PepkioClient:
    """Client for interacting with Pepkio journal-club-shuffle REST API tool service."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        verify: Optional[bool] = None,
    ):
        self.base_url = (base_url or get_default_base_url()).rstrip("/")
        self.api_key = get_api_key(api_key)
        self.timeout = timeout

        if verify is None:
            # Disable SSL verification automatically for localtest.me dev domains
            self.verify = "localtest.me" not in self.base_url
        else:
            self.verify = verify

        self._client = httpx.Client(
            base_url=self.base_url, timeout=self.timeout, verify=self.verify
        )

    def __enter__(self) -> "PepkioClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _get_headers(self, requires_auth: bool = True) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        elif requires_auth:
            raise PepkioAuthError(
                "API key is required for authenticated requests. "
                "Set PEPKIO_API_KEY environment variable or pass api_key to PepkioClient."
            )
        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            data = None

        if response.status_code in (401, 403):
            msg = (
                data.get("error", {}).get("message")
                if isinstance(data, dict) and isinstance(data.get("error"), dict)
                else "Authentication failed"
            )
            raise PepkioAuthError(msg, status_code=response.status_code, response_body=data)
        elif response.status_code == 404:
            msg = (
                data.get("error", {}).get("message")
                if isinstance(data, dict) and isinstance(data.get("error"), dict)
                else "Resource not found"
            )
            raise PepkioNotFoundError(msg, status_code=response.status_code, response_body=data)
        elif response.status_code >= 400:
            msg = (
                data.get("error", {}).get("message")
                if isinstance(data, dict) and isinstance(data.get("error"), dict)
                else f"HTTP Error {response.status_code}"
            )
            raise PepkioAPIError(msg, status_code=response.status_code, response_body=data)

        if isinstance(data, dict) and data.get("error"):
            err = data["error"]
            err_msg = err.get("message") if isinstance(err, dict) else str(err)
            raise PepkioAPIError(f"Tool execution error: {err_msg}", response_body=data)

        return data

    def get_manifest(self) -> Dict[str, Any]:
        """Fetch tool manifest containing input schema, examples, and metadata."""
        url = f"/api/tools/v1/tools/{TOOL_ID}/manifest"
        response = self._client.get(url, headers={"Content-Type": "application/json"})
        return self._handle_response(response)

    def run(
        self,
        input_data: Union[Dict[str, Any], BaseModel],
        idempotency_key: Optional[str] = None,
        label: Optional[str] = None,
        share: Optional[str] = None,
    ) -> RunResult:
        """Run the journal-club-shuffle tool synchronously."""
        url = f"/api/tools/v1/tools/{TOOL_ID}/run"
        payload_input = (
            input_data.model_dump(exclude_unset=True)
            if isinstance(input_data, BaseModel)
            else input_data
        )

        options: Dict[str, Any] = {}
        if idempotency_key:
            options["idempotency_key"] = idempotency_key
        if label:
            options["label"] = label
        if share:
            options["share"] = share

        payload: Dict[str, Any] = {"input": payload_input}
        if options:
            payload["options"] = options

        headers = self._get_headers(requires_auth=True)
        response = self._client.post(url, json=payload, headers=headers)
        data = self._handle_response(response)
        return RunResult(**data)

    def get_run(self, run_id: str) -> RunResult:
        """Retrieve details/status of a specific run by ID."""
        url = f"/api/tools/v1/runs/{run_id}"
        headers = self._get_headers(requires_auth=True)
        response = self._client.get(url, headers=headers)
        data = self._handle_response(response)
        return RunResult(**data)
