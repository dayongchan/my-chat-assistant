<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1 class="status-code">404</h1>
      <h2 class="error-title">页面未找到</h2>
      <p class="error-message">抱歉，您访问的页面不存在或已被移除</p>
      <router-link to="/" class="back-link">返回首页</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.not-found-content {
  text-align: center;
  background-color: white;
  border-radius: 12px;
  padding: 60px 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.status-code {
  font-size: 80px;
  font-weight: 700;
  margin: 0 0 20px 0;
  color: #1890ff;
  line-height: 1;
}

.error-title {
  font-size: 28px;
  margin: 0 0 16px 0;
  color: #333;
}

.error-message {
  font-size: 16px;
  color: #666;
  margin: 0 0 30px 0;
  line-height: 1.5;
}

.back-link {
  display: inline-block;
  padding: 12px 24px;
  background-color: #1890ff;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.back-link:hover {
  background-color: #40a9ff;
}
</style>