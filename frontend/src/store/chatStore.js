import { defineStore } from 'pinia';
import { api } from '../services/api';
import axios from 'axios';

export const useChatStore = defineStore('chat', {
  state: () => ({
    conversations: [],
    currentConversation: null,
    messages: [],
    isLoading: false,
    isSending: false,
    error: null
  }),
  
  actions: {
    // 获取所有对话
    async fetchConversations() {
      this.isLoading = true;
      this.error = null;
      
      try {
        // 注意：api响应拦截器直接返回response.data，所以不需要再访问response.data
        const conversationsData = await api.get('/api/conversations');
        this.conversations = conversationsData;
        return conversationsData;
      } catch (error) {
        this.error = error.response?.data?.detail || '获取对话列表失败';
        console.error('获取对话列表失败:', error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 创建新对话
    async createConversation(title = '新对话') {
      this.isLoading = true;
      this.error = null;
      
      try {
        // 注意：后端API期望title作为查询参数，而不是请求体的一部分
        // 注意：api响应拦截器直接返回response.data，所以不需要再访问response.data
        const newConversation = await api.post('/api/conversations', null, {
          params: { title }
        });
        this.conversations.unshift(newConversation);
        this.setCurrentConversation(newConversation.id);
        return newConversation;
      } catch (error) {
        this.error = error.response?.data?.detail || '创建对话失败';
        console.error('创建对话失败:', error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 设置当前对话
    async setCurrentConversation(conversationId) {
      this.isLoading = true;
      this.error = null;
      
      try {
        console.log('开始获取对话详情，对话ID:', conversationId);
        // 注意：api响应拦截器直接返回response.data，所以不需要再访问response.data
        const conversationData = await api.get(`/api/conversations/${conversationId}`);
        console.log('获取对话详情成功:', conversationData);
        console.log('对话消息数量:', conversationData.messages ? conversationData.messages.length : 0);
        
        this.currentConversation = conversationData;
        this.messages = conversationData.messages || [];
        
        console.log('设置后的消息数量:', this.messages.length);
        return conversationData;
      } catch (error) {
        console.error('获取对话详情失败:', error);
        console.error('错误详情:', error.response?.data);
        this.error = error.response?.data?.detail || '获取对话详情失败';
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 删除对话
    async deleteConversation(conversationId) {
      this.isLoading = true;
      this.error = null;
      
      try {
        await api.delete(`/api/conversations/${conversationId}`);
        
        // 从列表中移除对话
        this.conversations = this.conversations.filter(
          conv => conv.id !== conversationId
        );
        
        // 如果删除的是当前对话，清除当前对话
        if (this.currentConversation && this.currentConversation.id === conversationId) {
          this.currentConversation = null;
          this.messages = [];
        }
        
        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || '删除对话失败';
        console.error('删除对话失败:', error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 批量删除对话
    async deleteConversationsBatch(conversationIds) {
      this.isLoading = true;
      this.error = null;
      
      try {
        // 使用POST请求来模拟批量删除，因为DELETE请求可能不支持请求体
        const response = await api.post('/api/conversations/batch-delete', {
          conversation_ids: conversationIds
        });
        
        // 从列表中移除已删除的对话
        this.conversations = this.conversations.filter(
          conv => !conversationIds.includes(conv.id)
        );
        
        // 如果删除的对话中包含当前对话，清除当前对话
        if (this.currentConversation && conversationIds.includes(this.currentConversation.id)) {
          this.currentConversation = null;
          this.messages = [];
        }
        
        return response;
      } catch (error) {
        this.error = error.response?.data?.detail || '批量删除对话失败';
        console.error('批量删除对话失败:', error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 删除所有对话
    async deleteAllConversations() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await api.delete('/api/conversations/all');
        
        // 清空所有对话
        this.conversations = [];
        this.currentConversation = null;
        this.messages = [];
        
        return response;
      } catch (error) {
        this.error = error.response?.data?.detail || '删除所有对话失败';
        console.error('删除所有对话失败:', error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 批量删除对话
    async deleteConversationsBatch(conversationIds) {
      this.isLoading = true;
      this.error = null;
      
      try {
        // 使用POST请求来模拟批量删除，因为DELETE请求可能不支持请求体
        const response = await api.post('/api/conversations/batch-delete', {
          conversation_ids: conversationIds
        });
        
        // 从列表中移除已删除的对话
        this.conversations = this.conversations.filter(
          conv => !conversationIds.includes(conv.id)
        );
        
        // 如果删除的对话中包含当前对话，清除当前对话
        if (this.currentConversation && conversationIds.includes(this.currentConversation.id)) {
          this.currentConversation = null;
          this.messages = [];
        }
        
        return response;
      } catch (error) {
        this.error = error.response?.data?.detail || '批量删除对话失败';
        console.error('批量删除对话失败:', error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 删除所有对话
    async deleteAllConversations() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await api.delete('/api/conversations/all');
        
        // 清空所有对话
        this.conversations = [];
        this.currentConversation = null;
        this.messages = [];
        
        return response;
      } catch (error) {
        this.error = error.response?.data?.detail || '删除所有对话失败';
        console.error('删除所有对话失败:', error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 更新对话标题
    async updateConversationTitle(conversationId, title) {
      this.isLoading = true;
      this.error = null;
      
      try {
        // 注意：后端目前没有更新对话标题的API，这里直接更新本地状态
        // 更新本地对话列表中的标题
        const conversation = this.conversations.find(conv => conv.id === conversationId);
        if (conversation) {
          conversation.title = title;
        }
        
        // 更新当前对话标题
        if (this.currentConversation && this.currentConversation.id === conversationId) {
          this.currentConversation.title = title;
        }
        
        return { success: true, message: '标题已更新' };
      } catch (error) {
        this.error = '更新对话标题失败';
        console.error('更新对话标题失败:', error);
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // 发送消息
    async sendMessage(content, useStream = false) {
      console.log('开始发送消息:', { content, useStream });
      this.isSending = true;
      this.error = null;
      
      try {
        if (!this.currentConversation?.id) {
          throw new Error('没有选中的对话');
        }
        
        // 创建用户消息
        const userMessage = {
          id: `user-${Date.now()}`,
          conversation_id: this.currentConversation.id,
          content: content,
          role: 'user',
          created_at: new Date().toISOString()
        };
        
        // 添加用户消息到消息列表
        this.messages.push(userMessage);
        
        // 显示加载中的AI回复
        const aiTempId = `ai-temp-${Date.now()}`;
        const aiMessage = {
          id: aiTempId,
          conversation_id: this.currentConversation.id,
          content: '',
          role: 'assistant',
          created_at: new Date().toISOString(),
          streaming: true
        };
        this.messages.push(aiMessage);
        
        // 如果是流式响应
        if (useStream) {
          console.log('使用流式响应模式...');
          return await this.handleStreamResponse(content, aiTempId);
        }
        
        // 非流式响应
        console.log('使用非流式响应模式...');
        const response = await api.post(`/api/conversations/${this.currentConversation.id}/messages`, {
          content: content,
          use_stream: false
        });
        
        console.log('API请求成功! 响应数据:', response);
        
        // 更新AI消息
        const aiResponseContent = response.ai_message?.content || '未获取到响应内容';
        const messageIndex = this.messages.findIndex(m => m.id === aiTempId);
        
        if (messageIndex !== -1) {
          this.messages.splice(messageIndex, 1, {
            ...this.messages[messageIndex],
            content: aiResponseContent,
            streaming: false,
            id: response.ai_message?.id || aiTempId
          });
        }
        
        return response;
      } catch (error) {
        console.error('发送消息失败:', error);
        this.error = error.response?.detail || error.message || '发送消息失败';
        
        // 清理临时AI消息
        const aiTempMessages = this.messages.filter(m => m.id.startsWith('ai-temp-'));
        aiTempMessages.forEach(msg => {
          const index = this.messages.findIndex(m => m.id === msg.id);
          if (index !== -1) {
            this.messages.splice(index, 1);
          }
        });
        
        throw error;
      } finally {
        this.isSending = false;
      }
    },
    
    // 处理流式响应
    async handleStreamResponse(content, aiTempId) {
      try {
        const response = await fetch(`http://localhost:8000/api/conversations/${this.currentConversation.id}/messages`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({
            content: content,
            use_stream: true
          })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) break;
          
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop(); // 保留未完成的行
          
          for (const line of lines) {
            if (line.trim()) {
              try {
                const data = JSON.parse(line);
                
                if (data.type === 'chunk') {
                  // 更新流式内容
                  const messageIndex = this.messages.findIndex(m => m.id === aiTempId);
                  if (messageIndex !== -1) {
                    const currentMessage = this.messages[messageIndex];
                    this.messages.splice(messageIndex, 1, {
                      ...currentMessage,
                      content: currentMessage.content + data.content
                    });
                  }
                } else if (data.type === 'end') {
                  // 流式响应结束
                  const messageIndex = this.messages.findIndex(m => m.id === aiTempId);
                  if (messageIndex !== -1) {
                    this.messages.splice(messageIndex, 1, {
                      ...this.messages[messageIndex],
                      streaming: false,
                      id: data.ai_message?.id || aiTempId
                    });
                  }
                  return data;
                } else if (data.type === 'error') {
                  throw new Error(data.error);
                }
              } catch (parseError) {
                console.error('解析流式数据失败:', parseError);
              }
            }
          }
        }
        
        // 如果流式响应意外结束
        const messageIndex = this.messages.findIndex(m => m.id === aiTempId);
        if (messageIndex !== -1) {
          this.messages.splice(messageIndex, 1, {
            ...this.messages[messageIndex],
            streaming: false
          });
        }
        
      } catch (error) {
        console.error('流式响应处理失败:', error);
        
        // 清理临时AI消息
        const messageIndex = this.messages.findIndex(m => m.id === aiTempId);
        if (messageIndex !== -1) {
          this.messages.splice(messageIndex, 1);
        }
        
        throw error;
      }
    },
    
    // 处理模拟响应
    async handleMockResponse(aiTempId, content) {
      console.log('使用模拟模式响应...');
      
      // 根据用户输入内容提供更相关的模拟响应
      let mockResponses;
      if (content.includes('你好') || content.includes('嗨')) {
        mockResponses = [
          '你好！',
          '很高兴见到你！',
          '我是一个AI助手，',
          '可以帮助你解答问题，',
          '或者进行各种对话交流。',
          '有什么我可以帮助你的吗？'
        ];
      } else if (content.includes('帮助') || content.includes('怎么')) {
        mockResponses = [
          '当然可以！',
          '我很乐意帮助你。',
          '请问具体是什么问题？',
          '或者你需要哪方面的指导？',
          '请详细告诉我，',
          '我会尽力为你提供帮助。'
        ];
      } else {
        mockResponses = [
          '感谢你的提问！',
          '我理解你的需求，',
          '这是一个很好的问题。',
          '根据我的理解，',
          '你可以考虑以下几点：',
          '首先，明确目标；',
          '其次，制定计划；',
          '最后，付诸行动。',
          '希望这些信息对你有所帮助！'
        ];
      }
      
      let fullResponse = '';
      for (let i = 0; i < mockResponses.length; i++) {
        // 模拟网络延迟（150-400ms）
        await new Promise(resolve => setTimeout(resolve, 150 + Math.random() * 250));
        
        // 更新内容
        fullResponse += mockResponses[i];
        
        // 找到AI消息的索引
        const messageIndex = this.messages.findIndex(m => m.id === aiTempId);
        if (messageIndex !== -1) {
          // 使用splice创建新对象来确保响应式更新
          this.messages.splice(messageIndex, 1, {
            ...this.messages[messageIndex],
            content: fullResponse
          });
        }
      }
      
      // 模拟完成后更新消息状态
      const finalIndex = this.messages.findIndex(m => m.id === aiTempId);
      if (finalIndex !== -1) {
        this.messages.splice(finalIndex, 1, {
          ...this.messages[finalIndex],
          streaming: false
        });
      }
      
      console.log('流式消息发送完成（模拟模式）');
    }
  }
});