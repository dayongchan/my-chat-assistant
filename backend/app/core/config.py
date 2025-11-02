import os
from functools import lru_cache
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


class Settings:
    """应用配置"""
    # 应用基本信息
    APP_NAME: str = os.getenv("APP_NAME", "My Chat Assistant")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./assistant.db")
    
    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "default-api-key-change-in-production")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    DEEPSEEK_API_BASE: str = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    
    # CORS配置
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]


@lru_cache()
def get_settings():
    """获取设置单例"""
    return Settings()


settings = get_settings()