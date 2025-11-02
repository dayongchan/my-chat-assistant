<template>
  <div class="login-container">
    <div class="login-form">
      <h2 class="login-title">登录 My Chat Assistant</h2>
      
      <form @submit.prevent="handleLogin" class="form">
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
            placeholder="请输入密码"
            required
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button
          type="submit"
          class="login-button"
          :disabled="isLoading"
        >
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div class="register-link">
        <p>还没有账号？<router-link to="/register">立即注册</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/userStore'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const email = ref('')
    const password = ref('')
    const error = ref('')
    
    const handleLogin = async () => {
      error.value = ''
      
      try {
        await userStore.login(email.value, password.value)
        
        // 获取重定向URL
        const redirectPath = router.currentRoute.value.query.redirect || '/'
        router.push(redirectPath)
      } catch (err) {
        error.value = userStore.error || '登录失败，请检查您的邮箱和密码'
      }
    }
    
    return {
      email,
      password,
      error,
      isLoading: computed(() => userStore.isLoading),
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.login-form {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-title {
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

.error-message {
  color: #ff4d4f;
  margin-bottom: 16px;
  padding: 12px;
  background-color: #fff2f0;
  border-radius: 6px;
  border: 1px solid #ffccc7;
}

.login-button {
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

.login-button:hover:not(:disabled) {
  background-color: #40a9ff;
}

.login-button:disabled {
  background-color: #d9d9d9;
  cursor: not-allowed;
}

.register-link {
  margin-top: 20px;
  text-align: center;
  color: #666;
}

.register-link a {
  color: #1890ff;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>