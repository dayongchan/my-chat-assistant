from fastapi import APIRouter
from .auth import router as auth_router
from .chat import router as chat_router
from .user import router as user_router

# 创建主路由
api_router = APIRouter()

# 包含各个子路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(chat_router, prefix="", tags=["聊天"])
api_router.include_router(user_router, prefix="/user", tags=["用户"])