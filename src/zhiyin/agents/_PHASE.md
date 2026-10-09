# [S5] 多 Agent 编排 —— 本目录你要写什么

**目标**：把分散的 Agent 串成"有主管、有分工、可持久化"的系统。

## 要实现的文件
- `planner.py`（S4）：输入用户需求 → 输出结构化计划（步骤列表 + 所需工具），用 JSON Schema 约束
- `supervisor.py`（S5）：用 **LangGraph** 把意图路由 → 记忆 → 检索 → 推荐 → 安全 编排成状态图

## 要掌握的 LangGraph 概念
- `State`：共享状态对象（用 TypedDict）
- `Node`：一个处理步骤（通常是一个 Agent）
- `ConditionalEdge`：条件流转（按意图选分支）
- `Checkpointer`：把图状态存库，支持中断恢复
- `interrupt()`：Human-in-the-loop，外发动作前人工确认

## 动手步骤
1. 用 Mermaid 或纸笔先画出状态图，再写代码。
2. 每个节点独立可测，最后再连起来。
3. 接 SQLite/Postgres Checkpointer，验证"中断后恢复"。
4. 给"发邀约/发帖"节点加人工确认。

## 验收标准
- [ ] 有可视化状态图
- [ ] 能跑通"故事 B：找搭子"全流程
- [ ] 进程中断后任务能恢复
- [ ] 能说出"何时不该用多 Agent"

## 常见坑
- 为多 Agent 而多 Agent（每个 Agent 都是一次额外 LLM 调用，成本翻倍）
- 状态对象设计混乱，节点互相覆盖数据
- 外发动作没人工确认
