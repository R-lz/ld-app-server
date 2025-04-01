<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div class="text-center mb-10" v-motion-slide-visible-once-top>
      <h2 class="text-3xl font-bold gradient-heading mb-3">
        上传新版本
      </h2>
      <p class="text-lg text-gray-600 dark:text-gray-400">
        上传应用的新版本，支持Android和iOS平台
      </p>
    </div>

    <form @submit.prevent="handleSubmit" class="card space-y-7" v-motion-slide-visible-once-bottom>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div>
          <label for="platform" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">平台</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg v-if="form.platform === 'Android'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 16V7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"></path>
                <line x1="12" y1="17" x2="12" y2="19"></line>
                <path d="M8 2l8 0"></path>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 21a9 9 0 0 1-9-9 9 9 0 0 1 9-9 9 9 0 0 1 9 9 9 9 0 0 1-9 9z"></path>
                <path d="M12 7v4l1.5 2.5"></path>
              </svg>
            </div>
            <select id="platform" v-model="form.platform" required class="input pl-10">
              <option value="Android">安卓</option>
              <option value="iOS">苹果</option>
            </select>
          </div>
        </div>

        <div>
          <label for="version" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">版本号</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
              </svg>
            </div>
            <input id="version" v-model="form.version" type="text" required placeholder="例如：1.0.0" class="input pl-10" />
          </div>
        </div>

        <div>
          <label for="version_code" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">版本代码</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <input id="version_code" v-model.number="form.version_code" type="number" required placeholder="例如：100" class="input pl-10" />
          </div>
        </div>

        <div>
          <label for="is_force_update" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">更新类型</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="form.is_force_update" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <select id="is_force_update" v-model="form.is_force_update" required class="input pl-10">
              <option :value="false">可选更新</option>
              <option :value="true">强制更新</option>
            </select>
          </div>
        </div>
      </div>

      <div>
        <label for="release_notes" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">发布说明</label>
        <div class="relative">
          <div class="absolute top-3 left-3 flex items-start pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <textarea 
            id="release_notes" 
            v-model="form.release_notes" 
            rows="4" 
            required 
            placeholder="这个版本有哪些新功能或改进？" 
            class="input pl-10"
          ></textarea>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">应用文件</label>
        <div 
          class="mt-1 flex flex-col justify-center items-center px-6 pt-5 pb-6 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-lg bg-gray-50 dark:bg-gray-800 transition-all duration-200"
          :class="{ 'border-primary bg-primary/5 dark:border-primary dark:bg-primary/10': isDragging }" 
          @dragenter.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false" 
          @dragover.prevent 
          @drop.prevent="handleFileDrop"
        >
          <div class="space-y-3 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 24 24" class="text-primary-light dark:text-primary mx-auto transition-transform duration-300" :class="{'scale-110': isDragging}">
              <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5">
                <path d="M4 15V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2H4" opacity="0.2" />
                <path d="M14 2v4.5a1 1 0 0 0 1 1h4.5M4 15h2m0 0l2-2m-2 2l2 2m-4-9h8" />
                <path d="M14 11h4m-2-2v4M4 19h2m0 0l2-2m-2 2l2 2" />
              </g>
            </svg>
            <div class="flex flex-col sm:flex-row text-sm text-gray-600 dark:text-gray-400 justify-center">
              <label for="file-upload"
                class="relative cursor-pointer rounded-md font-medium text-primary hover:text-primary-dark focus-within:outline-none px-3 py-1.5 border border-primary/30 hover:border-primary transition-colors duration-200 mx-auto sm:mx-2 mb-2 sm:mb-0">
                <span>选择文件</span>
                <input id="file-upload" type="file" class="sr-only" @change="handleFileSelect"
                  :accept="form.platform === 'Android' ? '.apk' : '.ipa'" />
              </label>
              <p class="pl-1 flex items-center">或拖拽文件到此处</p>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ form.platform === 'Android' ? 'APK' : 'IPA' }} 文件大小不超过 500MB
            </p>
          </div>
        </div>
        <div v-if="form.file" class="mt-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-sm text-gray-700 dark:text-gray-300">已选择文件：{{ form.file.name }}</span>
        </div>
      </div>

      <div v-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 dark:bg-red-900/20 dark:border-red-500">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-500">{{ error }}</p>
          </div>
        </div>
      </div>

      <div class="flex justify-end space-x-4 pt-2">
        <router-link to="/versions" class="inline-flex items-center px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 font-medium rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors duration-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          取消
        </router-link>
        <button 
          type="submit" 
          class="inline-flex items-center px-6 py-2 bg-gradient-to-r from-primary to-primary-light text-white font-medium rounded-md shadow-sm hover:shadow-md transition-all duration-200" 
          :disabled="loading"
        >
          <span v-if="loading" class="animate-spin mr-2 text-xl">⟳</span>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          {{ loading ? '上传中...' : '上传版本' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const isDragging = ref(false)

const form = reactive({
  platform: 'Android',
  version: '',
  version_code: null,
  is_force_update: false,
  release_notes: '',
  file: null
})

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const handleFileDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const validateAndSetFile = (file) => {
  const extension = file.name.split('.').pop().toLowerCase()
  const isValidExtension = form.platform === 'Android'
    ? extension === 'apk'
    : extension === 'ipa'

  if (!isValidExtension) {
    error.value = `请上传有效的 ${form.platform === 'Android' ? 'APK' : 'IPA'} 文件`
    return
  }

  if (file.size > 500 * 1024 * 1024) { // 500MB
    error.value = '文件大小必须小于500MB'
    return
  }

  form.file = file
  error.value = ''
}

const handleSubmit = async () => {
  if (!form.file) {
    error.value = '请选择要上传的文件'
    return
  }

  loading.value = true
  error.value = ''

  const formData = new FormData()
  formData.append('platform', form.platform)
  formData.append('version', form.version)
  formData.append('version_code', form.version_code)
  formData.append('is_force_update', form.is_force_update)
  formData.append('release_notes', form.release_notes)
  formData.append('app_file', form.file)

  try {
    const token = localStorage.getItem('token')
    await axios.post('/api/version/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
      }
    })
    router.push('/versions')
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = '请先登录后再上传版本'
      router.push('/login')
    } else {
      error.value = err.response?.data?.message || '上传版本失败，请重试'
    }
    console.error('Error uploading version:', err)
  } finally {
    loading.value = false
  }
}
</script>