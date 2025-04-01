<template>
  <div class="space-y-8 max-w-7xl mx-auto px-4 py-6">
    <div class="flex justify-between items-center" v-motion-slide-visible-once-top>
      <h2 class="text-3xl font-bold gradient-heading">应用配置管理</h2>
      <button 
        @click="showAddModal = true" 
        class="inline-flex items-center px-4 py-2 bg-gradient-to-r from-primary to-primary-light text-white font-medium rounded-md shadow-sm hover:shadow-md transition-all duration-200 transform hover:-translate-y-0.5" 
        v-if="isAdmin"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        添加配置
      </button>
    </div>

    <div v-if="loading" class="text-center py-16" v-motion-fade>
      <div class="inline-block animate-spin text-primary text-5xl mb-4">⟳</div>
      <p class="text-lg text-gray-600 dark:text-gray-400">加载中...</p>
    </div>

    <div v-else-if="error" class="text-center py-16 space-y-4" v-motion-fade>
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 dark:bg-red-900/20 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p class="text-red-500 text-lg">{{ error }}</p>
      <button @click="fetchConfigs" class="btn-primary mt-4 px-6">
        重试
      </button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="(config, index) in configs" 
        :key="config.key" 
        class="card group hover:scale-105 hover:shadow-xl transition-all duration-300"
        v-motion-slide-visible-once-bottom
        :delay="index * 50"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">
              {{ config.description }}
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              键名：{{ config.key }}
            </p>
          </div>
          <button 
            v-if="isAdmin" 
            @click="editConfig(config)" 
            class="p-2 rounded-full bg-gray-100 text-primary hover:bg-primary/10 hover:text-primary-dark transition-colors duration-200 dark:bg-gray-700"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
        </div>

        <div class="mt-5">
          <div v-if="config.type === 'color'" class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-full border shadow-inner" :style="{ backgroundColor: config.value }"></div>
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ config.value }}</span>
          </div>
          <div v-else-if="config.type === 'image'" class="mt-3">
            <div class="relative group overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700">
              <img :src="config.value" :alt="config.description" class="w-full h-36 object-cover transition-transform duration-300 group-hover:scale-110" />
              <div class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <a :href="config.value" target="_blank" class="text-white hover:underline font-medium">查看原图</a>
              </div>
            </div>
          </div>
          <div v-else class="text-sm text-gray-600 dark:text-gray-400 break-all p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div v-if="config.visible == true" class="font-mono">
              {{ config.value }}
            </div>
            <div v-else class="font-mono">
              {{ translateConfig(config.value) }}
            </div>
          </div>
        </div>

        <div class="mt-4 text-xs text-gray-500 dark:text-gray-400 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          最后更新：{{ formatDate(config.updated_at) }}
        </div>
      </div>
    </div>

    <!-- 添加/编辑配置模态框 -->
    <div v-if="showAddModal || showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div 
        class="bg-white dark:bg-gray-800 rounded-xl max-w-lg w-full p-6 shadow-xl"
        v-motion-pop
      >
        <h3 class="text-xl font-bold gradient-heading mb-6">
          {{ showEditModal ? '编辑配置' : '添加配置' }}
        </h3>
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div v-if="!showEditModal">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">配置键名</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
              </div>
              <input v-model="form.key" type="text" class="input pl-10" required placeholder="配置的唯一键名" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">描述</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                </svg>
              </div>
              <input v-model="form.description" type="text" class="input pl-10" required placeholder="配置的描述信息" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">类型</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
              </div>
              <select v-model="form.type" class="input pl-10" required>
                <option value="text">文本</option>
                <option value="color">颜色</option>
                <option value="image">图片</option>
              </select>
            </div>
          </div>

          <!-- 有些内容不可见 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">值</label>
            <div v-if="form.type === 'color'">
              <input v-model="form.value" type="color" class="w-full h-12 rounded-md cursor-pointer" required />
            </div>
            <div v-else class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <input v-model="form.value" :type="form.type === 'image' ? 'url' : 'text'" class="input pl-10"
                required :placeholder="form.type === 'image' ? '图片URL地址' : '配置值'" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">是否隐藏该字段</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <select v-model="form.visible" class="input pl-10" required>
                <option value="false">隐藏</option>
                <option value="true">显示</option>
              </select>
            </div>
          </div>

          <div class="flex justify-end space-x-3 mt-8">
            <button 
              type="button" 
              class="inline-flex items-center px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 font-medium rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors duration-200" 
              @click="closeModal"
            >
              取消
            </button>
            <button 
              type="submit" 
              class="inline-flex items-center px-6 py-2 bg-gradient-to-r from-primary to-primary-light text-white font-medium rounded-md shadow-sm hover:shadow-md transition-all duration-200" 
              :disabled="submitting"
            >
              <span v-if="submitting" class="animate-spin mr-2 text-xl">⟳</span>
              {{ submitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const isAdmin = ref(true)

const configs = ref([])
const loading = ref(false)
const error = ref(null)
const showAddModal = ref(false)
const showEditModal = ref(false)
const submitting = ref(false)

const form = ref({
  key: '',
  value: '',
  description: '',
  type: 'text',
  visible: true
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchConfigs = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await axios.get('/api/configs')
    configs.value = response.data
  } catch (err) {
    error.value = '加载配置失败，请重试'
    console.error('Error fetching configs:', err)
  } finally {
    loading.value = false
  }
}

const editConfig = (config) => {
  form.value = { 
    ...config,
    visible: config.visible.toString()
  }
  showEditModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  form.value = {
    key: '',
    value: '',
    description: '',
    type: 'text',
    visible: 'true'
  }
}

const handleSubmit = async () => {
  submitting.value = true

  try {
    const formData = new FormData()
    formData.append('value', form.value.value)
    formData.append('description', form.value.description)
    formData.append('type', form.value.type)
    formData.append('visible', form.value.visible === 'true')
    if (showEditModal.value) {
      await axios.put(`/api/configs/${form.value.key}`, formData)
    } else {
      formData.append('key', form.value.key)
      await axios.post('/api/configs', formData)
    }

    await fetchConfigs()
    closeModal()
  } catch (err) {
    error.value = '保存失败，请重试'
    console.error('Error saving config:', err)
  } finally {
    submitting.value = false
  }
}

const translateConfig = (value) => {
  // 如果是数字格式，使用特定的掩码格式
  if (/^\d{11,}$/.test(value)) {
    return value.replace(/^(\d{3})(\d+)(\d{4})$/, '$1****$3')
  }
  
  // 其他类型的值，只显示开头和结尾的少量字符
  const length = value.length
  if (length <= 8) {
    return '********'
  }
  
  // 对于较长的字符串，只显示前后各4个字符
  return value.slice(0, 4) + '********' + value.slice(-4)
}

onMounted(() => {
  fetchConfigs()
})
</script>