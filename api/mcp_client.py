from typing import Optional
from contextlib import AsyncExitStack
import traceback
from mcp.client.streamable_http import streamablehttp_client
from utils.logger import logger
from mcp import ClientSession, types

class MCPClient:
    def __init__(self):
        self.tools = []
        self.messages = []

    # async def connect_to_server(self, mcp_server_url: str):
    #     self._server_url = mcp_server_url
    #     try:
    #         streamable_transport = await self._exit_stack.enter_async_context(
    #             streamablehttp_client(self._server_url)
    #         )
    #         read, write, _ = streamable_transport

    #         self._session = await self._exit_stack.enter_async_context(
    #             ClientSession(read, write)
    #         )

    #         await self._session.initialize()
    #         self.logger.info("Connected to MCP server")

    #         mcp_tools = await self.get_mcp_tools()
    #         self.tools = [
    #             {
    #                 "name": tool.name,
    #                 "description": tool.description,
    #                 "input_schema": tool.inputSchema,
    #             }
    #             for tool in mcp_tools
    #         ]
    #         self.logger.info(f"Available tools: {[tool['name'] for tool in self.tools]}")
    #         return True

    #     except Exception as e:
    #         self.logger.error(f"Error connecting to MCP server: {e}")
    #         traceback.print_exc()
    #         raise

    # async def get_mcp_tools(self):
    #     try:
    #         response = await self._session.list_tools()
    #         return response.tools
    #     except Exception as e:
    #         self.logger.error(f"Error getting MCP tools: {e}")
    #         traceback.print_exc()
    #         raise

    # async def cleanup(self):
    #     try:
    #         await self._exit_stack.aclose()
    #         self.logger.info("Disconnected from MCP server")
    #     except* Exception as eg:
    #         self.logger.error("Errors occurred during cleanup:")
    #         for e in eg.exceptions:
    #             self.logger.error(f" - {type(e).__name__}: {e}")
    #         raise
       
