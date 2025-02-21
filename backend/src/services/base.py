import requests

from core.logging import logger


class APIClient:
    """Lightweight API client to handle requests."""

    def __init__(self, base_url: str, timeout: tuple[int, int] = (5, 10)):
        self.base_url = base_url
        self.timeout = timeout
        self.base_headers = {"Content-Type": "application/json"}

    def get(self, endpoint: str, headers: dict = None, params: dict = None):
        """Handles GET requests."""
        url = f"{self.base_url}{endpoint}"
        combined_headers = {**self.base_headers, **(headers or {})}
        try:
            response = requests.get(
                url, headers=combined_headers, params=params, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"GET request to {url} failed: {e}")
            raise
