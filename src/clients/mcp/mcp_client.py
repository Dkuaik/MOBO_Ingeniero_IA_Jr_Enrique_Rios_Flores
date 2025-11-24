import asyncio
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

class MCPClient:
    def __init__(self, url: str = "http://mcp:8003/sse"):
        self.url = url

    async def get_usd_price(self):
        """Call the get_usd_price tool from the MCP server."""
        async with sse_client(self.url) as transport:
            async with ClientSession(transport) as session:
                await session.initialize()
                result = await session.call_tool("get_usd_price", {})
                if result.content and len(result.content) > 0:
                    return result.content[0].text
                return None

if __name__ == "__main__":
    async def main():
        client = MCPClient()
        try:
            result = await client.get_usd_price()
            print("USD Price Data:", result)
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())