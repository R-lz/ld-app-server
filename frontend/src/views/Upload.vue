<template>
  <div class="max-w-3xl mx-auto">
    <div class="text-center mb-8">
      <h2 class="text-3xl font-bold bg-gradient-to-r from-primary to-primary-light text-transparent bg-clip-text">
        上传新版本
      </h2>
      <p class="mt-2 text-gray-600">
        上传应用的新版本
      </p>
    </div>

    <form @submit.prevent="handleSubmit" class="card space-y-6">
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="platform" class="block text-sm font-medium text-gray-700">平台</label>
          <select id="platform" v-model="form.platform" required class="input mt-1">
            <option value="Android">安卓</option>
            <option value="iOS">苹果</option>
          </select>
        </div>

        <div>
          <label for="version" class="block text-sm font-medium text-gray-700">版本号</label>
          <input id="version" v-model="form.version" type="text" required placeholder="例如：1.0.0" class="input mt-1" />
        </div>

        <div>
          <label for="version_code" class="block text-sm font-medium text-gray-700">版本代码</label>
          <input id="version_code" v-model.number="form.version_code" type="number" required placeholder="例如：100"
            class="input mt-1" />
        </div>

        <div>
          <label for="is_force_update" class="block text-sm font-medium text-gray-700">更新类型</label>
          <select id="is_force_update" v-model="form.is_force_update" required class="input mt-1">
            <option :value="false">可选更新</option>
            <option :value="true">强制更新</option>
          </select>
        </div>
      </div>

      <div>
        <label for="release_notes" class="block text-sm font-medium text-gray-700">发布说明</label>
        <textarea id="release_notes" v-model="form.release_notes" rows="4" required placeholder="这个版本有哪些新功能或改进？"
          class="input mt-1"></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">应用文件</label>
        <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md"
          :class="{ 'border-primary': isDragging }" @dragenter.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false" @dragover.prevent @drop.prevent="handleFileDrop">
          <div class="space-y-1 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
              <path fill="currentColor" fill-rule="evenodd"
                d="M12 2v6.5a1.5 1.5 0 0 0 1.5 1.5H20v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"
                class="duoicon-secondary-layer" opacity=".3" />
              <path fill="currentColor" fill-rule="evenodd"
                d="M14 2.043c.379.08.726.269 1 .543L19.414 7c.274.274.463.621.543 1H14zm-2.346 9.656l-.894 1.535l-1.737.376a.4.4 0 0 0-.213.658l1.184 1.325l-.18 1.768a.4.4 0 0 0 .56.406L12 17.051l1.626.716a.4.4 0 0 0 .56-.406l-.18-1.768l1.184-1.325a.4.4 0 0 0-.213-.658l-1.737-.376l-.894-1.535a.4.4 0 0 0-.692 0"
                class="duoicon-primary-layer" />
            </svg>
            <div class="flex text-sm text-gray-600">
              <label for="file-upload"
                class="relative cursor-pointer rounded-md font-medium text-primary hover:text-primary-dark focus-within:outline-none">
                <span>选择文件</span>
                <input id="file-upload" type="file" class="sr-only" @change="handleFileSelect"
                  :accept="form.platform === 'Android' ? '.apk' : '.ipa'" />
              </label>
              <p class="pl-1">或拖拽文件到此处</p>
            </div>
            <p class="text-xs text-gray-500">
              {{ form.platform === 'Android' ? 'APK' : 'IPA' }} 文件大小不超过 500MB
            </p>
          </div>
        </div>
        <div v-if="form.file" class="mt-2 text-sm text-gray-500">
          已选择文件：{{ form.file.name }}
        </div>
      </div>

      <div v-if="error" class="text-red-500 text-sm">
        {{ error }}
      </div>

      <div class="flex justify-end">
        <router-link to="/versions" class="btn-secondary mr-4">
          取消
        </router-link>
        <button type="submit" class="btn-primary" :disabled="loading">
          <span v-if="loading" class="animate-spin mr-2">⟳</span>
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
    error.value = `Please upload a valid ${form.platform === 'Android' ? 'APK' : 'IPA'} file`
    return
  }

  if (file.size > 500 * 1024 * 1024) { // 500MB
    error.value = 'File size must be less than 500MB'
    return
  }

  form.file = file
  error.value = ''
}

const handleSubmit = async () => {
  if (!form.file) {
    error.value = 'Please select a file to upload'
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
      error.value = err.response?.data?.message || 'Failed to upload version. Please try again.'
    }
    console.error('Error uploading version:', err)
  } finally {
    loading.value = false
  }
}
</script>