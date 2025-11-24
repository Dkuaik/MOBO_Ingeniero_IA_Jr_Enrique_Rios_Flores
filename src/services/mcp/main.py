import uvicorn
from mcp.server import FastMCP

app = FastMCP("usd-price-server")

#Definición de la tool sobre el precio actual del dolar
@app.tool()
async def get_usd_price():
    """Get the current USD exchange rates from open.er-api.com"""
    import requests
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        response.raise_for_status()
        data = response.json()
        return str(data)
    except Exception as e:
        return f"Error fetching USD price: {str(e)}"

if __name__ == "__main__":
    uvicorn.run(app.sse_app(), host="0.0.0.0", port=8003) #montado de servidor