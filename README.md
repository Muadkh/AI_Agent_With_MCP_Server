# Personal Technical Assistant (An Agent buit with Open AI Agents SDK Hosted in FastAPI, have Access to MCP Server (via streamable HTTP transport))

This repo containt complete code to create a personal technical assistant. Whose task is to retrieve accurate and up-to-date technical data from websites, online documentation, or repositories based on user queries.
## Features

- FastAPI backend to host the agent 
- OpenAI Agents SDK to run the agent
- MCP server reachable via Streamable HTTP transport
- Streamlit frontend as the chat UI
- AI Model (gemini-2.0-flash) 
- Agent Have Internal Session based Memory

## Prerequisites

- Python 3.11 or higher
- Basic knowledge of FastAPI and REST APIs
- MCP Python SDK
- OpenAI Agents SDK
- Streamlit
- Tavilt-python
- UV package Manager

## Getting Started

1. **Clone the Repository**:

  git clone git@github.com:Muadkh/AI_Agent_With_MCP_Server.git
  cd AI_Agent_With_MCP_Server

2. **Install Dependencies**:
```
- pip install uv (Install Package Manager)
- Run uv sync (Will Install all depedencies)
- source .venv/bin/activate (Activate your .venv folder) 
  ```
3. **Set Up Environment Variables**:
Create a `.env` file in the api directory and add your API keys.
  ```env
  GEMINI_API_KEY=
  OPENAI_API_KEY= (For Tracing Only)
  TAVILY_API_KEY=
  Port= (MCP Server Port)
  Agent_Prompt= (For Setting Model Behaviour)
  ```

5. **Run the Application**:
  ```bash
  - cd api
  - uv run server.py (Run MCP Server)
  - uv run main.py (Run FastAPI app)
  - cd frontend
  - streamlit run main.py (Run streamlit app)
  ```

6. **Access the GUI**:
  Open your browser and navigate to `http://localhost:8501` for Front-End & `http://localhost:8000/docs` to explore the Fast API documentation.

## Resources 
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [Open AI Agents SDK Documentation](https://openai.github.io/openai-agents-python)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Tavily Documentation](https://docs.tavily.com/welcome)
