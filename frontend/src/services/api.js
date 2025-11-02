import axios from 'axios'

// 创建axios实例
export const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    
    // 如果存在token，则设置Authorization头
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 处理401未授权错误
    if (error.response?.status === 401) {
      // 清除本地存储并跳转到登录页
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    
    // 处理其他错误
    return Promise.reject(error)
  }
)

// 认证相关API
export const authApi = {
  // 用户注册
  register: (username, email, password) => {
    return api.post('/api/auth/register', {
      username,
      email,
      password
    })
  },
  
  // 用户登录
  login: (email, password) => {
    // 创建表单数据
    const formData = new URLSearchParams()
    formData.append('username', email) // OAuth2PasswordRequestForm使用username字段
    formData.append('password', password)
    return api.post('/api/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  }
}

// 对话相关API
export const conversationApi = {
  // 获取所有对话
  getAll: () => {
    return api.get('/api/conversations')
  },
  
  // 创建对话
  create: (title) => {
    // 注意：后端API期望title作为查询参数，而不是请求体的一部分
    return api.post('/api/conversations', null, {
      params: { title }
    })
  },
  
  // 获取对话详情
  getById: (conversationId) => {
    return api.get(`/api/conversations/${conversationId}`)
  },
  
  // 更新对话
  update: (conversationId, data) => {
    return api.put(`/api/conversations/${conversationId}`, data)
  },
  
  // 删除对话
  delete: (conversationId) => {
    return api.delete(`/api/conversations/${conversationId}`)
  }
}

// 消息相关API
export const messageApi = {
  // 获取对话的消息列表
  getByConversation: (conversationId) => {
    return api.get(`/api/conversations/${conversationId}/messages`)
  },
  
  // 创建消息
  create: (conversationId, content, role = 'user') => {
    return api.post('/api/messages', {
      conversation_id: conversationId,
      content,
      role
    })
  }
}

// 聊天相关API
export const chatApi = {
  // 发送聊天消息到特定对话
  sendMessage: (conversationId, content) => {
    return api.post(`/api/conversations/${conversationId}/messages`, {
      content
    })
  }
}

export default api