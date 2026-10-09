"""S0 · Day4 练习：调用大模型 + 结构化输出

用法：
    uv run python examples/s0/02_llm_structured.py

任务：补完 classify()，让模型把一句用户输入分类成意图，并解析成结构化对象。

为什么这一步重要：
    你后面 S4 的「意图识别」、S5 的「计划生成」，本质都是这件事——
    让模型输出**可被程序解析**的结构，而不是一段随便的散文。

关键点：
    1. 在 system prompt 里明确要求「只输出 JSON」，并给出字段说明。
    2. 很多模型支持 response_format={"type": "json_object"} 强制 JSON 模式。
    3. 用 Pydantic 解析，解析失败要能兜底（模型偶尔会不听话）。
"""

from __future__ import annotations

import json

from pydantic import BaseModel, Field

from zhiyin.config import settings
from zhiyin.llm import LLM


class Intent(BaseModel):
    """意图识别的结构化结果。"""

    intent: str = Field(description="意图类别，如 chitchat / knowledge_query / task / emotion")
    confidence: float = Field(description="置信度 0~1")
    reason: str = Field(description="判断依据，一句话")


SYSTEM_PROMPT = """你是一个意图识别器。把用户的话归类到以下意图之一：
- chitchat：闲聊打招呼
- knowledge_query：想了解某个知识、找攻略、问信息
- task：需要你帮他做一件有明确动作的事（找人、约时间、定提醒）
- emotion：情绪倾诉、需要安慰
只输出 JSON，格式：{"intent": "...", "confidence": 0.9, "reason": "..."}
不要输出任何解释文字或 markdown 代码块。"""


def classify(text: str) -> Intent:
    """调用模型把 text 分类，返回 Intent 对象。"""
    llm = LLM()

    # TODO 1: 组织 messages（system + user），调用 llm.chat(...)
    #         建议传入 response_format={"type": "json_object"} 强制 JSON
    # raw = llm.chat([...], response_format={"type": "json_object"})
    raise NotImplementedError("请补完 classify 的调用")

    # TODO 2: 把 raw 解析成 Intent；解析失败时返回一个默认值（confidence=0）
    # return Intent(**json.loads(raw))


def _demo() -> None:
    settings.ensure_llm_ready()
    samples = [
        "你好呀",
        "我们小区附近哪家球馆性价比高？",
        "周末想找人打羽毛球",
        "最近压力好大，感觉坚持不下去了",
    ]
    for s in samples:
        r = classify(s)
        print(f"{s}\n  -> intent={r.intent}  conf={r.confidence}  ({r.reason})\n")


if __name__ == "__main__":
    _demo()


# ================= 提示（先别看！）=================
# TODO 1 参考：
#   raw = llm.chat(
#       [{"role": "system", "content": SYSTEM_PROMPT},
#        {"role": "user", "content": text}],
#       response_format={"type": "json_object"},
#   )
#
# TODO 2 参考：
#   try:
#       data = json.loads(raw)
#       return Intent(**data)
#   except Exception as e:
#       print(f"[warn] 解析失败：{e}；原始输出={raw!r}")
#       return Intent(intent="chitchat", confidence=0.0, reason="解析失败，兜底")
