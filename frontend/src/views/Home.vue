<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center" v-motion-slide-visible-once-top>
      <h1 class="text-5xl font-bold gradient-heading mb-4">
        应用管理系统
      </h1>
      <p class="mt-4 text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
        轻松管理移动应用，实现配置热更新，支持多平台多渠道投放
      </p>
      <div class="mt-8 flex justify-center space-x-4">
        <router-link
          to="/versions"
          v-if="authStore.isAuthenticated"
          class="btn-primary"
        >
          开始使用
        </router-link>
        <router-link 
          to="/login" 
          v-else 
          class="btn-primary"
        >
          立即登录
        </router-link>
      </div>
    </div>

    <div class="mt-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Version Management Card -->
      <div
        class="card group hover:scale-105 hover:shadow-xl transition-all duration-300"
        v-motion-slide-visible-once-bottom
      >
        <div class="h-14 w-14 bg-gradient-to-br from-primary/20 to-primary/10 dark:from-primary/30 dark:to-primary/20 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-gradient-to-br group-hover:from-primary/30 group-hover:to-primary/20 transition-all duration-300">
          <svg class="h-7 w-7 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">版本管理</h3>
        <p class="mt-3 text-gray-600 dark:text-gray-400">
          跟踪所有应用版本，包括发布说明和更新要求，支持一键回滚
        </p>
        <div v-if="!authStore.isAuthenticated" class="mt-4 text-sm text-red-500">
          请先登录以访问此功能
        </div>
        <router-link
          :to="authStore.isAuthenticated ? '/versions' : '/login'"
          class="mt-6 inline-flex items-center text-primary hover:text-primary-dark group-hover:translate-x-1 transition-all duration-300"
        >
          <span>{{ authStore.isAuthenticated ? '查看版本' : '登录' }}</span>
          <svg class="ml-1 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>

      <!-- Upload Card -->
      <div
        class="card group hover:scale-105 hover:shadow-xl transition-all duration-300"
        v-motion-slide-visible-once-bottom
        :delay="100"
      >
        <div class="h-14 w-14 bg-gradient-to-br from-primary/20 to-primary/10 dark:from-primary/30 dark:to-primary/20 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-gradient-to-br group-hover:from-primary/30 group-hover:to-primary/20 transition-all duration-300">
          <svg class="h-7 w-7 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">上传新版本</h3>
        <p class="mt-3 text-gray-600 dark:text-gray-400">
          简单的拖放界面，支持批量上传，自动识别包信息和签名验证
        </p>
        <div v-if="!authStore.isAuthenticated" class="mt-4 text-sm text-red-500">
          请先登录以访问此功能
        </div>
        <router-link
          :to="authStore.isAuthenticated ? '/upload' : '/login'"
          class="mt-6 inline-flex items-center text-primary hover:text-primary-dark group-hover:translate-x-1 transition-all duration-300"
        >
          <span>{{ authStore.isAuthenticated ? '上传版本' : '登录' }}</span>
          <svg class="ml-1 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>

      <!-- Config Management Card -->
      <div
        class="card group hover:scale-105 hover:shadow-xl transition-all duration-300"
        v-motion-slide-visible-once-bottom
        :delay="200"
      >
        <div class="h-14 w-14 bg-gradient-to-br from-primary/20 to-primary/10 dark:from-primary/30 dark:to-primary/20 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-gradient-to-br group-hover:from-primary/30 group-hover:to-primary/20 transition-all duration-300">
          <svg class="h-7 w-7 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">配置管理</h3>
        <p class="mt-3 text-gray-600 dark:text-gray-400">
          管理应用的秘钥、域名、主题色等配置，支持多环境配置与A/B测试
        </p>
        <div v-if="!authStore.isAuthenticated" class="mt-4 text-sm text-red-500">
          请先登录以访问此功能
        </div>
        <router-link
          :to="authStore.isAuthenticated ? '/configs' : '/login'"
          class="mt-6 inline-flex items-center text-primary hover:text-primary-dark group-hover:translate-x-1 transition-all duration-300"
        >
          <span>{{ authStore.isAuthenticated ? '管理配置' : '登录' }}</span>
          <svg class="ml-1 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
    </div>

    <div class="mt-20 text-center" v-if="!authStore.isAuthenticated" v-motion-slide-visible-once-bottom>
      <p class="text-gray-600 dark:text-gray-400 mb-6 text-lg">
        准备开始使用？请登录以访问所有功能
      </p>
      <router-link
        to="/login"
        class="btn-primary px-8 py-3 text-lg"
      >
        立即登录
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script> 