from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings
from app.schemas.user import TokenData


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间
    
    Returns:
        编码后的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建刷新令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间
    
    Returns:
        编码后的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> TokenData:
    """
    验证令牌
    
    Args:
        token: JWT令牌
        credentials_exception: 凭证异常
    
    Returns:
        令牌数据
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        username: str = payload.get("username")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id), username=username)
        return token_data
    except JWTError:
        raise credentials_exception


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码
    
    Returns:
        是否匹配
    """
    # 处理bcrypt密码长度限制 - 最多72字节
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password[:72]
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """
    获取密码哈希
    
    Args:
        password: 明文密码
    
    Returns:
        哈希密码
    """
    # 处理bcrypt密码长度限制 - 最多72字节
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')