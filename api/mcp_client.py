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
