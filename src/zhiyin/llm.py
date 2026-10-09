"""[S0] LLM 统一封装。

作用：把"怎么调大模型"这件事收敛到一个类里。后面所有 Agent / RAG / 记忆
都通过它调用模型，方便统一加日志、重试、成本统计、模型路由（S9）。

运行冒烟测试：
    uv run python -m zhiyin.llm
"""

from __future__ import annotations

from typing import Any, Iterator

from openai import OpenAI

from zhiyin.config import settings

Message = dict[str, str]


class LLM:
    """极简 LLM 客户端：对话 / 流式 / 结构化输出。"""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or settings.llm_model
        self._client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )

    # ---------- 基础对话 ----------
    def chat(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        """普通（一次性）对话，返回模型文本。"""
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore[arg-type]
            temperature=settings.llm_temperature if temperature is None else temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return resp.choices[0].message.content or ""

    # ---------- 流式对话 ----------
    def stream(self, messages: list[Message], **kwargs: Any) -> Iterator[str]:
        """流式对话，逐段 yield 文本（用于 SSE 首 token 优化）。"""
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore[arg-type]
            stream=True,
            **kwargs,
        )
        for chunk in resp:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    # ---------- 工具调用（S1 用）----------
    def chat_with_tools(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]],
        **kwargs: Any,
    ) -> Any:
        """返回原始 message 对象，便于取出 tool_calls。S1 手写 ReAct 时用。"""
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore[arg-type]
            tools=tools,  # type: ignore[arg-type]
            **kwargs,
        )
        return resp.choices[0].message

    @property
    def raw(self) -> OpenAI:
        """逃生舱：需要用到未封装的高级能力时直接拿底层 client。"""
        return self._client


if __name__ == "__main__":
    settings.ensure_llm_ready()
    llm = LLM()
    print(">> 普通对话：")
    print(llm.chat([{"role": "user", "content": "用一句话介绍你自己。"}]))
    print("\n>> 流式对话：")
    for piece in llm.stream([{"role": "user", "content": "数到 5。"}]):
        print(piece, end="", flush=True)
    print()
