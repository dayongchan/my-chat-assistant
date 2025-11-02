from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base


class UserSettings(Base):
    """用户设置模型"""
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    settings = Column(JSON, default={})
    
    # 建立与用户的关系
    user = relationship("User", backref="settings", uselist=False)