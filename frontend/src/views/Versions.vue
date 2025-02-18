<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-900">应用版本列表</h2>
      <router-link to="/upload" class="btn-primary">
        上传新版本
      </router-link>
    </div>

    <div class="flex space-x-4 mb-6">
      <button
        v-for="platform in platforms"
        :key="platform"
        @click="selectedPlatform = platform"
        :class="[
          'btn',
          selectedPlatform === platform
            ? 'btn-primary'
            : 'btn-secondary'
        ]"
      >
        {{ platform }}
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin text-primary text-4xl">⟳</div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-500">{{ error }}</p>
      <button @click="fetchVersions" class="btn-primary mt-4">
        重试
      </button>
    </div>

    <div v-else-if="filteredVersions.length === 0" class="text-center py-12">
      <p class="text-gray-500">暂无 {{ selectedPlatform }} 平台的版本</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="version in filteredVersions"
        :key="version.id"
        class="card hover:shadow-lg transition-shadow"
        v-motion-slide-visible-bottom
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              版本 {{ version.version }}
            </h3>
            <p class="text-sm text-gray-500">
              版本代码：{{ version.version_code }}
            </p>
          </div>
          <span
            :class="[
              'px-2 py-1 text-xs font-medium rounded-full',
              version.is_force_update
                ? 'bg-red-100 text-red-800'
                : 'bg-green-100 text-green-800'
            ]"
          >
            {{ version.is_force_update ? '强制更新' : '可选更新' }}
          </span>
        </div>

        <div class="mt-4">
          <h4 class="text-sm font-medium text-gray-900">发布说明：</h4>
          <p class="mt-1 text-gray-600 whitespace-pre-line">{{ version.release_notes }}</p>
        </div>

        <div class="mt-4 flex items-center justify-between">
          <div class="text-sm text-gray-500">
            发布时间：{{ formatDate(version.created_at) }}
          </div>
          <a
            :href="version.download_url"
            class="btn-secondary text-sm"
            target="_blank"
          >
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
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
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
    error.value = 'Failed to load versions. Please try again.'
    console.error('Error fetching versions:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchVersions()
})
</script> 