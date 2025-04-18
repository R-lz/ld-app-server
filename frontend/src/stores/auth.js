import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login(username, password) {
      try {
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        const response = await axios.post('/token', formData)
        const { access_token } = response.data

        this.token = access_token
        localStorage.setItem('token', access_token)

        // 确保 token 格式正确
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

        return true
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
      const router = useRouter()
      router.push('/login')
    },

    // 添加初始化方法
    initializeAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
    },

    // 添加错误拦截器
    setupAxiosInterceptors() {
      axios.interceptors.response.use(
        response => response,
        error => {
          if (error.response?.status === 401) {
            this.logout()
          }
          return Promise.reject(error)
        }
      )
    }
  }
}) 