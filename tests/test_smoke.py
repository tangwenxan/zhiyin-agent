"""基础冒烟测试：不依赖真实 LLM，只验证骨架可导入、工具可注册执行。"""

from zhiyin.tools.registry import ToolRegistry, Skill


def test_registry_register_and_execute() -> None:
    reg = ToolRegistry()
    reg.register(
        Skill(
            name="echo",
            description="回显输入",
            func=lambda text: f"echo:{text}",
            parameters={
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        )
    )
    assert len(reg.openai_tools()) == 1
    assert reg.execute("echo", {"text": "hi"}) == "echo:hi"


def test_registry_unknown_tool() -> None:
    reg = ToolRegistry()
    try:
        reg.execute("nope", {})
    except KeyError:
        pass
    else:
        raise AssertionError("未知工具应当抛 KeyError")
