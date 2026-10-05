# YFunctionApi

A small OpenAI-compatible mock API for integration testing. It checks a Bearer API key and always returns `Test` from the chat-completions endpoint. It does not call an AI model.

## API

`POST /v1/chat/completions`

```http
Authorization: Bearer <your-api-key>
Content-Type: application/json
```

```json
{
  "model": "test-model",
  "messages": [{"role": "user", "content": "Hello"}]
}
```

The response has the standard chat-completion shape, with `choices[0].message.content` set to `Test`. Requests with a missing or incorrect key receive HTTP 401. Requests with `"stream": true` receive an OpenAI-style server-sent event stream that ends with `finish_reason: "stop"` and `[DONE]`.

`GET /health` returns `{"status":"ok"}` for service health checks. `GET /v1/models` lists the mock model and requires the same Bearer key as the completion endpoint.

## Run locally

Requires Python 3.10 or newer.

```powershell
python -m pip install -r requirements.txt
$env:TEST_API_KEY = "sk-test-local-change-me"
uvicorn main:app --reload --port 8000
```

Call the API:

```powershell
curl.exe http://127.0.0.1:8000/v1/chat/completions `
  -H "Authorization: Bearer sk-test-local-change-me" `
  -H "Content-Type: application/json" `
  -d '{"model":"test-model","messages":[{"role":"user","content":"Hello"}]}'
```

OpenAPI documentation is available at `http://127.0.0.1:8000/docs` while the server is running.

## Run with Docker

```sh
docker build -t yfunction-api .
docker run --rm -p 8000:8000 -e TEST_API_KEY=sk-test-local-change-me yfunction-api
```

For a public deployment, run the Docker image on a server or container host and set `TEST_API_KEY` as a platform secret. GitHub Pages hosts static sites and cannot run this Python API server.

## OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-test-local-change-me",
    base_url="http://127.0.0.1:8000/v1",
)

result = client.chat.completions.create(
    model="test-model",
    messages=[{"role": "user", "content": "Hello"}],
)
print(result.choices[0].message.content)  # Test
```

Use a unique secret for any public deployment. Never commit a real API key or expose it in browser-side code.
