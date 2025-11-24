import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.clients.mcp.mcp_client import MCPClient


class TestMCPClient:
    """Test MCP client."""

    def test_init(self):
        """Test MCP client initialization."""
        client = MCPClient()
        assert client.url == "http://mcp:8002"

    def test_init_custom_url(self):
        """Test MCP client with custom URL."""
        client = MCPClient("http://custom:9000")
        assert client.url == "http://custom:9000"

    @pytest.mark.asyncio
    @patch('src.clients.mcp.mcp_client.sse_client')
    async def test_get_usd_price(self, mock_sse_client):
        """Test getting USD price."""
        # Mock the transport and session
        mock_transport = AsyncMock()
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.content = [MagicMock()]
        mock_result.content[0].text = "USD Price: 1.0"

        mock_session.call_tool.return_value = mock_result
        mock_sse_client.return_value.__aenter__.return_value = mock_transport
        mock_session.__aenter__.return_value = mock_session

        with patch('src.clients.mcp.mcp_client.ClientSession', return_value=mock_session):
            client = MCPClient()
            result = await client.get_usd_price()
            assert result == "USD Price: 1.0"
            mock_session.call_tool.assert_called_once_with("get_usd_price", {})