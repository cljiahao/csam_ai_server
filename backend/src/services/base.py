import requests
from pathlib import Path
from contextlib import ExitStack

from core.logging import logger


class APIClient:
    """Lightweight API client to handle requests."""

    def __init__(self, base_url: str, timeout: tuple[int, int] = (5, 10)):
        self.base_url = base_url
        self.timeout = timeout
        self.base_headers = {"Content-Type": "application/json"}
        self.file_headers = {"Accept": "application/json"}

    def get(self, endpoint: str, headers: dict = None, params: dict = None):
        """Handles GET requests."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
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

    def post(self, endpoint: str, data: dict = None, headers: dict = None):
        """Handles POST requests."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        combined_headers = {**self.base_headers, **(headers or {})}
        try:
            response = requests.post(
                url, json=data, headers=combined_headers, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"POST request to {url} failed: {e}")
            raise

    def post_files(
        self,
        endpoint: str,
        file_path_list: dict[str, Path],
        data: dict = None,
        headers: dict = None,
    ):
        """Handles POST requests with a file upload."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        combined_headers = {**self.file_headers, **(headers or {})}

        try:
            # Use ExitStack to manage multiple file context managers
            with ExitStack() as stack:
                files = {
                    key: stack.enter_context(open(path, "rb"))
                    for key, path in file_path_list.items()
                }

                response = requests.post(
                    url,
                    files=files,
                    json=data,
                    headers=combined_headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            logger.error(f"POST file request to {url} failed: {e}")
            raise
