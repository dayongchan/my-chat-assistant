<template>
  <div class="app-container">
    <!-- 路由视图 -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {}
  }
}
</script>

<style>
.app-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 全局样式 */
:root {
  --primary-color: #0070f3;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --info-color: #17a2b8;
  --light-color: #f8f9fa;
  --dark-color: #343a40;
  --border-color: #dee2e6;
  --background-color: #ffffff;
  --text-color: #333333;
  --text-muted: #6c757d;
}

/* 通用样式 */
button {
  cursor: pointer;
  border: none;
  outline: none;
  background: none;
  font-family: inherit;
}

input, textarea {
  font-family: inherit;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>