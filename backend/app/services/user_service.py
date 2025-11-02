from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User as UserModel
from app.models.user_settings import UserSettings as UserSettingsModel
from app.schemas.user import UserCreate, UserUpdate
from app.utils import get_password_hash, verify_password


class UserService:
    """用户服务类"""
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
        """通过邮箱获取用户"""
        return db.query(UserModel).filter(UserModel.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
        """通过用户名获取用户"""
        return db.query(UserModel).filter(UserModel.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserModel]:
        """通过ID获取用户"""
        return db.query(UserModel).filter(UserModel.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> UserModel:
        """创建用户"""
        # 检查邮箱是否已存在
        existing_user = UserService.get_user_by_email(db, user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 检查用户名是否已存在
        existing_user = UserService.get_user_by_username(db, user_create.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用"
            )
        
        # 创建新用户
        hashed_password = get_password_hash(user_create.password)
        db_user = UserModel(
            username=user_create.username,
            email=user_create.email,
            password_hash=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, email_or_username: str, password: str) -> Optional[UserModel]:
        """验证用户，支持邮箱或用户名登录"""
        # 首先尝试通过邮箱查找
        user = UserService.get_user_by_email(db, email_or_username)
        if not user:
            # 如果邮箱查找失败，尝试通过用户名查找
            user = UserService.get_user_by_username(db, email_or_username)
        
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserModel:
        """更新用户信息"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新字段
        if user_update.username:
            # 检查用户名是否已被其他用户使用
            existing_user = UserService.get_user_by_username(db, user_update.username)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已被使用"
                )
            user.username = user_update.username
        
        if user_update.email:
            # 检查邮箱是否已被其他用户使用
            existing_user = UserService.get_user_by_email(db, user_update.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被注册"
                )
            user.email = user_update.email
        
        if user_update.password:
            user.password_hash = get_password_hash(user_update.password)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_settings(db: Session, user_id: int) -> Dict[str, Any]:
        """
        获取用户设置
        如果用户没有设置记录，则返回空设置
        """
        user_settings = db.query(UserSettingsModel).filter(UserSettingsModel.user_id == user_id).first()
        if user_settings:
            return user_settings.settings
        return {}
    
    @staticmethod
    def update_user_settings(db: Session, user_id: int, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新用户设置
        如果用户没有设置记录，则创建新记录
        """
        # 验证用户是否存在
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 查找或创建用户设置记录
        user_settings = db.query(UserSettingsModel).filter(UserSettingsModel.user_id == user_id).first()
        if not user_settings:
            user_settings = UserSettingsModel(user_id=user_id, settings=settings)
            db.add(user_settings)
        else:
            user_settings.settings = settings
        
        db.commit()
        db.refresh(user_settings)
        return user_settings.settings


# 创建用户服务实例
user_service = UserService()