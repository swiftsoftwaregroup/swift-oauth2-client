from dataclasses import dataclass
from typing import List

@dataclass
class OAuth2Config:
    """
    Configuration class for OAuth2 authentication.

    This class holds the necessary information for OAuth2 authentication,
    including the token URL, client credentials, and requested scopes.

    Attributes:
        token_url (str): The URL to obtain the OAuth2 token.
        client_id (str): The client ID for OAuth2 authentication.
        client_secret (str): The client secret for OAuth2 authentication.
        scopes (List[str]): A list of scopes to request for the OAuth2 token.

    Example:
        ```python
        config = OAuth2Config(
            token_url="https://api.example.com/oauth/token",
            client_id="your_client_id",
            client_secret="your_client_secret",
            scopes=["read", "write"]
        )
        ```
    """

    token_url: str
    client_id: str
    client_secret: str
    scopes: List[str]