# import streamlit as st
# import httpx
# from typing import Dict, Any
# import json


# class Chatbot:
#     def __init__(self, api_url: str):
#         self.api_url = api_url
#         self.current_tool_call = {"name": None, "args": None}
#         self.messages = st.session_state["messages"]

#     def display_message(self, message: Dict[str, Any]):
#         # display user message
#         if message["role"] == "user" and type(message["content"]) == str:
#             st.chat_message("user").markdown(message["content"])

#         # display tool result
#         if message["role"] == "user" and type(message["content"]) == list:
#             for content in message["content"]:
#                 if content["type"] == "tool_result":
#                     with st.chat_message("assistant"):
#                         st.write(f"Called tool: {self.current_tool_call['name']}:")
#                         st.json(
#                             {
#                                 "name": self.current_tool_call["name"],
#                                 "args": self.current_tool_call["args"],
#                                 "content": json.loads(content["content"][0]["text"]),
#                             },
#                             expanded=False,
#                         )

#         # display ai message
#         if message["role"] == "assistant" and type(message["content"]) == str:
#             st.chat_message("assistant").markdown(message["content"])

#         # store current ai tool use
#         if message["role"] == "assistant" and type(message["content"]) == list:
#             for content in message["content"]:
#                 # ai tool use
#                 if content["type"] == "tool_use":
#                     self.current_tool_call = {
#                         "name": content["name"],
#                         "args": content["input"],
#                     }

#     async def get_tools(self):
#         async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
#             response = await client.get(
#                 f"{self.api_url}/Web_Search/list_tools/",
#                 headers={"Content-Type": "application/json"},
#             )
#             print(response)
#             return response.json()

#     async def render(self):
#         st.title("MCP Client")

#         with st.sidebar:
#             st.subheader("Settings")
#             st.write("API URL: ", self.api_url)
#             result = await self.get_tools()
#             st.subheader("Tools")
#             st.write(tool["name"] for tool in result)

#         # Display existing messages
#         for message in self.messages:
#             self.display_message(message)

#         # Handle new query
#         query = st.chat_input("Enter your query here")
#         if query:
#             async with httpx.AsyncClient(timeout=60.0, verify=False) as client:
#                 async with client.stream(
#                 "POST",
#                 f"{self.api_url}/Web_Search/query/",
#                 json={"query": query},
#                 headers={"Content-Type": "application/json"},) as response:
#                     if response.status_code != 200:
#                         st.error(f"Backend error {response.status_code}: {await response.aread()}")
#                         return

#     # Stream the response chunks
#                     async for chunk in response.aiter_text():
#                         if chunk.strip():  # skip keep-alive empty chunks
#                             try:
#                                 event = json.loads(chunk)
#                 # Assume each event contains {"role": "...", "content": "..."}
#                                 st.session_state["messages"].append(event.delta.data)
#                                 self.display_message(event.type)
#                             except Exception:
#                                 st.write(f"{chunk}")
import streamlit as st
import httpx
import json
from typing import Dict, Any


class Chatbot:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.current_tool_call = {"name": None, "args": None}

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        self.messages = st.session_state["messages"]

    def display_message(self, message: Dict[str, Any]):
        """Render messages depending on role and type."""

        # User message
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])

        # Assistant plain text
        elif message["role"] == "assistant" and isinstance(message["content"], str):
            st.chat_message("assistant").markdown(message["content"])

        # Assistant tool result
        elif message["role"] == "assistant" and isinstance(message["content"], dict):
            with st.chat_message("assistant"):
                st.write(f"🔧 Tool result from {message['content']['name']}:")
                st.json(message["content"], expanded=False)

    async def get_tools(self):
        """Fetch available tools from backend"""
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.get(
                f"{self.api_url}/Web_Search/list_tools/",
                headers={"Content-Type": "application/json"},
            )
            return response.json()

    async def render(self):
        st.title("MCP Client")

        # Sidebar: show tools
        with st.sidebar:
            st.subheader("Settings")
            st.write("API URL: ", self.api_url)
            result = await self.get_tools()
            st.subheader("Tools")
            for tool in result:
                st.write(f"- {tool['name']}")

        # Display existing chat history
        for message in self.messages:
            self.display_message(message)

        # Handle new query input
        query = st.chat_input("Enter your query here")
        if query:
            self.messages.append({"role": "user", "content": query})
            self.display_message({"role": "user", "content": query})

            # Assistant reply (streaming)
            with st.chat_message("assistant"):
                placeholder = st.empty()
                tool_placeholder = st.empty()
                buffer = ""

                async with httpx.AsyncClient(timeout=60.0, verify=False) as client:
                    async with client.stream(
                        "POST",
                        f"{self.api_url}/Web_Search/query/",
                        json={"query": query},
                        headers={"Content-Type": "application/json"},
                    ) as response:

                        if response.status_code != 200:
                            st.error(
                                f"Backend error {response.status_code}: {await response.aread()}"
                            )
                            return

                        async for line in response.aiter_lines():
                            if line and line.startswith("data: "):
                                try:
                                    event = json.loads(line[6:])  # strip "data: "
                                    if event["type"] == "message":
                                        buffer += event["data"]
                                        placeholder.markdown(buffer)
                                    elif event["type"] == "tool_call":
                                        tool_placeholder.markdown(f"🔧 Calling tool:  {event['data']}")

                                    elif event["type"]=="done":
                                        tool_placeholder.markdown(f"✅ Agent turn finished")


                                except Exception:
                                    st.write(f"⚠️ Could not parse: {line}")

                # Save final assistant message
                self.messages.append({"role": "assistant", "content": buffer})
