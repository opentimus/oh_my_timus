from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from typing import Dict, List


class InMemoryHistory(BaseChatMessageHistory):
    """In-memory implementation of chat message history."""

    def __init__(self):
        self._messages: List[BaseMessage] = []

    @property
    def messages(self) -> List[BaseMessage]:
        return self._messages

    def add_message(self, message: BaseMessage) -> None:
        self._messages.append(message)

    def clear(self) -> None:
        self._messages = []


# Global store for session histories
_session_histories: Dict[str, InMemoryHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get or create a chat history for a session."""
    if session_id not in _session_histories:
        _session_histories[session_id] = InMemoryHistory()
    return _session_histories[session_id]


def clear_session_history(session_id: str) -> None:
    """Clear the chat history for a session."""
    if session_id in _session_histories:
        _session_histories[session_id].clear()