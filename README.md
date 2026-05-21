# Core Highlights

## "Claude Code" Voice-to-Agent Experience

No more dragging and dropping nodes or writing complex YAML. Just speak your requirements in natural language as if you were talking to Claude (e.g., "I want an agent that can check the weather, calculate shipping costs, and send emails"), and the system instantly generates a working agent.

## Native LangChain Integration

Deeply customized based on LangChain, inheriting its rich toolchain and memory management capabilities, while providing a lighter-weight and more open agent orchestration approach than Dify.

# Core Features

- **More Flexible** – No restrictions on workflow structure; supports arbitrarily complex loops and conditional jumps.

- **More Conversational** – All agents can be debugged and iterated in real time within the chat, without switching back to the backend editor.

- **More Open-Source Friendly** – Fully compatible with the LangChain ecosystem, making self-hosting and secondary development easy.
# Agent API

FastAPI application integrated with LangChain for building AI agents.

## Project Structure

```
├── app/
│   ├── api/           # API routes
│   ├── agents/        # LangChain agent logic
│   ├── core/          # Configuration
│   ├── schemas/       # Pydantic models
│   └── main.py        # FastAPI app
├── docs/
├── tests/
├── pyproject.toml
└── .env.example
```

## Setup

### Local Development

1. Install dependencies:
```bash
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

### Docker Deployment

1. Build and run with Docker Compose:
```bash
# Set your API key
export SILICONFLOW_API_KEY=your-api-key

# Build and run
docker-compose up -d
```

2. Or build manually:
```bash
docker build -t agent-api .
docker run -p 8000:8000 -e SILICONFLOW_API_KEY=your-api-key agent-api
```

## API Endpoints

- `GET /health` - Health check
- `POST /agent/chat` - Send message to agent, returns JSON response
- `POST /agent/chat/sse` - Stream agent response via SSE

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

## License

[Apache License 2.0](LICENSE)
