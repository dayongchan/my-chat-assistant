from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.user import User, UserUpdate
from app.services.user_service import user_service

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(deps.get_current_active_user)):
    """获取当前用户信息"""
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """更新当前用户信息"""
    user = await user_service.update_user(db, user_id=current_user.id, user_update=user_update)
    return user

@router.get("/settings")
async def get_user_settings(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """获取用户设置"""
    settings = user_service.get_user_settings(db, current_user.id)
    return {"user_id": current_user.id, "settings": settings}

@router.put("/settings")
async def update_user_settings(
    settings: dict,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """更新用户设置"""
    updated_settings = user_service.update_user_settings(db, current_user.id, settings)
    return {"status": "success", "message": "设置已更新", "settings": updated_settings}