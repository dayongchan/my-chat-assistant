from typing import List, Dict, Any, Generator
import requests
import json
from app.core.config import settings
from app.utils import format_messages_for_llm, generate_system_prompt


class LLMService:
    """LLM服务类 - 按照Deepseek官网标准调用API"""
    
    def __init__(self):
        """初始化服务"""
        print(f"正在使用API密钥: {settings.DEEPSEEK_API_KEY[:8]}...")
        print(f"正在使用API基础URL: {settings.DEEPSEEK_API_BASE}")
        print(f"正在使用模型: {settings.DEEPSEEK_MODEL}")
        
        # Deepseek API配置
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_base = settings.DEEPSEEK_API_BASE
        self.model = settings.DEEPSEEK_MODEL
        self.chat_endpoint = f"{self.api_base}/chat/completions"
        print("按照Deepseek官网标准调用API")
    
    def generate_response(self, messages: List[Dict[str, Any]]) -> str:
        """
        生成非流式响应 - 按照Deepseek官网标准调用API
        
        Args:
            messages: 消息列表，包含历史对话
        
        Returns:
            AI生成的回复
        """

        # 格式化消息，添加系统提示词
        formatted_messages = [
            {"role": "system", "content": generate_system_prompt()}
        ]
        formatted_messages.extend(format_messages_for_llm(messages))
        
        print(f"准备调用Deepseek API，模型: {self.model}")
        print(f"消息数量: {len(formatted_messages)}")
        
        try:
            # 按照Deepseek官网标准构建请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Deepseek标准请求参数
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "max_tokens": 2048,  # 增加token限制
                "temperature": 0.7,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "stream": False
            }
            
            # 发送请求
            print(f"发送请求到: {self.chat_endpoint}")
            response = requests.post(
                self.chat_endpoint,
                headers=headers,
                json=payload,
                timeout=60  # 增加超时时间
            )
            
            # 检查响应状态
            if response.status_code == 200:
                # 解析响应
                data = response.json()
                print(f"接收到API响应，状态: {data.get('object', 'unknown')}")
                
                # 按照Deepseek标准格式解析响应
                if data.get('choices') and len(data['choices']) > 0:
                    choice = data['choices'][0]
                    if choice.get('message') and choice['message'].get('content'):
                        content = choice['message']['content'].strip()
                        print(f"获取到Deepseek API回复，长度: {len(content)}字符")
                        
                        # 打印token使用情况
                        if data.get('usage'):
                            usage = data['usage']
                            print(f"Token使用情况 - 输入: {usage.get('prompt_tokens', 0)}, 输出: {usage.get('completion_tokens', 0)}, 总计: {usage.get('total_tokens', 0)}")
                        
                        return content
                    else:
                        return "抱歉，API返回了空的结果。"
                else:
                    return "抱歉，API没有返回有效的结果。"
            else:
                error_msg = f"API返回错误状态码: {response.status_code}"
                try:
                    error_data = response.json()
                    if error_data.get('error'):
                        error_msg += f", 错误信息: {error_data['error'].get('message', '未知错误')}"
                except:
                    error_msg += f", 响应内容: {response.text[:200]}"
                
                print(error_msg)
                return f"⚠️ API请求失败: {error_msg}"
                
        except requests.exceptions.Timeout:
            error_info = "⚠️ API请求超时，请检查网络连接或稍后重试"
            print(error_info)
            return error_info
        except requests.exceptions.ConnectionError:
            error_info = "⚠️ 网络连接错误，请检查网络连接"
            print(error_info)
            return error_info
        except Exception as e:
            error_info = f"⚠️ 调用Deepseek API时出错: {type(e).__name__}: {str(e)}"
            print(error_info)
            return error_info
    
    def generate_stream_response(self, messages: List[Dict[str, Any]]) -> Generator[str, None, None]:
        """
        生成流式响应 - 按照Deepseek官网标准实现流式调用
        
        Args:
            messages: 消息列表，包含历史对话
        
        Yields:
            AI生成的回复片段
        """
        # 格式化消息，添加系统提示词
        formatted_messages = [
            {"role": "system", "content": generate_system_prompt()}
        ]
        formatted_messages.extend(format_messages_for_llm(messages))
        
        print(f"准备调用Deepseek API(流式)，模型: {self.model}")
        
        try:
            # 按照Deepseek官网标准构建流式请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Deepseek标准流式请求参数
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "max_tokens": 2048,
                "temperature": 0.7,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "stream": True
            }
            
            # 发送流式请求
            print(f"发送流式请求到: {self.chat_endpoint}")
            response = requests.post(
                self.chat_endpoint,
                headers=headers,
                json=payload,
                stream=True,
                timeout=90  # 流式请求需要更长的超时时间
            )
            
            # 检查响应状态
            if response.status_code == 200:
                print("开始接收流式响应...")
                
                # 逐行处理Server-Sent Events (SSE)格式的响应
                for line in response.iter_lines():
                    if line:
                        # 解码并处理SSE格式
                        line = line.decode('utf-8').strip()
                        
                        # 跳过空行和事件类型行
                        if not line or line.startswith('event:'):
                            continue
                        
                        # 处理数据行
                        if line.startswith('data: '):
                            data_str = line[6:]
                            
                            # 检查流式结束标记
                            if data_str == '[DONE]':
                                print("流式响应结束")
                                break
                            
                            try:
                                # 解析JSON数据
                                data = json.loads(data_str)
                                
                                # 按照Deepseek标准格式解析流式数据
                                if data.get('choices') and len(data['choices']) > 0:
                                    choice = data['choices'][0]
                                    delta = choice.get('delta', {})
                                    
                                    # 提取内容片段
                                    if delta.get('content'):
                                        content = delta['content']
                                        yield content
                                        
                                    # 检查是否结束
                                    if choice.get('finish_reason'):
                                        print(f"流式响应完成，原因: {choice['finish_reason']}")
                                        break
                                        
                            except json.JSONDecodeError as e:
                                print(f"解析JSON失败: {data_str[:100]}..., 错误: {str(e)}")
                            except Exception as e:
                                print(f"处理数据块失败: {str(e)}")
                                
            else:
                error_msg = f"API返回错误状态码: {response.status_code}"
                try:
                    error_data = response.json()
                    if error_data.get('error'):
                        error_msg += f", 错误信息: {error_data['error'].get('message', '未知错误')}"
                except:
                    error_msg += f", 响应内容: {response.text[:200]}"
                
                print(error_msg)
                yield f"⚠️ 流式API请求失败: {error_msg}"
                
        except requests.exceptions.Timeout:
            error_info = "⚠️ 流式API请求超时，请检查网络连接或稍后重试"
            print(error_info)
            yield error_info
        except requests.exceptions.ConnectionError:
            error_info = "⚠️ 网络连接错误，请检查网络连接"
            print(error_info)
            yield error_info
        except Exception as e:
            error_info = f"⚠️ 流式调用Deepseek API时出错: {type(e).__name__}: {str(e)}"
            print(error_info)
            yield error_info


# 创建LLM服务实例
llm_service = LLMService()