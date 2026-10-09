# [S3] 长期记忆系统 —— 本目录你要写什么

**目标**：让 Agent 跨会话记住用户，并且会更新、会遗忘、会按用户隔离。

## 要实现的文件
| 文件 | 内容 |
|---|---|
| `extractor.py` | 从对话中抽取结构化事实（LLM 抽取，输出 JSON） |
| `store.py` | 写入 + 去重 + **冲突消解**（新事实与旧事实矛盾时更新） + 时间衰减 |
| `retriever.py` | 按 user_id 检索相关记忆，拼进 system prompt |

## 记忆数据结构（建议）
```python
Memory(
    user_id: str, type: str,          # episodic | semantic | preference
    content: str, embedding: list[float],
    importance: float,                # 0~1
    created_at: datetime, last_used_at: datetime,
    valid_until: datetime | None,     # 时效性
)
```

## 动手步骤
1. 对话结束后异步抽取事实。
2. 写入时做语义去重 + 冲突消解（相似度 + LLM 判断是否矛盾）。
3. 每轮对话前检索相关记忆注入 prompt。
4. 跑通验收故事 A：隔天新会话主动问起"考研/跑步"。

## 验收标准
- [ ] 跨会话能正确回忆用户事实
- [ ] 用户偏好变化时记忆能更新而非堆积矛盾
- [ ] 多用户测试数据不串
- [ ] （可选）横向对比 Mem0/Zep，写成笔记

## 常见坑
- 把整段对话当记忆（那是缓存，不是记忆）
- 不做去重，记忆爆炸且互相矛盾
- 忘记 user_id 隔离
- 检索不筛相关度，全塞进 prompt 反而干扰模型
