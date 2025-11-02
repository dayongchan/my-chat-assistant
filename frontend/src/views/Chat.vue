<template>
  <div class="chat-container">
    <!-- 侧边栏：对话列表 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2 class="app-title">My Chat Assistant</h2>
        <button class="new-chat-button" @click="handleNewChat">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 3V17M3 10H17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          新建对话
        </button>
      </div>
      
      <!-- 批量操作工具栏 -->
      <div v-if="conversations.length > 0" class="batch-toolbar">
        <div class="batch-controls">
          <label class="select-all-label">
            <input
              type="checkbox"
              v-model="selectAll"
              @change="handleSelectAll"
            />
            全选
          </label>
          <span class="selected-count">已选择 {{ selectedConversations.length }} 个对话</span>
          <div class="batch-actions">
            <button
              v-if="selectedConversations.length > 0"
              class="batch-delete-button"
              @click="deleteSelectedConversations"
            >
              删除选中
            </button>
            <button
              class="delete-all-button"
              @click="deleteAllConversations"
            >
              清空所有
            </button>
          </div>
        </div>
      </div>
      
      <div class="conversation-list">
        <div
          v-for="conversation in conversations"
          :key="conversation.id"
          :class="['conversation-item', { active: currentConversation?.id === conversation.id, selected: selectedConversations.includes(conversation.id) }]"
          @click="selectConversation(conversation.id)"
        >
          <div class="conversation-checkbox">
            <input
              type="checkbox"
              :value="conversation.id"
              v-model="selectedConversations"
              @click.stop
            />
          </div>
          <div class="conversation-info">
            <h3 class="conversation-title">{{ conversation.title }}</h3>
            <p class="conversation-preview">{{ getPreviewText(conversation) }}</p>
          </div>
          <button class="delete-button" @click.stop="deleteConversation(conversation.id)">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 4L13 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M3 12L13 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
      
      <div class="sidebar-footer">
        <button class="logout-button" @click="handleLogout">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M7 12L11 8L7 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M11 8H3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          退出登录
        </button>
      </div>
    </div>
    
    <!-- 主聊天区域 -->
    <div class="chat-main">
      <div v-if="currentConversation" class="chat-content">
        <!-- 对话标题栏 -->
        <div class="chat-header">
          <input
            v-model="currentConversation.title"
            class="conversation-title-input"
            @blur="updateConversationTitle"
            placeholder="对话标题"
          />
        </div>
        
        <!-- 消息列表 -->
        <div class="messages-container" ref="messagesContainer">
          <div v-if="messages.length === 0" class="empty-messages">
            <p>开始与AI助手对话吧！</p>
          </div>
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message-wrapper', message.role]">
            <div class="message">
              <div class="message-avatar">
                {{ message.role === 'user' ? '👤' : '🤖' }}
              </div>
              <div class="message-content">
                <p>{{ message.content }}</p>
              </div>
            </div>
          </div>
          <div v-if="isSending" class="message-wrapper assistant sending">
            <div class="message">
              <div class="message-avatar">🤖</div>
              <div class="message-content">
                <div class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 输入区域 -->
        <div class="input-container">
          <form @submit.prevent="sendMessage" class="input-form">
            <textarea
              v-model="inputMessage"
              class="message-input"
              placeholder="输入消息..."
              rows="3"
              :disabled="isSending"
              ref="inputRef"
              @keydown.enter.prevent="sendMessage"
            ></textarea>
            <div class="input-controls">
              <div class="stream-toggle">
                <input type="checkbox" id="streamMode" v-model="useStream" />
                <label for="streamMode">流式响应</label>
              </div>
              <button
                type="submit"
                class="send-button"
                :disabled="isSending || !inputMessage.trim()"
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M2 10H18M18 10L11 3M18 10L11 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                发送
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <div v-else class="no-conversation">
        <div class="empty-state">
          <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="40" cy="28" r="12" stroke="#1890ff" stroke-width="2"/>
            <path d="M40 50C49.9411 50 58 41.9411 58 32C58 22.0589 49.9411 14 40 14C30.0589 14 22 22.0589 22 32C22 32.2761 22.0107 32.5505 22.0319 32.8227C17.1047 33.8705 13 38.2415 13 44C13 49.5228 17.4772 54 23 54H57C62.5228 54 67 49.5228 67 44C67 38.2415 62.8953 33.8705 57.9681 32.8227C57.9893 32.5505 58 32.2761 58 32H57C57 40.2843 49.2843 48 41 48V63L27 54L41 45V60C46.5228 60 51 55.5228 51 50H40Z" fill="#1890ff" fill-opacity="0.1"/>
          </svg>
          <h3>没有选择对话</h3>
          <p>点击"新建对话"开始与AI助手交流</p>
          <button class="start-chat-button" @click="handleNewChat">
            开始新对话
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '../store/chatStore'
import { useUserStore } from '../store/userStore'

export default {
  name: 'Chat',
  setup() {
    const router = useRouter()
    const chatStore = useChatStore()
    const userStore = useUserStore()
    
    const inputMessage = ref('')
    const useStream = ref(true)
    const messagesContainer = ref(null)
    const inputRef = ref(null)
    
    // 批量删除相关变量
    const selectedConversations = ref([])
    const selectAll = ref(false)
    
    // 初始化
    onMounted(async () => {
      // 先初始化用户状态（从localStorage恢复认证状态）
      userStore.initialize()
      
      // 确保用户已认证
      if (!userStore.isAuthenticated) {
        router.push('/login')
        return
      }
      
      console.log("准备加载对话列表")
      // 加载对话列表
      await chatStore.fetchConversations()
      
      // 尝试恢复上次选中的对话
      const lastConversationId = localStorage.getItem('lastConversationId')
      if (lastConversationId && chatStore.conversations.some(conv => conv.id === parseInt(lastConversationId))) {
        await chatStore.setCurrentConversation(parseInt(lastConversationId))
      } else if (chatStore.conversations.length > 0) {
        // 如果没有保存的对话ID，自动选择第一个
        await chatStore.setCurrentConversation(chatStore.conversations[0].id)
      }
    })
    
    // 计算属性
    const conversations = computed(() => chatStore.conversations)
    const currentConversation = computed(() => chatStore.currentConversation)
    const messages = computed(() => chatStore.messages)
    const isSending = computed(() => chatStore.isSending)
    
    // 获取对话预览文本
    const getPreviewText = (conversation) => {
      if (conversation.messages && conversation.messages.length > 0) {
        const lastMessage = conversation.messages[conversation.messages.length - 1]
        return lastMessage.content.length > 30 
          ? lastMessage.content.substring(0, 30) + '...' 
          : lastMessage.content
      }
      return '没有消息'
    }
    
    // 选择对话
    const selectConversation = async (conversationId) => {
      await chatStore.setCurrentConversation(conversationId)
      // 保存当前对话ID到本地存储
      localStorage.setItem('lastConversationId', conversationId.toString())
      scrollToBottom()
    }
    
    // 创建新对话
    const handleNewChat = async () => {
      const newConversation = await chatStore.createConversation()
      // 保存新对话ID到本地存储
      if (newConversation && newConversation.id) {
        localStorage.setItem('lastConversationId', newConversation.id.toString())
      }
      inputRef.value?.focus()
    }
    
    // 删除对话
    const deleteConversation = async (conversationId) => {
      if (confirm('确定要删除这个对话吗？删除后无法恢复。')) {
        await chatStore.deleteConversation(conversationId)
        // 如果删除的是当前对话，清理本地存储的对话ID
        const lastConversationId = localStorage.getItem('lastConversationId')
        if (lastConversationId && parseInt(lastConversationId) === conversationId) {
          localStorage.removeItem('lastConversationId')
        }
      }
    }
    
    // 更新对话标题
    const updateConversationTitle = async () => {
      if (currentConversation.value && currentConversation.value.title.trim()) {
        await chatStore.updateConversationTitle(
          currentConversation.value.id,
          currentConversation.value.title.trim()
        )
      }
    }
    
    // 发送消息
    const sendMessage = async () => {
      if (!inputMessage.value.trim() || isSending.value) return
      
      const messageContent = inputMessage.value.trim()
      
      // 清空输入框
      inputMessage.value = ''
      
      // 滚动到底部
      await nextTick()
      scrollToBottom()
      
      try {
        await chatStore.sendMessage(messageContent, useStream.value)
        
        // 发送成功后再次滚动到底部
        await nextTick()
        scrollToBottom()
      } catch (error) {
        console.error('发送消息失败:', error)
      }
    }
    
    // 滚动到底部
    const scrollToBottom = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }
    
    // 退出登录
    const handleLogout = () => {
      userStore.logout()
      router.push('/login')
    }
    
    // 批量删除相关函数
    const handleSelectAll = () => {
      if (selectAll.value) {
        selectedConversations.value = conversations.value.map(conv => conv.id)
      } else {
        selectedConversations.value = []
      }
    }
    
    // 删除选中的对话
    const deleteSelectedConversations = async () => {
      if (selectedConversations.value.length === 0) return
      
      const message = selectedConversations.value.length === 1 
        ? '确定要删除这个对话吗？删除后无法恢复。'
        : `确定要删除选中的 ${selectedConversations.value.length} 个对话吗？删除后无法恢复。`
      
      if (confirm(message)) {
        try {
          await chatStore.deleteConversationsBatch(selectedConversations.value)
          selectedConversations.value = []
          selectAll.value = false
        } catch (error) {
          console.error('批量删除对话失败:', error)
        }
      }
    }
    
    // 删除所有对话
    const deleteAllConversations = async () => {
      if (conversations.value.length === 0) return
      
      if (confirm(`确定要删除所有 ${conversations.value.length} 个对话吗？删除后无法恢复。`)) {
        try {
          await chatStore.deleteAllConversations()
          selectedConversations.value = []
          selectAll.value = false
        } catch (error) {
          console.error('删除所有对话失败:', error)
        }
      }
    }
    
    return {
      conversations,
      currentConversation,
      messages,
      isSending,
      inputMessage,
      useStream,
      messagesContainer,
      inputRef,
      selectedConversations,
      selectAll,
      getPreviewText,
      selectConversation,
      handleNewChat,
      deleteConversation,
      updateConversationTitle,
      sendMessage,
      handleLogout,
      handleSelectAll,
      deleteSelectedConversations,
      deleteAllConversations
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  background-color: #f5f7fa;
}

/* 侧边栏样式 */
.sidebar {
  width: 300px;
  background-color: white;
  border-right: 1px solid #e8e8e8;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e8e8e8;
}

.app-title {
  margin: 0 0 20px 0;
  color: #1890ff;
  font-size: 20px;
  font-weight: 600;
}

.new-chat-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.new-chat-button:hover {
  background-color: #40a9ff;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.conversation-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.conversation-item:hover {
  background-color: #f5f5f5;
}

.conversation-item.active {
  background-color: #e6f7ff;
  border-left: 3px solid #1890ff;
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.conversation-title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 500;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conversation-preview {
  margin: 0;
  font-size: 14px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-button {
  padding: 6px;
  background: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  color: #999;
  transition: all 0.2s;
}

.delete-button:hover {
  background-color: #fff2f0;
  color: #ff4d4f;
}

/* 批量操作工具栏样式 */
.batch-toolbar {
  padding: 12px 20px;
  border-bottom: 1px solid #e8e8e8;
  background-color: #fafafa;
}

.batch-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.select-all-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
}

.selected-count {
  font-size: 14px;
  color: #1890ff;
  font-weight: 500;
}

.batch-actions {
  display: flex;
  gap: 8px;
}

.batch-delete-button, .delete-all-button {
  padding: 6px 12px;
  border: 1px solid #ff4d4f;
  border-radius: 4px;
  background-color: #fff;
  color: #ff4d4f;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.batch-delete-button:hover, .delete-all-button:hover {
  background-color: #ff4d4f;
  color: white;
}

.batch-delete-button:disabled {
  border-color: #d9d9d9;
  background-color: #f5f5f5;
  color: #bfbfbf;
  cursor: not-allowed;
}

/* 对话项选中状态 */
.conversation-item.selected {
  background-color: #e6f7ff;
  border-left: 3px solid #1890ff;
}

.conversation-checkbox {
  margin-right: 8px;
  display: flex;
  align-items: center;
}

.conversation-checkbox input[type="checkbox"] {
  cursor: pointer;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #e8e8e8;
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  background-color: #f5f5f5;
  color: #666;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-button:hover {
  background-color: #e8e8e8;
  color: #ff4d4f;
}

/* 主聊天区域样式 */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: 16px 24px;
  background-color: white;
  border-bottom: 1px solid #e8e8e8;
}

.conversation-title-input {
  width: 100%;
  padding: 8px;
  border: none;
  font-size: 18px;
  font-weight: 500;
  color: #333;
  background: transparent;
  outline: none;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.empty-messages {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #999;
  font-size: 16px;
}

.message-wrapper {
  display: flex;
}

.message-wrapper.user {
  justify-content: flex-end;
}

.message-wrapper.assistant {
  justify-content: flex-start;
}

.message {
  display: flex;
  max-width: 70%;
  gap: 12px;
}

.message-wrapper.user .message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-content {
  background-color: white;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  word-wrap: break-word;
}

.message-wrapper.user .message-content {
  background-color: #1890ff;
  color: white;
}

.typing-indicator {
  display: flex;
  gap: 6px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.input-container {
  padding: 20px;
  background-color: white;
  border-top: 1px solid #e8e8e8;
}

.input-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-input {
  width: 100%;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 16px;
  resize: none;
  outline: none;
  transition: border-color 0.3s;
}

.message-input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.input-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stream-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
}

.stream-toggle input[type="checkbox"] {
  cursor: pointer;
}

.send-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button:hover:not(:disabled) {
  background-color: #40a9ff;
}

.send-button:disabled {
  background-color: #d9d9d9;
  cursor: not-allowed;
}

/* 无对话状态样式 */
.no-conversation {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #999;
}

.empty-state {
  text-align: center;
  padding: 40px;
}

.empty-state h3 {
  margin: 20px 0 10px 0;
  color: #333;
  font-size: 20px;
}

.empty-state p {
  margin: 0 0 30px 0;
  font-size: 16px;
}

.start-chat-button {
  padding: 12px 24px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.start-chat-button:hover {
  background-color: #40a9ff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: 40%;
    border-right: none;
    border-bottom: 1px solid #e8e8e8;
  }
  
  .chat-main {
    height: 60%;
  }
  
  .message {
    max-width: 90%;
  }
}
</style>