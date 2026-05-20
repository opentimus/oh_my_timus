# Agent API

FastAPI application integrated with LangChain for building AI agents.

## Project Structure

```
agent-api/
├── app/
│   ├── api/           # API routes
│   ├── agents/        # LangChain agent logic
│   ├── core/          # Configuration
│   ├── schemas/       # Pydantic models
│   └── main.py        # FastAPI app
├── tests/
├── pyproject.toml
└── .env.example
```

## Setup

1. Install dependencies:
```bash
cd agent-api
pip install -e .
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /health` - Health check
- `POST /agent/chat` - Send message to agent
- `POST /agent/chat/stream` - Stream agent response

## Usage Example

```python
import httpx

async def chat():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/agent/chat",
            json={"query": "What's the weather in Tokyo?"}
        )
        print(response.json())
```

## Tools

The agent comes with built-in tools:
- `get_current_weather` - Get weather for a location
- `search_web` - Search the web
- `calculate` - Evaluate math expressions
