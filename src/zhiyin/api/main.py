"""[S0 起] FastAPI 网关：对外提供流式对话接口。

启动：
    uv run uvicorn zhiyin.api.main:app --reload
接口文档：
    http://127.0.0.1:8000/docs
测试：
    curl -N http://127.0.0.1:8000/chat -X POST \
         -H "Content-Type: application/json" \
         -d '{"message":"你好"}'
"""

from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from zhiyin.llm import LLM

app = FastAPI(title="知音 ZhiYin API", version="0.1.0")


class ChatRequest(BaseModel):
    message: str
    user_id: str = "demo_user"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest) -> StreamingResponse:
    """SSE 流式对话。后续阶段会在这里接：意图路由 -> 记忆 -> RAG -> Agent。"""
    llm = LLM()

    def event_stream():
        messages = [{"role": "user", "content": req.message}]
        for piece in llm.stream(messages):
            yield f"data: {json.dumps({'delta': piece}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
