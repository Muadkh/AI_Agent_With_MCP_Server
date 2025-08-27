

import asyncio
import contextlib
import json
import os
from typing import Any
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
# from mcp_client import MCPClient


_: bool = load_dotenv(find_dotenv())

# URL of our standalone MCP server (from shared_mcp_server)
MCP_SERVER_URL = "http://localhost:3000/mcp/" 
os.environ["OPENAI_TRACING"] = "1"
Agent_Prompt= os.getenv("Agent_Prompt")
gemini_api_key = os.getenv("GEMINI_API_KEY")
# openai_api_key=os.getenv("OPENAI_API_KEY")
print(gemini_api_key)
#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # client=MCPClient()
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
    print(f"MCPServerStreamableHttpParams configured for URL: {mcp_params.get('url')}")
    async with MCPServerStreamableHttp(params=mcp_params, name="My_Web_Search_Server") as mcp_server_stateless:
        print(f"MCPServerStreamableHttp client '{mcp_server_stateless.name}' created and entered context.")
        app.state.mcp_server=mcp_server_stateless
        app.state.assistant = Agent(
            name="Assistant",
            instructions=Agent_Prompt,
            mcp_servers=[mcp_server_stateless],
            model=OpenAIChatCompletionsModel(
                model="gemini-2.0-flash", 
                openai_client=client,
            ),
        )

        yield
      
    
            
          
           
         




app = FastAPI(lifespan=lifespan)

origions=[

    "http://localhost:8000"
]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origions,
    allow_credentials=True,
    allow_methods=['*'],
)

class QueryRequest(BaseModel):
    query: str
class Message(BaseModel):
    role: str
    content: Any


  

@app.post("/Web_Search/query/")
async def process_query(request: QueryRequest):
    """Process a query and return the response"""
    assis=app.state.assistant
    url=app.state.mcp_server
    async def generate():
        try:
        
        
            result = Runner.run_streamed(starting_agent=assis, input=request.query)
        
            async for event in result.stream_events():
            # Stream message deltas
                if event.type == "raw_response_event" and hasattr(event.data, "delta"):
                    delta = event.data.delta
                    if delta and "query" not in delta:
                        payload = {"type": "message", "data": delta}
                        yield f"data: {json.dumps(payload)}\n\n"
                   
            # (optional) handle other event types like tool use, thinking, etc.
                elif event.type == "run_item_stream_event":
                    if event.item.type == "tool_call_item":
                        payload = {"type": "tool_call", "data": event.item.raw_item.name}
                        yield f"data: {json.dumps(payload)}\n\n"
                
            if result.is_complete:
    # Send final done signal
                yield f"data: {json.dumps({'type':'done','data': result.final_output})}\n\n"


        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return  # no return body because StreamingResponse handles it
    return StreamingResponse(generate(), media_type="text/plain-text")
@app.get("/Web_Search/list_tools/")
async def get_mcp_tools():
    'List all available tools with mcp server'
    try:
        url=app.state.mcp_server
        res= await url.list_tools()
        tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema,
                }
                for tool in res
            ]
    
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)

