import os
from typing import Optional

DEFAULT_API_BASE_URL = "https://tools.pepkio.com"


def get_default_base_url() -> str:
    """Return configured API base URL from environment or default to production URL."""
    return os.environ.get("PEPKIO_API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


def get_api_key(api_key: Optional[str] = None) -> Optional[str]:
    """Resolve Pepkio API key from parameter or environment variables."""
    if api_key:
        return api_key
    return os.environ.get("PEPKIO_API_KEY") or os.environ.get("LOCAL_PEPKIO_API_KEY")
