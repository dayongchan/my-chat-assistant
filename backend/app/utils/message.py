from typing import List, Dict, Any
from app.schemas.message import MessageRole


def format_messages_for_llm(messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    格式化消息列表为LLM所需的格式
    
    Args:
        messages: 消息列表
    
    Returns:
        格式化后的消息列表
    """
    return [
        {"role": msg["role"].value if isinstance(msg["role"], MessageRole) else msg["role"], "content": msg["content"]}
        for msg in messages
    ]


def generate_system_prompt() -> str:
    """
    生成系统提示词
    
    Returns:
        系统提示词
    """
    return (
        "你是一个强大的AI助手，类似于DeepSeek。请根据用户的问题提供准确、有用的回答。\n"
        "保持友好、专业的语气，尽可能提供详细的解释和示例。\n"
        "如果遇到不确定的问题，请坦诚表示并建议用户提供更多信息。"
    )


def extract_conversation_title(user_input: str) -> str:
    """
    从用户输入中提取对话标题
    
    Args:
        user_input: 用户输入
    
    Returns:
        对话标题
    """
    # 简单实现：取前50个字符作为标题
    title = user_input.strip()[:50]
    if len(user_input.strip()) > 50:
        title += "..."
    return title