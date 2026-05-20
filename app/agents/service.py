# Copyright 2024 武汉海辞科技有限公司
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from typing import Optional, AsyncIterator
import uuid

from app.core.config import get_settings
from app.agents.tools import get_default_tools
from app.agents.memory import get_session_history


def get_llm() -> BaseChatModel:
    """Initialize the LLM based on configuration."""
    settings = get_settings()

    return ChatOpenAI(
        model=settings.model_name,
        temperature=settings.temperature,
        api_key=settings.siliconflow_api_key,
        base_url=settings.siliconflow_base_url,
    )


def create_agent_prompt() -> ChatPromptTemplate:
    """Create the agent prompt template."""
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. You have access to tools to help answer questions."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])


class AgentService:
    """Service for managing agent interactions."""

    def __init__(self):
        self.llm = get_llm()
        self.tools = get_default_tools()
        self.prompt = create_agent_prompt()
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
        )

    async def run(self, query: str, session_id: Optional[str] = None) -> dict:
        """Run the agent with a query."""
        if not session_id:
            session_id = str(uuid.uuid4())

        history = get_session_history(session_id)

        result = await self.agent_executor.ainvoke({
            "input": query,
            "chat_history": history.messages,
        })

        response = result.get("output", "")

        history.add_message(HumanMessage(content=query))
        history.add_message(AIMessage(content=response))

        return {
            "response": response,
            "session_id": session_id,
            "success": True,
        }

    async def stream(self, query: str, session_id: Optional[str] = None) -> AsyncIterator[str]:
        """Stream the agent's response."""
        if not session_id:
            session_id = str(uuid.uuid4())

        history = get_session_history(session_id)
        full_response = ""

        async for event in self.agent_executor.astream_events(
            {"input": query, "chat_history": history.messages},
            version="v1",
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    full_response += content
                    yield content
            elif kind == "on_tool_start":
                tool_name = event["name"]
                yield f"\n[Using tool: {tool_name}]\n"
            elif kind == "on_tool_end":
                yield "\n"

        history.add_message(HumanMessage(content=query))
        history.add_message(AIMessage(content=full_response))


_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """Get or create the agent service singleton."""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service