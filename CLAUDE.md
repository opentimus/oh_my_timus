# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI application integrated with LangChain for building AI agents. The project is located in the `agent-api/` subdirectory.

## Commands

```bash
# Install dependencies
cd agent-api && pip install -e .

# Install dev dependencies (for testing/linting)
pip install -e ".[dev]"

# Run the server
uvicorn app.main:app --reload

# Run tests
pytest

# Run single test file
pytest tests/test_api.py

# Run single test
pytest tests/test_api.py::test_health_check

# Lint
ruff check .
```

## Architecture

The application follows a layered architecture:

- **API Layer** (`app/api/`): FastAPI routers that handle HTTP requests. Routes inject the AgentService and delegate to it.

- **Agent Service** (`app/agents/service.py`): Core LangChain agent implementation. Uses `create_tool_calling_agent` with an `AgentExecutor`. The service is a singleton obtained via `get_agent_service()`. Supports both `run()` (returns full response) and `stream()` (async iterator for SSE).

- **Tools** (`app/agents/tools.py`): LangChain tools defined with `@tool` decorator. Currently includes mock implementations for weather, web search, and calculator.

- **Memory** (`app/agents/memory.py`): In-memory session history using LangChain's `BaseChatMessageHistory`. Session histories are stored in a global dict keyed by `session_id`.

- **Configuration** (`app/core/config.py`): Pydantic-settings based config loaded from `.env`. Key settings: `llm_provider` (anthropic/openai), `model_name`, API keys.

- **Schemas** (`app/schemas/`): Pydantic models for request/response validation.

## Key Patterns

- LLM selection is controlled by `LLM_PROVIDER` env var (anthropic or openai)
- Agent uses tool-calling paradigm with chat history preserved per session
- Streaming uses LangChain's `astream_events` API with SSE output
- All routes are mounted under `/agent` prefix