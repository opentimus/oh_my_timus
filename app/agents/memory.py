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