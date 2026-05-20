from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import AgentRequest
from app.agents import get_agent_service
import json

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/chat")
async def chat(request: AgentRequest):
    """Return the agent's response as a single JSON object."""
    try:
        agent = get_agent_service()
        result = await agent.run(request.query, request.session_id)
        return {"content": result["response"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/sse")
async def chat_sse(request: AgentRequest):
    """Stream the agent's response via Server-Sent Events."""

    async def generate():
        agent = get_agent_service()
        try:
            async for chunk in agent.stream(request.query, request.session_id):
                yield f"data: {json.dumps({'content': chunk})}\n"
            yield "data: [DONE]\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )