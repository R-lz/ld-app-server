<template>
  <div class="app-container">
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style>
:root {
  --color-primary: 34 197 94;
  --color-primary-light: 74 222 128;
  --color-primary-dark: 22 163 74;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

.app-container {
  @apply min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200;
}

/* 全局暗黑模式样式 */
.btn-primary {
  @apply bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-md shadow-sm transition-colors duration-200 
  dark:bg-green-600 dark:hover:bg-green-700;
}

.btn-secondary {
  @apply bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-md shadow-sm transition-colors duration-200
  dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-200;
}

.input {
  @apply w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50 transition-colors duration-200
  dark:bg-gray-800 dark:border-gray-600 dark:text-gray-200 dark:focus:border-green-500;
}

.card {
  @apply bg-white rounded-lg shadow-md p-6 transition-colors duration-200
  dark:bg-gray-800 dark:text-gray-200;
}
</style>
