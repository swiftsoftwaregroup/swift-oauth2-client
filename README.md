# Swift OAuth2 Client

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
        try:
            response, status_code = await client.call_api("GET", "/api/resource")
            print(f"Response (status {status_code}): {response}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
```

For a more comprehensive example, check out the `examples/oauth2_client_example.py` file in the repository.

## Documentation

For detailed documentation, including API reference and usage guides, visit our [documentation site](https://your-documentation-url.com).

## Development

To set up the development environment:

1. Ensure you have Poetry installed
2. Clone the repository
3. Run `poetry install` to install dependencies
4. Run tests with `poetry run pytest`
5. Build documentation with `poetry run mkdocs build` 
1. Serve the documentation with `poetry run mkdocs serve`. Then open a web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## License

This project is licensed under the Apache License, Version 2.0.