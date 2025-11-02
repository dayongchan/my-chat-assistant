import { createRouter, createWebHistory } from 'vue-router'

// 懒加载路由组件
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Chat = () => import('../views/Chat.vue')
const NotFound = () => import('../views/NotFound.vue')

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Chat',
    component: Chat,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      requiresAuth: false,
      redirectIfAuthenticated: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      requiresAuth: false,
      redirectIfAuthenticated: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token') !== null
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 需要认证但未登录，重定向到登录页
    next({ name: 'Login', query: { redirect: to.fullPath } })
  }
  // 检查是否已认证且需要重定向
  else if (to.meta.redirectIfAuthenticated && isAuthenticated) {
    // 已登录且不需要认证的页面，重定向到主页
    next({ name: 'Chat' })
  }
  else {
    // 正常导航
    next()
  }
})

export default router