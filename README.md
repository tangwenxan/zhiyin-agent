# 知音 ZhiYin · 社交产品 AI Agent 核心系统

> 一份为「社交产品 AI Agent 工程师」岗位量身打造的实战项目脚手架。
> 配套文档见上级目录：`知音ZhiYin-AI-Agent求职项目实战手册.html`

本仓库是按 **S0 → S10 十个阶段** 逐层搭建的骨架。每个模块目录下都有一份 `_PHASE.md`，
告诉你**这个目录属于哪个阶段、要写什么、验收标准是什么**。请按阶段顺序推进，不要跳。

---

## 项目定位（一句话）

以「社交兴趣社群 App 里的 AI 伙伴」为主线，把 **任务规划 / 长期记忆 / 意图识别 / 多 Agent 协同 /
RAG / Durable Execution / 沙箱 / Skills 与 MCP / 评测飞轮 / 推理优化** 串成一条可跑通、可演示、
可写进简历的技术链路。

## 四个验收故事（最终 Demo 目标）

| 故事 | 场景 | 考察能力 |
|---|---|---|
| A 个性化陪伴 | 隔天新会话仍记得"在准备考研、喜欢跑步" | 长期记忆 |
| B 多步任务 | "周末想找人打羽毛球" → 匹配球友 + 生成邀约 | 规划 + 多 Agent + 沙箱 |
| C 知识问答 | "附近哪家球馆性价比高" → 带引用作答 | RAG |
| D 长任务 | "3 天后提醒我交论文并发最新资料" | Durable Execution |

---

## 快速开始

```bash
# 1. 安装依赖（推荐 uv；没有 uv 就用 pip install -e .）
uv sync

# 2. 配置密钥
cp .env.example .env
#  编辑 .env，填入你的 LLM API Key

# 3. 冒烟测试：调用一次大模型
uv run python -m zhiyin.llm

# 4. 启动 API 服务
uv run uvicorn zhiyin.api.main:app --reload
#  浏览器打开 http://127.0.0.1:8000/docs
```

---

## 目录结构与阶段对应

```
zhiyin-agent/
├── src/zhiyin/
│   ├── config.py          # [S0] 配置与密钥管理（Pydantic Settings）
│   ├── llm.py             # [S0] LLM 统一封装（对话 / 结构化输出 / 流式）
│   ├── agents/            # [S1][S4][S5] 最小 Agent 循环 + Planner + Supervisor
│   │   ├── base.py        #        手写 ReAct 循环（S1 核心）
│   │   ├── planner.py     #        任务规划（S4）
│   │   └── supervisor.py  #        多 Agent 编排（S5）
│   ├── intent/            # [S4] 意图识别与路由
│   │   └── router.py
│   ├── rag/               # [S2] 检索增强
│   │   ├── ingest.py      #        加载 → 切分 → 向量化 → 入库
│   │   ├── chunking.py    #        切分策略（含父子块）
│   │   ├── retrieve.py    #        混合检索 + RRF
│   │   └── rerank.py      #        重排（BGE / Cohere）
│   ├── memory/            # [S3] 长期记忆
│   │   ├── extractor.py   #        事实抽取
│   │   ├── store.py       #        写入 / 去重 / 冲突消解
│   │   └── retriever.py   #        记忆检索与注入
│   ├── tools/             # [S1][S7] 工具与 Skill 抽象
│   │   └── registry.py    #        工具注册表（声明式 Skill）
│   ├── mcp_servers/       # [S7] 自建 MCP Server（FastMCP）
│   │   └── community_server.py
│   ├── runtime/           # [S6] 基础设施
│   │   ├── durable.py     #        持久化执行（checkpoint / 幂等 / 定时）
│   │   └── sandbox.py     #        沙箱执行（超时 / 资源 / 白名单）
│   ├── eval/              # [S8] 评测飞轮
│   │   ├── datasets/      #        测试集（含标注）
│   │   ├── metrics.py     #        RAGAS / DeepEval 封装
│   │   └── run_eval.py    #        一键评测
│   ├── obs/               # [S8] 可观测
│   │   └── tracing.py     #        Langfuse 接入
│   └── api/
│       └── main.py        # [S0起] FastAPI 网关（SSE 流式）
├── tests/                 # 单元测试（贯穿全程）
├── data/                  # 样例数据（社区帖子等）
└── docs/                  # 你的阶段笔记（S1-notes.md 等）
```

## 研发纪律（很重要）

1. **每天 commit**，commit message 写清楚做了什么。
2. **每完成一个阶段，在 `docs/` 下写一篇 `<阶段>-notes.md`**：做了什么 / 卡在哪 / 怎么解决 / 指标变化。
   8 周后这些笔记就是你面试的弹药。
3. **先跑通再加优化**，任何优化都要有优化前的基线数字。
4. **核心模块（Agent 循环 / 记忆 / 检索）必须能手写、能白板画出来**，不要全靠 AI 生成。
