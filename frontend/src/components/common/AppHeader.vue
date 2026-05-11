<script setup>
import { Menu } from 'lucide-vue-next'
import { authState } from '@/auth'

defineProps({
  title: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <header class="bg-white px-5 py-4 flex items-center justify-between sticky top-0 z-20 shadow-sm border-b border-gray-100 mb-1">
    <slot name="left">
      <template v-if="title">
        <h2 class="font-bold text-gray-900 text-xl">{{ title }}</h2>
      </template>
      <template v-else>
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold overflow-hidden">
            <img v-if="authState.profile.imageBase64 || authState.profile.image" :src="authState.profile.imageBase64 || authState.profile.image" class="w-full h-full object-cover" />
            <span v-else>{{ authState.profile.fullName ? authState.profile.fullName.charAt(0) : '?' }}</span>
          </div>
          <div>
            <h2 class="font-bold text-gray-900 text-[15px]">{{ authState.profile.fullName || 'Loading...' }}</h2>
            <p class="text-[11px] text-gray-500">{{ authState.profile.category || 'Volunteer' }}</p>
          </div>
        </div>
      </template>
    </slot>
    
    <slot name="right">
      <button class="w-9 h-9 bg-gray-50 rounded-full flex items-center justify-center hover:bg-gray-100">
        <Menu class="w-5 h-5 text-gray-600" />
      </button>
    </slot>
  </header>
</template>
