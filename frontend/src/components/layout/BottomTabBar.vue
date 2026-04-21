<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Home, BarChart2, Zap, Bell, User } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const emit = defineEmits(['act'])

const tabs = [
  { name: 'Home', path: '/', icon: Home },
  { name: 'Leaderboard', path: '/leaderboard', icon: BarChart2 },
  { name: 'Act', path: null, icon: Zap, isAction: true },
  { name: 'Alerts', path: '/announcements', icon: Bell },
  { name: 'Profile', path: '/profile', icon: User }
]

const go = (tab) => {
  if (tab.isAction) {
    emit('act')
  } else {
    router.push(tab.path)
  }
}

const isActive = (path) => {
  return route.path === path
}
</script>

<template>
  <div class="absolute bottom-0 w-full max-w-md bg-white border-t border-gray-100 flex items-center justify-between px-6 py-3 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-40 pb-6 pt-3 rounded-t-3xl border-x mx-auto right-0 left-0">
    <button 
      v-for="tab in tabs" :key="tab.name"
      @click="go(tab)"
      class="flex flex-col items-center justify-center relative w-14"
    >
      <div v-if="tab.isAction" class="absolute -top-10 w-14 h-14 bg-primary-600 rounded-full flex items-center justify-center text-white shadow-lg shadow-primary-500/40">
        <component :is="tab.icon" class="w-7 h-7 fill-white" />
      </div>
      
      <div class="flex flex-col items-center mt-1" :class="{ 'mt-6': tab.isAction }">
        <component 
          v-if="!tab.isAction"
          :is="tab.icon" 
          class="w-6 h-6 mb-1"
          :class="isActive(tab.path) ? 'text-primary-600' : 'text-gray-400'"
        />
        <span 
          class="text-[10px] font-medium"
          :class="isActive(tab.path) || tab.isAction ? 'text-primary-600' : 'text-gray-400'"
        >
          {{ tab.name }}
        </span>
      </div>
    </button>
  </div>
</template>
