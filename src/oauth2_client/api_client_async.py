import json
from typing import Dict, Any, Optional, Union, Tuple
from urllib.parse import urlencode
from pathlib import Path

import httpx

from .config import OAuth2Config
from .token_manager import TokenManager
from .exceptions import APIError

class APIClientAsync:
    """
    Asynchronous client for making authenticated API calls using OAuth2.

    This class handles API calls, including automatic token management
    and request/response processing.

    Attributes:
        base_url (str): The base URL for API calls.
        token_manager (TokenManager): Manages OAuth2 tokens.
        http_client (httpx.AsyncClient): Asynchronous HTTP client.

    Example:
        ```python
        config = OAuth2Config(...)
        async with APIClientAsync(config, "https://api.example.com") as client:
            response, status = await client.call_api("GET", "/users")
        ```
    """

    def __init__(self, config: Optional[OAuth2Config], base_url: str):
        """
        Initialize the APIClientAsync.

        Args:
            config (Optional[OAuth2Config]): OAuth2 configuration. If None, no authentication is used.
            base_url (str): The base URL for API calls.
        """
        self.base_url = base_url
        self.token_manager = TokenManager(config) if config else None
        self.http_client = httpx.AsyncClient(follow_redirects=True)

    async def call_api(self, method: str, path: str, body: Any = None, additional_headers: Optional[Dict[str, str]] = None) -> Tuple[Union[bytes, str, Dict], int]:
        """
        Make an authenticated API call.

        Args:
            method (str): HTTP method (e.g., "GET", "POST").
            path (str): API endpoint path.
            body (Any, optional): Request body. Defaults to None.
            additional_headers (Optional[Dict[str, str]], optional): Additional HTTP headers. Defaults to None.

        Returns:
            Tuple[Union[bytes, str, Dict], int]: Response body and status code.

        Raises:
            APIError: If the API call fails.

        Example:
            ```python
            response, status = await client.call_api("GET", "/users")
            print(f"Status: {status}, Response: {response}")
            ```
        """
        headers = additional_headers.copy() if additional_headers else {}
        
        if self.token_manager:
            token = await self.token_manager.get_valid_token()
            headers["Authorization"] = f"Bearer {token}"

        if isinstance(body, str):
            headers.setdefault("Content-Type", "text/plain")
        elif isinstance(body, bytes):
            headers.setdefault("Content-Type", "application/octet-stream")
        elif isinstance(body, dict):
            body = urlencode(body)
            headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
        elif body is not None:
            body = json.dumps(body)
            headers.setdefault("Content-Type", "application/json")

        try:
            response = await self.http_client.request(method, self.base_url + path, content=body, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(f"API call failed: {e}") from e

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return response.json(), response.status_code
        elif "text/" in content_type:
            return response.text, response.status_code
        else:
            return response.content, response.status_code

    async def download_file(self, method: str, path: str, body: Any = None, additional_headers: Optional[Dict[str, str]] = None, dest_path: Optional[Union[str, Path]] = None) -> Union[str, bytes]:
        """
        Download a file from the API.

        Args:
            method (str): HTTP method (usually "GET").
            path (str): API endpoint path.
            body (Any, optional): Request body. Defaults to None.
            additional_headers (Optional[Dict[str, str]], optional): Additional HTTP headers. Defaults to None.
            dest_path (Optional[Union[str, Path]], optional): Destination path to save the file. If None, returns the file content.

        Returns:
            Union[str, bytes]: File content or success message.

        Example:
            ```python
            result = await client.download_file("GET", "/files/document.pdf", dest_path="local_document.pdf")
            print(result)
            ```
        """
        content, _ = await self.call_api(method, path, body, additional_headers)

        if dest_path:
            dest_path = Path(dest_path)
            if isinstance(content, str):
                dest_path.write_text(content, encoding="utf-8")
            elif isinstance(content, bytes):
                dest_path.write_bytes(content)
            else:  # For JSON content
                dest_path.write_text(json.dumps(content, indent=2), encoding="utf-8")
            return f"File downloaded successfully as {dest_path}"
        else:
            return content

    async def close(self):
        """Close the HTTP client session."""
        await self.http_client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


def new_api_client_async(config: Optional[OAuth2Config], base_url: str) -> APIClientAsync:
    """
    Create a new APIClientAsync instance.

    Args:
        config (Optional[OAuth2Config]): OAuth2 configuration. If None, no authentication is used.
        base_url (str): The base URL for API calls.

    Returns:
        APIClientAsync: A new APIClientAsync instance.

    Example:
        ```python
        config = OAuth2Config(...)
        client = new_api_client_async(config, "https://api.example.com")
        async with client:
            # Use the client
        ```
    """
    return APIClientAsync(config, base_url)
