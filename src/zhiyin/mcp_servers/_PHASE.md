# [S7] 自建 MCP Server —— 本目录你要写什么

**目标**：用 **FastMCP** 把社区工具标准化暴露，实现"写一次，多宿主可用"。

## 要实现的文件
- `community_server.py`：暴露 4 个工具
  - `search_posts(keyword)`：检索帖子
  - `create_post(title, content)`：发帖（危险 → 需人工确认/沙箱）
  - `get_user_profile(user_id)`：查用户资料
  - `list_events(city)`：查活动

## 要掌握的概念
- MCP 三角色：Host / Client / Server
- 三类能力：Tools / Resources / Prompts
- 传输：stdio（本地）/ Streamable HTTP（远程）
- 用 **MCP Inspector** 调试 Server
- 鉴权：OAuth 2.1 / Token 作用域（了解）

## 动手步骤
1. `uv add "mcp[cli]" fastmcp`
2. 写 Server，`fastmcp dev community_server.py` 用 Inspector 调通。
3. 让主项目以 MCP Client 接入，工具来自协议而非硬编码。
4. 写 `docs/mcp.md`：画出"客户端调用 MCP 工具"的时序。

## 验收标准
- [ ] MCP Server 能被 Inspector 和主项目同时调用
- [ ] 替换工具无需修改 Agent 代码

## 常见坑
- 把 MCP 当"又一个 HTTP 接口"（价值在标准化）
- 工具 Schema 描述不清
- 危险工具不做鉴权与输入校验
