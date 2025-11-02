<template>
  <div class="register-container">
    <div class="register-form">
      <h2 class="register-title">注册 My Chat Assistant</h2>
      
      <form @submit.prevent="handleRegister" class="form">
        <div class="form-group">
          <label for="username" class="form-label">用户名</label>
          <input
            type="text"
            id="username"
            v-model="username"
            class="form-input"
            placeholder="请输入用户名"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="email" class="form-label">邮箱</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="form-input"
            placeholder="请输入邮箱"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">密码</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-input"
            placeholder="请输入密码（至少6位）"
            required
            minlength="6"
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword" class="form-label">确认密码</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            class="form-input"
            placeholder="请再次输入密码"
            required
          />
          <div v-if="password !== confirmPassword && confirmPassword" class="password-match-error">
            两次输入的密码不一致
          </div>
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button
          type="submit"
          class="register-button"
          :disabled="isLoading || password !== confirmPassword || password.length < 6"
        >
          {{ isLoading ? '注册中...' : '注册' }}
        </button>
      </form>
      
      <div class="login-link">
        <p>已有账号？<router-link to="/login">立即登录</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/userStore'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const username = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const error = ref('')
    
    const handleRegister = async () => {
      // 基本表单验证
      if (password.value !== confirmPassword.value) {
        error.value = '两次输入的密码不一致'
        return
      }
      
      if (password.value.length < 6) {
        error.value = '密码长度至少为6位'
        return
      }
      
      error.value = ''
      
      try {
        // 先检查用户名、邮箱和密码是否符合要求
        if (!username.value || username.value.length < 3) {
          error.value = '用户名至少需要3个字符'
          return
        }
        
        if (!email.value || !email.value.includes('@')) {
          error.value = '请输入有效的邮箱地址'
          return
        }
        
        if (!password.value || password.value.length < 6) {
          error.value = '密码至少需要6个字符'
          return
        }
        
        // 注册用户
        console.log('开始注册用户:', username.value)
        await userStore.register(username.value, email.value, password.value)
        
        // 注册成功后自动登录
        console.log('注册成功，尝试自动登录...')
        try {
          await userStore.login(email.value, password.value)
          
          // 登录成功，跳转到聊天页面
          router.push('/')
        } catch (loginError) {
          console.error('自动登录失败:', loginError)
          // 注册成功但登录失败，提示用户手动登录
          error.value = '注册成功，但自动登录失败。请手动登录。'
        }
      } catch (err) {
        console.error('注册错误:', err)
        error.value = userStore.error || '注册失败，请稍后再试'
      }
    }
    
    return {
      username,
      email,
      password,
      confirmPassword,
      error,
      isLoading: computed(() => userStore.isLoading),
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.register-form {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.register-title {
  text-align: center;
  color: #1890ff;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.password-match-error {
  color: #ff4d4f;
  font-size: 14px;
  margin-top: 4px;
}

.error-message {
  color: #ff4d4f;
  margin-bottom: 16px;
  padding: 12px;
  background-color: #fff2f0;
  border-radius: 6px;
  border: 1px solid #ffccc7;
}

.register-button {
  width: 100%;
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

.register-button:hover:not(:disabled) {
  background-color: #40a9ff;
}

.register-button:disabled {
  background-color: #d9d9d9;
  cursor: not-allowed;
}

.login-link {
  margin-top: 20px;
  text-align: center;
  color: #666;
}

.login-link a {
  color: #1890ff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>