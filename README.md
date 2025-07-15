# Multi-Agent Tool Calling with LangChain, Groq, and MCP

A multi-agent system demonstrating dynamic tool discovery and execution using LangChain, Groq's Llama3 model, and the Multi-Server Communication Protocol (MCP). This project showcases how to integrate various tool servers (Math and Weather) with different communication transports (stdio and HTTP streamable) for an intelligent agent to leverage.

## Features

* **Multi-Server Communication Protocol (MCP)**: Utilizes MCP for seamless communication between the central client and independent tool servers.
* **Dynamic Tool Discovery**: The agent client dynamically discovers available tools and their functionalities from registered MCP servers.
* **LangChain Integration**: Leverages LangChain's `create_react_agent` for robust agent behavior and tool orchestration.
* **Groq Llama3 Integration**: Uses the `ChatGroq` model with Llama3-70b-8192 for powerful language understanding and response generation.
* **Diverse Tool Transports**: Demonstrates two types of MCP transports:
    * **Standard I/O (stdio)**: For the `Math` server, showcasing simple, direct process communication.
    * **Streamable HTTP**: For the `Weather` server, demonstrating integration with a `uvicorn`-backed FastAPI application.
* **Weather Tool**: Fetches real-time weather information for a given location using the OpenWeatherMap API.
* **Math Tool**: Performs basic arithmetic operations (addition, multiplication).
* **Error Handling**: Includes basic error handling for API key issues and invalid city queries.

## Project Structure
```bash
multi-agent-mcp-project/
├── .gitignore                 # Files to be ignored by Git
├── client.py                  # The main agent application that orchestrates tools
├── mathserver.py              # MCP server for mathematical operations
├── requirements.txt           # Python dependencies 
├── README.md                  # Project overview, setup, usage
└── weather.py                 # MCP server for fetching weather data 
```

## Installation

Follow these steps to set up and run the project locally:

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/multi-agent-mcp-project.git](https://github.com/your-username/multi-agent-mcp-project.git)
    cd multi-agent-mcp-project
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up environment variables:**

    You need API keys for Groq and OpenWeatherMap.

    * **Groq API Key:** Obtain one from [Groq Console](https://console.groq.com/keys).
    * **OpenWeatherMap API Key:** Obtain one from [OpenWeatherMap](https://openweathermap.org/api).

    Create a `.env` file in the root of your project directory, based on `.env.example`, and populate it with your keys:

    ```bash
    cp .env.example .env
    ```

    Now, open the `.env` file and add your actual API keys:

    ```
    GROQ_API_KEY="your_groq_api_key_here"
    OPENWEATHER_API_KEY="your_openweathermap_api_key_here"
    ```
    Replace `"your_groq_api_key_here"` and `"your_openweathermap_api_key_here"` with your actual API keys.

## Usage

To run the multi-agent system, simply execute the `client.py` script. The `client.py` will automatically start the `mathserver.py` and `weather.py` servers in the background and connect to them.

```bash
python client.py
You will see output similar to this, demonstrating the agent's thought process and the results of tool calls:

🔧 Loading environment variables...
🚀 Starting main()...
🔑 GROQ_API_KEY: FOUND ✅
🌦️  OPENWEATHER_API_KEY: FOUND ✅
⚙️  Initializing MultiServerMCPClient...
🛠️  Getting tools from servers...
✅ Successfully fetched 3 tools:
   🔹 add: Add to numbers
   🔹 multiple: Multiply two numbers
   🔹 get_weather: Get the current weather for a given location. 
🧠 Initializing Groq model...
✅ Groq model initialized.
🤖 Creating React-style agent with tools...
✅ Agent created.
💬 Sending math question to agent...

--- ✅ Math Response ---
🧠 Agent Thought: The user is asking to calculate "(3 + 5) x 12". I need to use the 'add' tool first, then the 'multiple' tool.
🟢 Final Answer: 96
💬 Sending weather question to agent...

--- ✅ Weather Response ---
🧠 Agent Thought: The user is asking for the weather in "Hyderabad, India". I should use the `get_weather` tool with "Hyderabad, India" as the location.
🟢 Final Answer: 🌤️ Weather in Hyderabad, IN: overcast clouds. 29.89°C (feels like 34.02°C), 69% humidity.
💬 Sending weather query for invalid city...

--- 🧪 Weather (Invalid City) Response ---
🧠 Agent Thought: The user is asking for the weather in "NotARealCityHere?". I need to use the `get_weather` tool with "NotARealCityHere?" as the location.
🟢 Final Answer: ❌ City 'NotARealCityHere?' not found.
✅ All done!
How it Works
client.py:

Initializes MultiServerMCPClient to manage connections to different MCP servers.

Defines configurations for the Math server (using stdio transport) and the Weather server (using streamable_http transport via http://localhost:3000).

Fetches available tools from all connected servers.

Initializes the ChatGroq model.

Creates a LangChain React-style agent, providing it with the discovered tools.

Invokes the agent with various prompts to demonstrate its ability to use the add, multiple, and get_weather tools.

mathserver.py:

A simple MCP server that exposes add and multiple functions as tools.

It uses transport="stdio" to communicate via standard input/output streams.

weather.py:

An MCP server that exposes a 

get_weather function as a tool. 

It integrates with the OpenWeatherMap API to fetch weather data. 

It explicitly runs a 

uvicorn server to serve the FastMCP application via HTTP, allowing client.py to connect using streamable_http transport. 


os.environ["FASTMCP_PORT"] = "3000" is set to ensure the weather.py server starts on port 3000. 

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch for your feature or bug fix.

Make your changes.

Write tests for your changes.

Ensure all tests pass.

Submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
