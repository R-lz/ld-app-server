<template>
  <div class="min-h-[80vh] flex items-center justify-center">
    <div class="card w-full max-w-md">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold bg-gradient-to-r from-primary to-primary-light text-transparent bg-clip-text">
          欢迎回来
        </h2>
        <p class="mt-2 text-gray-600">请登录以继续</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">用户名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="input mt-1"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="input mt-1"
          />
        </div>

        <div v-if="error" class="text-red-500 text-sm">
          {{ error }}
        </div>

        <button
          type="submit"
          class="btn-primary w-full flex justify-center"
          :disabled="loading"
        >
          <span v-if="loading" class="animate-spin mr-2">⟳</span>
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(username.value, password.value)
    const redirectPath = route.query.redirect || '/'
    router.push(redirectPath)
  } catch (err) {
    error.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
</script> 