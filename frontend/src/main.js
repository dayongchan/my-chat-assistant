import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// 导入全局样式
import './assets/style.css'

// 创建应用实例
const app = createApp(App)

// 使用Pinia状态管理
app.use(createPinia())

// 使用路由
app.use(router)

// 配置axios全局实例
// axios.defaults.baseURL = 'http://localhost:8000/api'
axios.defaults.baseURL = '/api'
axios.defaults.timeout = 10000

// 添加请求拦截器
axios.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 挂载应用
app.mount('#app')