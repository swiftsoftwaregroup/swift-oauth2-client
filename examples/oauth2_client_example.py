import asyncio
import os
from oauth2_client import OAuth2Config, new_api_client
from oauth2_client.exceptions import OAuth2ClientError

async def main():
    # Configure the OAuth2 client
    config = OAuth2Config(
        token_url="https://api.example.com/oauth/token",
        client_id=os.getenv("OAUTH_CLIENT_ID", "your_client_id"),
        client_secret=os.getenv("OAUTH_CLIENT_SECRET", "your_client_secret"),
        scopes=["read", "write"]
    )
    base_url = "https://api.example.com"

    try:
        async with new_api_client(config, base_url) as client:
            # Make a GET request
            print("Making a GET request...")
            response, status_code = await client.call_api("GET", "/api/user")
            print(f"Response (status {status_code}):")
            print(response)

            # Make a POST request
            print("\nMaking a POST request...")
            data = {"name": "John Doe", "email": "john@example.com"}
            response, status_code = await client.call_api("POST", "/api/user", body=data)
            print(f"Response (status {status_code}):")
            print(response)

            # Download a file
            print("\nDownloading a file...")
            result = await client.download_file("GET", "/api/document", dest_path="downloaded_document.pdf")
            print(result)

    except OAuth2ClientError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())