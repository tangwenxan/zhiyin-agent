"""[S1][S7] 工具与 Skill 抽象。

一个"Skill"= 声明式的工具：名称 + 描述 + 参数 Schema + 处理器 + 权限。
S1 先用它让 Agent 能调工具；S7 再把它升级成可动态注册/加载的 Skill 体系。

关键点：工具的 description 写得越清楚，模型选错工具的概率越低。
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Skill:
    name: str
    description: str
    func: Callable[..., Any]
    parameters: dict[str, Any] = field(default_factory=dict)
    # [S6] 标记为 True 的工具必须走沙箱 / 需要人工确认
    dangerous: bool = False

    def to_openai_tool(self) -> dict[str, Any]:
        """转成大模型 Function Calling 需要的 JSON Schema 格式。"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
                or {"type": "object", "properties": {}, "required": []},
            },
        }

    def run(self, **kwargs: Any) -> Any:
        return self.func(**kwargs)


class ToolRegistry:
    """工具注册表：注册、查找、批量导出 schema、统一执行。"""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        if skill.name in self._skills:
            raise ValueError(f"工具已存在：{skill.name}")
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def all(self) -> list[Skill]:
        return list(self._skills.values())

    def openai_tools(self) -> list[dict[str, Any]]:
        """给 S1 的 ReAct 循环用：一次性拿到所有工具定义。"""
        return [s.to_openai_tool() for s in self._skills.values()]

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        """执行工具。S6 可在这里接沙箱与权限校验。"""
        skill = self.get(name)
        if skill is None:
            raise KeyError(f"未知工具：{name}")
        return skill.run(**arguments)


# ---------- 全局注册表（后续各阶段往这里注册工具）----------
registry = ToolRegistry()


def tool(
    name: str | None = None,
    description: str = "",
    parameters: dict[str, Any] | None = None,
    dangerous: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """装饰器写法：@tool(description="...")，自动注册。"""

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        skill = Skill(
            name=name or fn.__name__,
            description=description or (inspect.getdoc(fn) or ""),
            func=fn,
            parameters=parameters or {"type": "object", "properties": {}, "required": []},
            dangerous=dangerous,
        )
        registry.register(skill)
        return fn

    return deco


if __name__ == "__main__":
    @tool(
        name="search_community",
        description="按关键词检索社区帖子。当用户想找攻略、找搭子、找活动时使用。",
        parameters={
            "type": "object",
            "properties": {"keyword": {"type": "string", "description": "检索关键词"}},
            "required": ["keyword"],
        },
    )
    def search_community(keyword: str) -> str:
        return f"[假数据] 关于「{keyword}」的帖子有 3 条。"

    print(registry.openai_tools())
    print(registry.execute("search_community", {"keyword": "羽毛球"}))
