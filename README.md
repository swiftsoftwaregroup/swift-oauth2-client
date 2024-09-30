# Swift OAuth2 Client

[![PyPI version](https://badge.fury.io/py/swift-oauth2-client.svg)](https://badge.fury.io/py/swift-oauth2-client)

Swift OAuth2 Client is a Python SDK that provides a simple and efficient way to interact with OAuth2-protected APIs. It handles token management, API calls, and file downloads with support for asynchronous operations.

## Features

- Asynchronous API calls using `httpx`
- Automatic token management and renewal
- Support for various request body types and response formats
- File download capabilities
- Easy-to-use interface with type hints
- Comprehensive documentation

## Installation

```bash
pip install swift-oauth2-client
```

## Quick Start

Here's a basic example of how to use the Swift OAuth2 Client:

```python
from oauth2_client import OAuth2Config, new_api_client

config = OAuth2Config(
    token_url="https://api.example.com/oauth/token",
    client_id="your_client_id",
    client_secret="your_client_secret",
    scopes=["read", "write"]
)

with new_api_client(config, "https://api.example.com") as client:
    response, status = client.call_api("GET", "/users")
    print(f"Status: {status}, Response: {response}")
```

Asynchronous usage:

```python
import asyncio
from oauth2_client import OAuth2Config, new_api_client_async

async def main():
    config = OAuth2Config(
        token_url="https://api.example.com/oauth/token",
        client_id="your_client_id",
        client_secret="your_client_secret",
        scopes=["read", "write"]
    )

    async with new_api_client_async(config, "https://api.example.com") as client:
        response, status = await client.call_api("GET", "/users")
        print(f"Status: {status}, Response: {response}")

asyncio.run(main())
```

For more comprehensive examples, check out the `examples/oauth2_client_example_async.py` and `examples/oauth2_client_example.py`files in the repository.

## Documentation

For detailed documentation, including API reference and usage guides, visit our [documentation site](https://swiftsoftwaregroup.github.io/swift-oauth2-client).

## Development

To set up the development environment:

1. Ensure you have Poetry installed
2. Clone the repository
3. Run `poetry install` to install dependencies
4. Run tests with `poetry run pytest`

## Docs

1. Build documentation with `poetry run mkdocs build` 
2. Serve the documentation with `poetry run mkdocs serve`. 
3. Open a web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## License

This project is licensed under the Apache License, Version 2.0.