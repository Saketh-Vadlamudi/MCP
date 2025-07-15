# weather.py - Try explicitly running uvicorn
import os
os.environ["FASTMCP_PORT"] = "3000" # This sets the default port for FastMCP

from mcp.server.fastmcp import FastMCP
import aiohttp
from dotenv import load_dotenv
import uvicorn # <-- Add this import

load_dotenv()

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "❌ Error: API key not found."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key, "units": "metric"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as resp:
                resp.raise_for_status()
                data = await resp.json()
                if data.get("cod") == "404":
                    return f"❌ City '{location}' not found."

                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                city = data["name"]
                country = data["sys"]["country"]

                return (f"🌤️ Weather in {city}, {country}: {weather}. "
                        f"{temp}°C (feels like {feels_like}°C), {humidity}% humidity.")
    except Exception as e:
        return f"⚠️ Error fetching weather: {e}"

if __name__ == "__main__":
    print("🔌 Starting Weather MCP server on port 3000...")
    # Get the ASGI app from FastMCP
    app = mcp.streamable_http_app() # This gets the FastAPI app that FastMCP creates

    # Explicitly run with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000) # Ensure host and port match