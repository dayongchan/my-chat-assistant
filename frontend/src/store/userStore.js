import { defineStore } from 'pinia'
import { api } from '../services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  }),
  
  actions: {
    // 初始化用户状态
    initialize() {
      const token = localStorage.getItem('access_token')
      const userData = localStorage.getItem('user')
      
      if (token && userData) {
        this.currentUser = JSON.parse(userData)
        this.isAuthenticated = true
      }
    },
    
    // 用户注册
    async register(username, email, password) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await api.post('/api/auth/register', {
          username,
          email,
          password
        })
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '注册失败'
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    // 用户登录
    async login(email, password) {
      this.isLoading = true
      this.error = null
      
      try {
        // 创建表单数据
        const formData = new URLSearchParams()
        formData.append('username', email) // OAuth2PasswordRequestForm使用username字段
        formData.append('password', password)
        
        console.log('登录请求发送到: /api/auth/token')
        // 注意：由于响应拦截器直接返回了response.data，所以这里的response实际上是后端返回的data对象
        const response = await api.post('/api/auth/token', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        
        console.log('登录响应:', response)
        
        // 检查响应结构
        if (!response) {
          throw new Error('无效的服务器响应')
        }
        
        // 由于响应拦截器直接返回了data，所以这里直接从response中提取token
        let access_token, refresh_token
        if (response.access_token && response.token_type) {
          // 响应直接包含token信息
          access_token = response.access_token
          refresh_token = response.refresh_token
        } else {
          throw new Error('无效的响应格式，未找到token信息')
        }
        
        if (!access_token) {
          throw new Error('未获取到访问令牌')
        }
        
        // 保存token和用户信息
        localStorage.setItem('access_token', access_token)
        if (refresh_token) {
          localStorage.setItem('refresh_token', refresh_token)
        }
        
        // 假设从token中解析用户信息
        this.currentUser = {
          email,
          // 这里可以添加更多用户信息
        }
        localStorage.setItem('user', JSON.stringify(this.currentUser))
        
        this.isAuthenticated = true
        return response
      } catch (error) {
        console.error('登录错误:', error)
        // 提供更详细的错误信息
        if (error.response) {
          this.error = error.response.data?.detail || error.response.data?.message || '用户名或密码错误'
        } else if (error.request) {
          this.error = '网络错误，请检查您的连接'
        } else {
          this.error = error.message || '登录失败，请稍后重试'
        }
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    // 用户登出
    logout() {
      // 清除本地存储
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      
      // 重置状态
      this.currentUser = null
      this.isAuthenticated = false
      this.error = null
    },
    
    // 更新用户信息
    async updateUser(userData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await api.put('/api/user/me', userData)
        this.currentUser = response.data
        localStorage.setItem('user', JSON.stringify(this.currentUser))
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '更新用户信息失败'
        throw error
      } finally {
        this.isLoading = false
      }
    }
  }
})