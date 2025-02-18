import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { MotionPlugin } from '@vueuse/motion'
import axios from 'axios'
import router from './router'
import App from './App.vue'
import './style.css'
import { useAuthStore } from './stores/auth'

// Configure axios
// 在开发环境使用完整的URL，在生产环境使用相对路径
axios.defaults.baseURL = import.meta.env.DEV ? 'http://localhost:8923' : ''

// 从 localStorage 恢复 token 并设置到 axios 头部
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

// 初始化认证状态
const authStore = useAuthStore(pinia)
authStore.initializeAuth()

app.use(router)
app.use(MotionPlugin)

app.mount('#app')
