from pydantic import BaseModel
from typing import Optional
from enum import Enum


class AgentRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class AgentResponse(BaseModel):
    response: str
    session_id: str
    success: bool = True
    error: Optional[str] = None


class StreamChunk(BaseModel):
    content: str
    done: bool = False