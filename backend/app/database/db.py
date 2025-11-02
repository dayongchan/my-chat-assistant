from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 创建数据库引擎 - 适配SQLite
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite需要这个参数来支持多线程
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖项：获取数据库会话
def get_db():
    """获取数据库会话的依赖项"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()