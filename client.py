# client.py
import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import traceback

print("🔧 Loading environment variables...")
load_dotenv()

async def main():
    print("🚀 Starting main()...")

    groq_api_key = os.getenv("GROQ_API_KEY")
    openweathermap_api_key = os.getenv("OPENWEATHER_API_KEY")

    print("🔑 GROQ_API_KEY:", "FOUND ✅" if groq_api_key else "❌ MISSING")
    print("🌦️  OPENWEATHER_API_KEY:", "FOUND ✅" if openweathermap_api_key else "⚠️ MISSING (used by weather.py)")

    if not groq_api_key:
        print("❌ Error: GROQ_API_KEY not found in .env file.")
        return
    if not openweathermap_api_key:
        print("⚠️ Warning: OPENWEATHER_API_KEY not found in .env file of the client.")

    os.environ["GROQ_API_KEY"] = groq_api_key

    print("⚙️  Initializing MultiServerMCPClient...")
    client = MultiServerMCPClient(
        {
            "Math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "Weather": {
                "transport": "streamable_http",
                "url": "http://localhost:3000"
            }
        }
    )

    print("🛠️  Getting tools from servers...")
    try:
        tools = await client.get_tools()
        print(f"✅ Successfully fetched {len(tools)} tools:")
        for tool in tools:
            print(f"   🔹 {tool.name}: {tool.description}")
    except Exception as e:
        print("❌ Error fetching tools:", e)
        traceback.print_exception(type(e), e, e.__traceback__)
        return

    print("🧠 Initializing Groq model...")
    try:
        model = ChatGroq(model="llama3-70b-8192")
        print("✅ Groq model initialized.")
    except Exception as e:
        print("❌ Failed to initialize Groq model:", e)
        return

    print("🤖 Creating React-style agent with tools...")
    try:
        agent = create_react_agent(model, tools)
        print("✅ Agent created.")
    except Exception as e:
        print("❌ Failed to create agent:", e)
        return

    print("💬 Sending math question to agent...")
    try:
        math_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
        )
        print("\n--- ✅ Math Response ---")
        print("🧠 Agent Thought:", math_response['messages'][0].content)
        print("🟢 Final Answer:", math_response['messages'][-1].content)
    except Exception as e:
        print("❌ Math query failed:", e)

    print("💬 Sending weather question to agent...")
    try:
        weather_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "what is the weather in Hyderabad, India?"}]}
        )
        print("\n--- ✅ Weather Response ---")
        print("🧠 Agent Thought:", weather_response['messages'][0].content)
        print("🟢 Final Answer:", weather_response['messages'][-1].content)
    except Exception as e:
        print("❌ Weather query failed:", e)

    print("💬 Sending weather query for invalid city...")
    try:
        invalid_weather_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "what is the weather in NotARealCityHere?"}]}
        )
        print("\n--- 🧪 Weather (Invalid City) Response ---")
        print("🧠 Agent Thought:", invalid_weather_response['messages'][0].content)
        print("🟢 Final Answer:", invalid_weather_response['messages'][-1].content)
    except Exception as e:
        print("❌ Invalid city query failed:", e)

    print("✅ All done!")

asyncio.run(main())
