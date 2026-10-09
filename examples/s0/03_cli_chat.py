"""S0 · Day5 交付物：多轮对话 CLI 助手

用法：
    uv run python examples/s0/03_cli_chat.py

这是 S0 的最终作业。补完 4 个 TODO 后，它应该满足：
    1. 多轮对话：能记住上文（比如先说"我叫小林"，再问"我叫什么"）
    2. 流式输出：回复逐字打出，而不是等一整段
    3. 命令：/clear 清空历史，/exit 退出
    4. 配置从 settings 读，代码里不出现任何硬编码的密钥/模型名

做完这个，你就具备进入 S1（手写 ReAct Agent）的全部前置能力了。
"""

from __future__ import annotations

from zhiyin.config import settings
from zhiyin.llm import LLM, Message

SYSTEM_PROMPT = "你是一个友好的社交社群 AI 助手，回答简洁、口语化。"
MAX_TURNS = 10  # 最多保留最近 10 轮对话（20 条消息），防止上下文无限增长


def trim(messages: list[Message]) -> list[Message]:
    """只保留 system 消息 + 最近 MAX_TURNS 轮对话。
    对应知识点：上下文窗口有限，历史太长要裁剪。"""
    system = [m for m in messages if m["role"] == "system"]
    rest = [m for m in messages if m["role"] != "system"]
    return system + rest[-MAX_TURNS * 2 :]


def main() -> None:
    settings.ensure_llm_ready()
    llm = LLM()

    # TODO 1: 初始化 messages，把 SYSTEM_PROMPT 作为第一条 system 消息
    messages: list[Message] = []
    raise NotImplementedError("请补完 TODO 1：初始化 messages")

    print("知音 CLI 助手已启动。输入 /clear 清空历史，/exit 退出。\n")

    while True:
        try:
            user_input = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input == "/exit":
            print("再见！")
            break
        if user_input == "/clear":
            # TODO 2: 清空历史（但保留 system 消息）
            raise NotImplementedError("请补完 TODO 2：/clear 逻辑")

        # TODO 3: 把用户输入追加进 messages（role="user"）
        raise NotImplementedError("请补完 TODO 3：追加用户消息")

        print("知音 > ", end="", flush=True)

        # TODO 4: 调用 llm.stream(trim(messages)) 流式打印，
        #         并把模型这一整轮回复拼起来、追加进 messages（role="assistant"）
        #         注意：messages 传的是裁剪后的版本，但追加要追加到完整 messages 上
        raise NotImplementedError("请补完 TODO 4：流式输出并记录回复")

        print("\n")


if __name__ == "__main__":
    main()


# ================= 提示（先别看！）=================
# TODO 1: messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#
# TODO 2: messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#         print("（历史已清空）")
#         continue
#
# TODO 3: messages.append({"role": "user", "content": user_input})
#
# TODO 4:
#   reply_parts: list[str] = []
#   for piece in llm.stream(trim(messages)):
#       print(piece, end="", flush=True)
#       reply_parts.append(piece)
#   messages.append({"role": "assistant", "content": "".join(reply_parts)})
