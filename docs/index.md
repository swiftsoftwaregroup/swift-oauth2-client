# Welcome to Swift OAuth2 Client

Swift OAuth2 Client is a Python SDK that simplifies interaction with OAuth2-protected APIs. This documentation will guide you through the installation, usage, and API reference of the SDK.

## Installation

You can install Swift OAuth2 Client using pip:

```bash
pip install swift-oauth2-client
```

## Basic Usage

Here's a quick example of how to use Swift OAuth2 Client:

```python
import asyncio
from oauth2_client import OAuth2Config, new_api_client

async def main() -> None:
    config = OAuth2Config(
        token_url="https://api.example.com/oauth/token",
        client_id="your_client_id",
        client_secret="your_client_secret",
        scopes=["read", "write"]
    )

    async with new_api_client(config, "https://api.example.com") as client:
        response, status_code = await client.call_api("GET", "/api/resource")
        print(f"Response (status {status_code}): {response}")

asyncio.run(main())
```

For more detailed information, check out the [API Reference](api_reference.md).