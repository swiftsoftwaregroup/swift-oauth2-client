import pytest
import respx
import httpx
from oauth2_client import OAuth2Config, new_api_client_async
from oauth2_client.exceptions import TokenRefreshError, APIError

@pytest.fixture
def oauth2_config():
    return OAuth2Config(
        token_url="http://api.example.com/token",
        client_id="test_client_id",
        client_secret="test_client_secret",
        scopes=["api:read", "api:write"]
    )

@pytest.fixture
def base_url():
    return "http://api.example.com"

@pytest.mark.asyncio
@respx.mock
async def test_token_refresh(oauth2_config, base_url):
    respx.post(oauth2_config.token_url).mock(
        return_value=httpx.Response(200, json={
            "access_token": "test_access_token",
            "expires_in": 3600
        })
    )

    async with new_api_client_async(oauth2_config, base_url) as client:
        token = await client.token_manager.get_valid_token()
        assert token == "test_access_token"

@pytest.mark.asyncio
@respx.mock
async def test_token_refresh_error(oauth2_config, base_url):
    respx.post(oauth2_config.token_url).mock(
        return_value=httpx.Response(400, json={"error": "invalid_client"})
    )

    async with new_api_client_async(oauth2_config, base_url) as client:
        with pytest.raises(TokenRefreshError):
            await client.token_manager.get_valid_token()

@pytest.mark.asyncio
@respx.mock
async def test_api_call_success(oauth2_config, base_url):
    respx.post(oauth2_config.token_url).mock(
        return_value=httpx.Response(200, json={
            "access_token": "test_access_token",
            "expires_in": 3600
        })
    )
    respx.get(f"{base_url}/api/test").mock(
        return_value=httpx.Response(200, json={"message": "Success"})
    )

    async with new_api_client_async(oauth2_config, base_url) as client:
        response, status_code = await client.call_api("GET", "/api/test")
        assert status_code == 200
        assert response == {"message": "Success"}

@pytest.mark.asyncio
@respx.mock
async def test_api_call_error(oauth2_config, base_url):
    respx.post(oauth2_config.token_url).mock(
        return_value=httpx.Response(200, json={
            "access_token": "test_access_token",
            "expires_in": 3600
        })
    )
    respx.get(f"{base_url}/api/test").mock(
        return_value=httpx.Response(404, json={"error": "Not found"})
    )

    async with new_api_client_async(oauth2_config, base_url) as client:
        with pytest.raises(APIError):
            await client.call_api("GET", "/api/test")

@pytest.mark.asyncio
@respx.mock
async def test_download_file(oauth2_config, base_url, tmp_path):
    respx.post(oauth2_config.token_url).mock(
        return_value=httpx.Response(200, json={
            "access_token": "test_access_token",
            "expires_in": 3600
        })
    )
    respx.get(f"{base_url}/api/download").mock(
        return_value=httpx.Response(200, content=b"file content")
    )

    async with new_api_client_async(oauth2_config, base_url) as client:
        dest_path = tmp_path / "downloaded_file.txt"
        result = await client.download_file("GET", "/api/download", dest_path=dest_path)
        assert result == f"File downloaded successfully as {dest_path}"
        assert dest_path.read_text() == "file content"

@pytest.mark.asyncio
@respx.mock
async def test_different_content_types(oauth2_config, base_url):
    respx.post(oauth2_config.token_url).mock(
        return_value=httpx.Response(200, json={
            "access_token": "test_access_token",
            "expires_in": 3600
        })
    )
    
    # Test JSON response
    respx.get(f"{base_url}/api/json").mock(
        return_value=httpx.Response(200, json={"key": "value"}, headers={"Content-Type": "application/json"})
    )
    
    # Test text response
    respx.get(f"{base_url}/api/text").mock(
        return_value=httpx.Response(200, content="Hello, World!", headers={"Content-Type": "text/plain"})
    )
    
    # Test binary response
    respx.get(f"{base_url}/api/binary").mock(
        return_value=httpx.Response(200, content=b"\x00\x01\x02", headers={"Content-Type": "application/octet-stream"})
    )

    async with new_api_client_async(oauth2_config, base_url) as client:
        # Test JSON response
        response, status_code = await client.call_api("GET", "/api/json")
        assert status_code == 200
        assert response == {"key": "value"}

        # Test text response
        response, status_code = await client.call_api("GET", "/api/text")
        assert status_code == 200
        assert response == "Hello, World!"

        # Test binary response
        response, status_code = await client.call_api("GET", "/api/binary")
        assert status_code == 200
        assert response == b"\x00\x01\x02"

@pytest.mark.asyncio
async def test_token_expiration(oauth2_config, base_url, mocker):
    mock_time = mocker.patch('time.time')
    mock_time.return_value = 0

    async with new_api_client_async(oauth2_config, base_url) as client:
        client.token_manager.access_token = "old_token"
        client.token_manager.expires_at = 100

        # Token is still valid
        mock_time.return_value = 50
        token = await client.token_manager.get_valid_token()
        assert token == "old_token"

        # Token has expired
        mock_time.return_value = 150
        mocker.patch.object(client.token_manager, 'refresh_token', return_value=None)
        await client.token_manager.get_valid_token()
        client.token_manager.refresh_token.assert_called_once()
