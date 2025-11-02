from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User

class UserService:
    """用户服务类"""
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str) -> User:
        """创建新用户"""
        db_user = User(
            username=username,
            email=email,
            password_hash=get_password_hash(password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """通过用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """通过邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """验证用户"""
        user = UserService.get_user_by_username(db, username)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
        """更新用户信息"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    if key == 'password':
                        setattr(user, 'password_hash', get_password_hash(value))
                    else:
                        setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user