"""[S1] 最小 Agent 闭环：手写 ReAct 循环。

为什么强调"手写"：只有亲手实现一遍，你才真正理解 Agent 的本质 ——
模型只负责"决策（要不要调工具、调哪个、传什么参数）"，
真正的循环控制、工具执行、结果回填，全部由你写的代码完成。

TODO（S1 任务）：把下面 3 处 TODO 补完，让 Agent 能回答：
    "明天适合打球吗？"（需要先调 get_weather）
参考运行：
    uv run python -m zhiyin.agents.base
"""

from __future__ import annotations

import json
from typing import Any

from zhiyin.config import settings
from zhiyin.llm import LLM, Message
from zhiyin.tools.registry import registry

SYSTEM_PROMPT = """你是一个社交兴趣社群的 AI 助手。
你可以调用工具来获取信息。请遵循：
1. 需要外部信息时，先调用工具，再基于结果作答。
2. 不要编造工具返回结果之外的事实。
3. 用简洁、友好的中文回答。
"""

MAX_STEPS = 6  # 防止死循环 + 控制成本


def run_agent(user_input: str, *, verbose: bool = True) -> str:
    llm = LLM()
    messages: list[Message] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]
    tools = registry.openai_tools()

    for step in range(1, MAX_STEPS + 1):
        if verbose:
            print(f"\n--- step {step} ---")

        # TODO 1: 调用 llm.chat_with_tools(messages, tools)，拿到返回的 message
        # msg = llm.chat_with_tools(messages, tools)
        msg = llm.chat_with_tools(messages, tools)

        # 情况一：模型不再调用工具，直接给出最终答案 -> 结束循环
        if not getattr(msg, "tool_calls", None):
            return msg.content or ""

        # 模型要求调用工具：把模型的这条消息加入历史
        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
            }  # type: ignore[list-item]
        )

        # 情况二：逐个执行工具，把结果作为 tool 消息回填
        for tc in msg.tool_calls:
            name = tc.function.name
            try:
                args: dict[str, Any] = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}

            if verbose:
                print(f"[调用工具] {name}({args})")

            # TODO 2: 执行工具，拿到结果 result
            # result = registry.execute(name, args)
            result = registry.execute(name, args)

            if verbose:
                print(f"[工具结果] {result}")

            # TODO 3: 把工具结果作为 role="tool" 的消息追加进 messages
            # messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
            messages.append(
                {"role": "tool", "tool_call_id": tc.id, "content": str(result)}
            )

    return "（达到最大步数仍未完成，请简化你的问题。）"


# ---------- 演示用工具 ----------
from zhiyin.tools.registry import tool  # noqa: E402


@tool(
    name="get_weather",
    description="查询某城市明天的天气。当用户询问天气、是否适合户外活动时使用。",
    parameters={
        "type": "object",
        "properties": {"city": {"type": "string", "description": "城市名，如 北京"}},
        "required": ["city"],
    },
)
def get_weather(city: str) -> str:
    # 现在返回假数据；S2 之后可替换为真实 API
    return f"{city}明天：多云转晴，气温 18-26℃，风力 2 级，适合户外运动。"


if __name__ == "__main__":
    settings.ensure_llm_ready()
    print(run_agent("明天适合打球吗？我在北京。"))
