"""
A synchronous wrapper for the asynchronous TokenManagerAsync class.
"""
import asyncio
from .token_manager_async import TokenManagerAsync

class TokenManager:
    """
    A synchronous wrapper for the asynchronous TokenManagerAsync class.

    This class provides a blocking, synchronous interface for acquiring and refreshing
    OAuth2 tokens, using an asyncio event loop to run the asynchronous methods of
    TokenManagerAsync.

    Attributes:
        _async_token_manager (TokenManagerAsync): An instance of the TokenManagerAsync class.
        _loop (asyncio.AbstractEventLoop): The asyncio event loop to run async methods.

    Example usage:
        ```python
        import asyncio
        from token_manager import TokenManager
        from token_manager_async import TokenManagerAsync
        from config import OAuth2Config

        # Step 1: Initialize the OAuth2 configuration
        config = OAuth2Config(
            client_id="your_client_id",
            client_secret="your_client_secret",
            token_url="https://oauth2-server.com/token",
            scopes=["scope1", "scope2"]
        )

        # Step 2: Create an instance of TokenManagerAsync with the configuration
        async_token_manager = TokenManagerAsync(config)

        # Step 3: Get an asyncio event loop (or create a new one)
        loop = asyncio.get_event_loop()

        # Step 4: Initialize the TokenManager with the async token manager and the event loop
        token_manager = TokenManager(async_token_manager=async_token_manager, loop=loop)

        # Step 5: Use the TokenManager to get a valid token synchronously
        token = token_manager.get_valid_token()

        # Output the token
        print(f"Access Token: {token}")
        ```
    """

    def __init__(self, async_token_manager: TokenManagerAsync, loop: asyncio.AbstractEventLoop):
        """
        Initializes the TokenManager with an async token manager and event loop.

        Args:
            async_token_manager (TokenManagerAsync): The asynchronous token manager responsible
                for managing tokens.
            loop (asyncio.AbstractEventLoop): The asyncio event loop used to run async tasks.
        """
        self._async_token_manager = async_token_manager
        self._loop = loop

    def get_valid_token(self) -> str:
        """
        Retrieves a valid OAuth2 token synchronously, refreshing it if necessary.

        This method wraps the async get_valid_token method from TokenManagerAsync and
        runs it in the provided event loop.

        Returns:
            str: A valid OAuth2 access token.
        """
        future = asyncio.ensure_future(self._async_token_manager.get_valid_token(), loop=self._loop)
        return self._loop.run_until_complete(future)

    @property
    def access_token(self) -> str:
        """
        Accesses the current OAuth2 access token.

        Returns:
            str: The current OAuth2 access token.
        """
        return self._async_token_manager.access_token

    @access_token.setter
    def access_token(self, value: str):
        """
        Sets the current OAuth2 access token.

        Args:
            value (str): The new access token.
        """
        self._async_token_manager.access_token = value

    @property
    def expires_at(self) -> float:
        """
        Accesses the expiration time of the current OAuth2 access token.

        Returns:
            float: The expiration time of the token in UNIX time.
        """
        return self._async_token_manager.expires_at

    @expires_at.setter
    def expires_at(self, value: float):
        """
        Sets the expiration time of the current OAuth2 access token.

        Args:
            value (float): The new expiration time in UNIX time.
        """
        self._async_token_manager.expires_at = value

    def refresh_token(self):
        """
        Refreshes the OAuth2 access token synchronously.

        This method wraps the async refresh_token method from TokenManagerAsync and
        runs it in the provided event loop.

        Returns:
            None
        """
        future = asyncio.ensure_future(self._async_token_manager.refresh_token(), loop=self._loop)
        return self._loop.run_until_complete(future)
