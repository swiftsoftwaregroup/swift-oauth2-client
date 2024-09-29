"""
A synchronous client for making authenticated API calls using OAuth2.
"""
import asyncio
from typing import Dict, Any, Optional, Union, Tuple
from pathlib import Path
from .config import OAuth2Config

from .api_client_async import APIClientAsync
from .token_manager import TokenManager

class APIClient:
    """
    Client for making authenticated API calls using OAuth2.

    This class provides a synchronous interface for API calls, internally using
    an asynchronous client.

    Attributes:
        token_manager (TokenManager): Manages OAuth2 tokens synchronously.
        async_client (APIClientAsync): The underlying asynchronous client.
    """

    def __init__(self, config: Optional[OAuth2Config], base_url: str):
        """
        Initialize the APIClient.

        Args:
            config (Optional[OAuth2Config]): OAuth2 configuration. If None, no authentication is used.
            base_url (str): The base URL for API calls.
        """
        self._loop = asyncio.new_event_loop()
        self.async_client = self._loop.run_until_complete(APIClientAsync(config, base_url).__aenter__())
        self.token_manager = TokenManager(self.async_client.token_manager, self._loop)

    def call_api(self, method: str, path: str, body: Any = None, additional_headers: Optional[Dict[str, str]] = None) -> Tuple[Union[bytes, str, Dict], int]:
        """
        Make an API call.

        Args:
            method (str): HTTP method (e.g., "GET", "POST").
            path (str): API endpoint path.
            body (Any, optional): Request body. Defaults to None.
            additional_headers (Optional[Dict[str, str]], optional): Additional HTTP headers. Defaults to None.

        Returns:
            Tuple[Union[bytes, str, Dict], int]: Response body and status code.

        Example:
            ```python
            response, status_code = client.call_api("GET", "/users")
            print(f"Status: {status_code}, Response: {response}")
            ```
        """
        return self._loop.run_until_complete(self.async_client.call_api(method, path, body, additional_headers))

    def download_file(self, method: str, path: str, body: Any = None, additional_headers: Optional[Dict[str, str]] = None, dest_path: Optional[Union[str, Path]] = None) -> Union[str, bytes]:
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
            result = client.download_file("GET", "/files/document.pdf", dest_path="local_document.pdf")
            print(result)
            ```
        """
        return self._loop.run_until_complete(self.async_client.download_file(method, path, body, additional_headers, dest_path))

    def close(self):
        """
        Close the client and its underlying resources.

        This method should be called when the client is no longer needed.
        """
        self._loop.run_until_complete(self.async_client.__aexit__(None, None, None))
        self._loop.close()

    def __enter__(self):
        """
        Enter the runtime context related to this object.

        Returns:
            APIClient: The client instance.

        Example:
            ```python
            with APIClient(config, "https://api.example.com") as client:
                response, status = client.call_api("GET", "/users")
            ```
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context related to this object.

        This method calls `close()` to ensure all resources are properly released.
        """
        self.close()

def new_api_client(config: Optional[OAuth2Config], base_url: str) -> APIClient:
    """
    Create a new APIClient instance.

    Args:
        config (Optional[OAuth2Config]): OAuth2 configuration. If None, no authentication is used.
        base_url (str): The base URL for API calls.

    Returns:
        APIClient: A new APIClient instance.

    Example:
        ```python
        config = OAuth2Config(...)
        client = new_api_client(config, "https://api.example.com")
        ```
    """
    return APIClient(config, base_url)