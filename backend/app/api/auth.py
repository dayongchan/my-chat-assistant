from datetime import timedelta
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import create_access_token
from app.database.session import get_db
from app.services.user_service import user_service

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录获取访问令牌"""
    logger.info(f"登录尝试: username={form_data.username}")
    
    try:
        # 尝试通过邮箱或用户名验证用户
        user = user_service.authenticate_user(db, form_data.username, form_data.password)
        
        if not user:
            logger.warning(f"登录失败: 用户不存在或密码错误, username={form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            logger.warning(f"登录失败: 用户账户已被禁用, username={form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户账户已被禁用"
            )
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        
        logger.info(f"登录成功: user_id={user.id}, username={user.username}, email={user.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"登录过程发生异常: username={form_data.username}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程中发生错误"
        )

# 注册请求模型
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@router.post("/register")
def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册"""
    logger.info(f"注册尝试: username={register_data.username}, email={register_data.email}")
    
    try:
        # 检查用户名是否已存在
        if user_service.get_user_by_username(db, register_data.username):
            logger.warning(f"注册失败: 用户名已存在, username={register_data.username}")
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        if user_service.get_user_by_email(db, register_data.email):
            logger.warning(f"注册失败: 邮箱已被注册, email={register_data.email}")
            raise HTTPException(status_code=400, detail="邮箱已被注册")
        
        # 创建新用户
        from app.schemas.user import UserCreate
        user_create = UserCreate(username=register_data.username, email=register_data.email, password=register_data.password)
        
        logger.info(f"开始创建用户: username={register_data.username}, email={register_data.email}")
        user = user_service.create_user(db, user_create)
        
        logger.info(f"注册成功: user_id={user.id}, username={user.username}, email={user.email}")
        return {"id": user.id, "username": user.username, "email": user.email}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"注册过程发生异常: username={register_data.username}, email={register_data.email}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册过程中发生错误"
        )