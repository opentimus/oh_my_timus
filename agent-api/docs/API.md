# Agent API Documentation

## Endpoints

### POST /agent/chat

Return the agent's response as a single JSON object.

**Request:**
```json
{
  "query": "What's the weather in Tokyo?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{"content": "你好！"}
```

### POST /agent/chat/sse

Stream the agent's response via Server-Sent Events.

**Request:**
```json
{
  "query": "Calculate 25 * 4 + 10",
  "session_id": "optional-session-id"
}
```

**Response (SSE stream):**
```
Content-Type: text/event-stream

data: {"content": "你"}
data: {"content": "好"}
data: {"content": "！"}
data: [DONE]
```

每行以 `data: ` 开头，内容为 JSON 字符串。流结束时发送 `data: [DONE]`。

## Session Management

- If `session_id` is omitted, a new UUID is generated
- Same `session_id` maintains conversation history
- History is stored in-memory (resets on server restart)

## Example Usage

### Python (httpx)
```python
import httpx

# JSON response
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/agent/chat",
        json={"query": "Tell me a story"}
    )
    print(response.json()["content"])

# Streaming (SSE)
async with httpx.AsyncClient() as client:
    async with client.stream(
        "POST",
        "http://localhost:8000/agent/chat/sse",
        json={"query": "Tell me a story"}
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                print(json.loads(data)["content"])
```

### JavaScript (fetch)
```javascript
// JSON response
const jsonResponse = await fetch('http://localhost:8000/agent/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Tell me a story' })
});
const jsonData = await jsonResponse.json();
console.log(jsonData.content);

// Streaming (SSE) - Note: EventSource doesn't support POST, use fetch instead
const sseResponse = await fetch('http://localhost:8000/agent/chat/sse', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Tell me a story' })
});

const sseReader = sseResponse.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await sseReader.read();
  if (done) break;

  const text = decoder.decode(value);
  const lines = text.split('\n').filter(line => line.startsWith('data: '));

  for (const line of lines) {
    const data = line.slice(6);
    if (data === '[DONE]') {
      console.log('Stream complete');
    } else {
      console.log(JSON.parse(data).content);
    }
  }
}
```

### curl
```bash
# JSON response
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me a joke"}'

# Streaming (SSE)
curl -X POST http://localhost:8000/agent/chat/sse \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me a joke"}'
```
