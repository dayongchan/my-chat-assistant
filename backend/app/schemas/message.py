from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class MessageRole(str, Enum):
    """消息角色枚举"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageBase(BaseModel):
    """消息基础模型"""
    content: str = Field(..., min_length=1)


class MessageCreate(MessageBase):
    """消息创建模型"""
    role: MessageRole


class MessageInDB(MessageBase):
    """数据库中的消息模型"""
    id: int
    conversation_id: int
    role: MessageRole
    created_at: datetime
    
    class Config:
        from_attributes = True


class Message(MessageInDB):
    """消息响应模型"""
    pass


class ChatRequest(BaseModel):
    """聊天请求模型"""
    conversation_id: Optional[int] = None
    content: str = Field(..., min_length=1)
    use_stream: bool = False