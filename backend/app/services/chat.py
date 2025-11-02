from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message
from app.services.llm_service import LLMService
# # import tiktoken  # 暂时注释掉，避免安装问题  # 暂时注释掉，避免安装问题

class ChatService:
    """对话服务类"""
    
    @staticmethod
    def create_conversation(db: Session, user_id: int, title: str) -> Conversation:
        """创建新对话"""
        db_conversation = Conversation(user_id=user_id, title=title)
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        return db_conversation
    
    @staticmethod
    def get_conversations(db: Session, user_id: int) -> List[Conversation]:
        """获取用户的所有对话"""
        return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).all()
    
    @staticmethod
    def get_conversation(db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """获取对话详情"""
        return db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()
    
    @staticmethod
    def delete_conversation(db: Session, conversation_id: int, user_id: int) -> bool:
        """删除对话"""
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()
        if conversation:
            db.delete(conversation)
            db.commit()
            return True
        return False
    
    @staticmethod
    def delete_all_conversations(db: Session, user_id: int) -> int:
        """删除用户的所有对话"""
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).all()
        
        deleted_count = len(conversations)
        
        for conversation in conversations:
            db.delete(conversation)
        
        db.commit()
        return deleted_count
    
    @staticmethod
    def delete_conversations_by_ids(db: Session, conversation_ids: List[int], user_id: int) -> int:
        """批量删除指定ID的对话"""
        conversations = db.query(Conversation).filter(
            Conversation.id.in_(conversation_ids),
            Conversation.user_id == user_id
        ).all()
        
        deleted_count = len(conversations)
        
        for conversation in conversations:
            db.delete(conversation)
        
        db.commit()
        return deleted_count
    
    @staticmethod
    def add_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
        """添加消息"""
        # 暂时不计算token数量，避免tiktoken安装问题
        # encoding = tiktoken.get_encoding("cl100k_base")
        # token_count = len(encoding.encode(content))
        
        db_message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            token_count=0  # 暂时设为0
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    
    @staticmethod
    def generate_answer(db: Session, conversation_id: int, user_message: str) -> str:
        """使用LLM服务生成回答"""
        # 获取对话历史
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise ValueError("Conversation not found")
        
        # 获取历史消息（最近的一些消息作为上下文）
        # 为了避免上下文过长，只获取最近的20条消息
        history_messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(20).all()
        
        # 反转列表，使消息按时间顺序排列
        history_messages.reverse()
        
        # 构建消息列表
        messages = []
        for msg in history_messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        # 添加最新用户消息（如果尚未在历史消息中）
        # 避免重复添加用户消息
        if not history_messages or history_messages[-1].role != 'user' or history_messages[-1].content != user_message:
            messages.append({"role": "user", "content": user_message})
        
        # 使用LLM服务生成回答
        llm_service = LLMService()
        try:
            # 使用LLM服务的generate_response方法
            response_text = llm_service.generate_response(messages)
            return response_text
        except Exception as e:
            raise Exception(f"LLM服务调用失败: {str(e)}")
    
    @staticmethod
    def get_conversation_messages(db: Session, conversation_id: int, limit: int = 50) -> List[Message]:
        """
        获取对话的消息历史
        
        Args:
            db: 数据库会话
            conversation_id: 对话ID
            limit: 限制返回消息数量
            
        Returns:
            消息列表
        """
        return db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit).all()