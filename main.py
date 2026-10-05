import os
import time
import uuid
from typing import Any

from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse


app = FastAPI(title="YFunctionApi", version="1.0.0")


def get_api_key() -> str:
    key = os.getenv("TEST_API_KEY")
    if not key:
        raise RuntimeError("Set the TEST_API_KEY environment variable before starting the API.")
    return key


def unauthorized() -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "error": {
                "message": "Invalid API key",
                "type": "authentication_error",
                "code": "invalid_api_key",
            }
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


def is_authorized(authorization: str | None) -> bool:
    return authorization == f"Bearer {get_api_key()}"


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/models")
async def list_models(
    authorization: str | None = Header(default=None),
):
    if not is_authorized(authorization):
        return unauthorized()

    return {
        "object": "list",
        "data": [
            {
                "id": "test-model",
                "object": "model",
                "created": 0,
                "owned_by": "yfunction",
            }
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(
    body: dict[str, Any],
    authorization: str | None = Header(default=None),
):
    if not is_authorized(authorization):
        return unauthorized()

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": body.get("model") or "test-model",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "Test"},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 1,
            "total_tokens": 1,
        },
    }
