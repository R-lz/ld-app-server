import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    darkMode: localStorage.getItem('darkMode') === 'true' || false
  }),

  actions: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode.toString())
      this.applyTheme()
    },
    
    setDarkMode(value) {
      this.darkMode = value
      localStorage.setItem('darkMode', this.darkMode.toString())
      this.applyTheme()
    },
    
    applyTheme() {
      // 应用暗黑模式到根HTML元素
      if (this.darkMode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    },
    
    // 初始化主题
    initTheme() {
      // 检查用户的系统偏好
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      
      // 如果本地存储没有设置，则使用系统偏好
      if (localStorage.getItem('darkMode') === null && prefersDark) {
        this.setDarkMode(true)
      } else {
        this.applyTheme()
      }
    }
  }
}) 