import os
from functools import lru_cache


class Settings:
    """数据库配置"""
    # 使用SQLite数据库替代PostgreSQL
    DATABASE_URL: str = "sqlite:///./assistant.db"


@lru_cache()
def get_settings():
    """获取设置单例"""
    return Settings()


settings = get_settings()