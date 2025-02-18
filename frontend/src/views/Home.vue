<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center">
      <h1 class="text-4xl font-bold bg-gradient-to-r from-primary to-primary-light text-transparent bg-clip-text">
        应用版本管理系统
      </h1>
      <p class="mt-4 text-xl text-gray-600">
        轻松管理和分发您的移动应用版本
      </p>
    </div>

    <div class="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Version Management Card -->
      <div
        class="card hover:shadow-lg transition-shadow"
        v-motion-slide-visible-bottom
      >
        <div class="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
          <svg class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900">版本管理</h3>
        <p class="mt-2 text-gray-600">
          跟踪所有应用版本，包括发布说明和更新要求
        </p>
        <div v-if="!authStore.isAuthenticated" class="mt-4 text-sm text-red-500">
          请先登录以访问此功能
        </div>
        <router-link
          :to="authStore.isAuthenticated ? '/versions' : '/login'"
          class="btn-primary mt-4 inline-block"
        >
          {{ authStore.isAuthenticated ? '查看版本' : '登录' }}
        </router-link>
      </div>

      <!-- Upload Card -->
      <div
        class="card hover:shadow-lg transition-shadow"
        v-motion-slide-visible-bottom
        :delay="100"
      >
        <div class="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
          <svg class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900">上传新版本</h3>
        <p class="mt-2 text-gray-600">
          使用简单的拖放界面上传新版本应用
        </p>
        <div v-if="!authStore.isAuthenticated" class="mt-4 text-sm text-red-500">
          请先登录以访问此功能
        </div>
        <router-link
          :to="authStore.isAuthenticated ? '/upload' : '/login'"
          class="btn-primary mt-4 inline-block"
        >
          {{ authStore.isAuthenticated ? '上传版本' : '登录' }}
        </router-link>
      </div>

      <!-- Platform Support Card -->
      <div
        class="card hover:shadow-lg transition-shadow"
        v-motion-slide-visible-bottom
        :delay="200"
      >
        <div class="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
          <svg class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900">多平台支持</h3>
        <p class="mt-2 text-gray-600">
          同时支持 Android (APK) 和 iOS (IPA) 应用
        </p>
        <div v-if="!authStore.isAuthenticated" class="mt-4 text-sm text-red-500">
          请先登录以访问此功能
        </div>
        <router-link
          :to="authStore.isAuthenticated ? '/versions' : '/login'"
          class="btn-primary mt-4 inline-block"
        >
          {{ authStore.isAuthenticated ? '浏览平台' : '登录' }}
        </router-link>
      </div>
    </div>

    <div class="mt-16 text-center" v-if="!authStore.isAuthenticated">
      <p class="text-gray-600 mb-4">
        准备开始使用？请登录以访问所有功能
      </p>
      <router-link
        to="/login"
        class="btn-primary"
      >
        登录
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script> 