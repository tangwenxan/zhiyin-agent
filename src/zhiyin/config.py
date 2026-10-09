"""[S0] 配置与密钥管理。

原则：所有配置都走环境变量（.env），代码里绝不硬编码任何密钥。
后面每个阶段新增的配置（向量库、Langfuse 等）都往这里加。
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---- LLM ----
    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com/v1"
    llm_model: str = "deepseek-chat"
    llm_temperature: float = 0.3
    llm_small_model: str = ""  # [S9] 模型路由用的小模型

    # ---- 存储 ----
    database_url: str = "sqlite:///./zhiyin.db"
    vector_store: str = "chroma"  # [S2] chroma | qdrant
    chroma_path: str = "./data/chroma"

    # ---- 可观测 ----
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"

    def ensure_llm_ready(self) -> None:
        """冒烟检查：没配 Key 就直接给出清晰报错，而不是等到调用时才崩。"""
        if not self.llm_api_key:
            raise RuntimeError(
                "缺少 LLM_API_KEY。请复制 .env.example 为 .env 并填入你的 API Key。"
            )


# 全局单例：其他模块 `from zhiyin.config import settings` 直接用
settings = Settings()


if __name__ == "__main__":
    print("配置加载成功：")
    print(f"  base_url = {settings.llm_base_url}")
    print(f"  model    = {settings.llm_model}")
    print(f"  api_key  = {'已配置' if settings.llm_api_key else '未配置（请填 .env）'}")
