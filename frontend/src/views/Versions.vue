<template>
  <div class="space-y-8 max-w-7xl mx-auto px-4 py-6">
    <div class="flex justify-between items-center" v-motion-slide-visible-once-top>
      <h2 class="text-3xl font-bold gradient-heading">应用版本列表</h2>
      <router-link to="/upload" class="inline-flex items-center px-4 py-2 bg-gradient-to-r from-primary to-primary-light text-white font-medium rounded-md shadow-sm hover:shadow-md transition-all duration-200 transform hover:-translate-y-0.5">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        上传新版本
      </router-link>
    </div>

    <div class="flex flex-wrap gap-3 mb-6" v-motion-slide-visible-once-bottom>
      <button
        v-for="platform in platforms"
        :key="platform"
        @click="selectedPlatform = platform"
        :class="[
          selectedPlatform === platform
            ? 'bg-gradient-to-r from-primary to-primary-light text-white shadow-md'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600',
          'px-5 py-2.5 rounded-full font-medium transition-all duration-200 flex items-center'
        ]"
      >
        <svg v-if="platform === 'Android'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 16V7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"></path>
          <line x1="12" y1="17" x2="12" y2="19"></line>
          <path d="M8 2l8 0"></path>
        </svg>
        <svg v-if="platform === 'iOS'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 21a9 9 0 0 1-9-9 9 9 0 0 1 9-9 9 9 0 0 1 9 9 9 9 0 0 1-9 9z"></path>
          <path d="M12 7v4l1.5 2.5"></path>
        </svg>
        {{ platform }}
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
      <button @click="fetchVersions" class="btn-primary mt-4 px-6">
        重试
      </button>
    </div>

    <div v-else-if="filteredVersions.length === 0" class="text-center py-16" v-motion-fade>
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
      </div>
      <p class="text-gray-500 dark:text-gray-400 text-lg">暂无 {{ selectedPlatform }} 平台的版本</p>
      <router-link to="/upload" class="btn-primary mt-6 px-6 inline-flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        上传第一个版本
      </router-link>
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="(version, index) in filteredVersions"
        :key="version.id"
        class="card group hover:scale-105 hover:shadow-xl transition-all duration-300"
        v-motion-slide-visible-once-bottom
        :delay="index * 50"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">
              版本 {{ version.version }}
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              版本代码：{{ version.version_code }}
            </p>
          </div>
          <span
            :class="[
              'px-3 py-1 text-sm font-medium rounded-full flex items-center',
              version.is_force_update
                ? 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
                : 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
            ]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="version.is_force_update" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ version.is_force_update ? '强制更新' : '可选更新' }}
          </span>
        </div>

        <div class="mt-5">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            发布说明：
          </h4>
          <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <p class="text-gray-600 dark:text-gray-300 whitespace-pre-line text-sm">{{ version.release_notes || '未提供发布说明' }}</p>
          </div>
        </div>

        <div class="mt-5 flex items-center justify-between">
          <div class="text-sm text-gray-500 dark:text-gray-400 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            发布时间：{{ formatDate(version.created_at) }}
          </div>
          <a
            :href="version.download_url"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-dark transition-colors duration-200"
            target="_blank"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            下载
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const platforms = ['Android', 'iOS']
const selectedPlatform = ref('Android')
const versions = ref([])
const loading = ref(false)
const error = ref(null)

const filteredVersions = computed(() => {
  return versions.value
    .filter(v => v.platform.toLowerCase() === selectedPlatform.value.toLowerCase())
    .sort((a, b) => b.version_code - a.version_code)
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const fetchVersions = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await axios.get('/api/versions')
    versions.value = response.data
  } catch (err) {
    error.value = '加载版本信息失败，请重试'
    console.error('Error fetching versions:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchVersions()
})
</script> 