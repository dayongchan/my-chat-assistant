from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """用户更新模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserInDB(UserBase):
    """数据库中的用户模型"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class User(UserInDB):
    """用户响应模型"""
    pass


class Token(BaseModel):
    """令牌模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """令牌数据模型"""
    user_id: Optional[int] = None
    username: Optional[str] = None