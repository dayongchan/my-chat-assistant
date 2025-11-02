from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.session import get_current_active_user
from app.database.session import get_db
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.chat import ChatService

router = APIRouter()

@router.post("/conversations")
def create_conversation(title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """创建新对话"""
    conversation = ChatService.create_conversation(db, current_user.id, title)
    # 转换为字典
    return {
        "id": conversation.id,
        "user_id": conversation.user_id,
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
        "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None
    }

@router.get("/conversations")
def get_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """获取用户的所有对话"""
    conversations = ChatService.get_conversations(db, current_user.id)
    # 转换为字典列表
    return [
        {
            "id": conv.id,
            "user_id": conv.user_id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat() if conv.created_at else None,
            "updated_at": conv.updated_at.isoformat() if conv.updated_at else None
        }
        for conv in conversations
    ]

@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """获取对话详情"""
    conversation = ChatService.get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    
    # 获取对话的所有消息
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()
    
    # 转换为字典
    return {
        "id": conversation.id,
        "user_id": conversation.user_id,
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
        "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
        "messages": [
            {
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "token_count": msg.token_count
            }
            for msg in messages
        ]
    }

@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """删除对话"""
    success = ChatService.delete_conversation(db, conversation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="对话不存在")
    return {"message": "对话删除成功"}

class BatchDeleteRequest(BaseModel):
    conversation_ids: List[int]

@router.delete("/conversations")
def delete_conversations_batch(request: BatchDeleteRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """批量删除对话"""
    if not request.conversation_ids:
        raise HTTPException(status_code=400, detail="请提供要删除的对话ID列表")
    
    deleted_count = ChatService.delete_conversations_by_ids(db, request.conversation_ids, current_user.id)
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="未找到指定的对话")
    
    return {"message": f"成功删除 {deleted_count} 个对话"}

@router.delete("/conversations/all")
def delete_all_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """删除用户的所有对话"""
    deleted_count = ChatService.delete_all_conversations(db, current_user.id)
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="没有找到对话记录")
    
    return {"message": f"成功删除所有 {deleted_count} 个对话"}

@router.post("/conversations/batch-delete")
def batch_delete_conversations(request: BatchDeleteRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """批量删除对话（POST方式）"""
    if not request.conversation_ids:
        raise HTTPException(status_code=400, detail="请提供要删除的对话ID列表")
    
    deleted_count = ChatService.delete_conversations_by_ids(db, request.conversation_ids, current_user.id)
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="未找到指定的对话")
    
    return {"message": f"成功删除 {deleted_count} 个对话"}

from fastapi.responses import StreamingResponse
import json

class MessageRequest(BaseModel):
    content: str
    use_stream: bool = False

@router.post("/conversations/{conversation_id}/messages")
def send_message(conversation_id: int, request: MessageRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """发送消息并获取回复"""
    # 验证对话是否属于当前用户
    conversation = ChatService.get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    
    # 添加用户消息
    user_message = ChatService.add_message(db, conversation_id, "user", request.content)
    
    # 如果是流式响应
    if request.use_stream:
        return StreamingResponse(
            stream_response(db, conversation_id, request.content, user_message),
            media_type="text/plain; charset=utf-8"
        )
    
    # 非流式响应
    try:
        ai_response = ChatService.generate_answer(db, conversation_id, request.content)
        # 添加AI回复消息
        ai_message = ChatService.add_message(db, conversation_id, "assistant", ai_response)
        
        # 将SQLAlchemy对象转换为字典
        user_message_dict = {
            "id": user_message.id,
            "conversation_id": user_message.conversation_id,
            "role": user_message.role,
            "content": user_message.content,
            "created_at": user_message.created_at.isoformat() if user_message.created_at else None,
            "token_count": user_message.token_count
        }
        
        ai_message_dict = {
            "id": ai_message.id,
            "conversation_id": ai_message.conversation_id,
            "role": ai_message.role,
            "content": ai_response,
            "created_at": ai_message.created_at.isoformat() if ai_message.created_at else None,
            "token_count": ai_message.token_count
        }
        
        return {"user_message": user_message_dict, "ai_message": ai_message_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def stream_response(db: Session, conversation_id: int, content: str, user_message):
    """流式响应生成器"""
    from app.services.llm_service import LLMService
    
    # 获取对话历史
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        yield json.dumps({"error": "对话不存在"})
        return
    
    # 获取历史消息
    history_messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).limit(20).all()
    
    # 反转列表，使消息按时间顺序排列
    history_messages.reverse()
    
    # 构建消息列表
    messages = []
    for msg in history_messages:
        messages.append({"role": msg.role, "content": msg.content})
    
    # 添加最新用户消息
    if not history_messages or history_messages[-1].role != 'user' or history_messages[-1].content != content:
        messages.append({"role": "user", "content": content})
    
    # 使用LLM服务生成流式响应
    llm_service = LLMService()
    
    try:
        # 发送开始标记
        yield json.dumps({
            "type": "start",
            "user_message": {
                "id": user_message.id,
                "conversation_id": user_message.conversation_id,
                "role": user_message.role,
                "content": user_message.content,
                "created_at": user_message.created_at.isoformat() if user_message.created_at else None,
                "token_count": user_message.token_count
            }
        }) + "\n"
        
        # 流式生成响应
        full_response = ""
        for chunk in llm_service.generate_stream_response(messages):
            full_response += chunk
            yield json.dumps({
                "type": "chunk",
                "content": chunk
            }) + "\n"
        
        # 添加AI回复消息到数据库
        ai_message = ChatService.add_message(db, conversation_id, "assistant", full_response)
        
        # 发送结束标记
        yield json.dumps({
            "type": "end",
            "ai_message": {
                "id": ai_message.id,
                "conversation_id": ai_message.conversation_id,
                "role": ai_message.role,
                "content": full_response,
                "created_at": ai_message.created_at.isoformat() if ai_message.created_at else None,
                "token_count": ai_message.token_count
            }
        }) + "\n"
        
    except Exception as e:
        yield json.dumps({
            "type": "error",
            "error": str(e)
        }) + "\n"