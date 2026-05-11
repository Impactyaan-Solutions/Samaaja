<script setup>
import { computed } from 'vue'
import { ChevronDown, Leaf, Droplets, BookOpen, Settings } from 'lucide-vue-next'
import AppHeader from '@/components/common/AppHeader.vue'
import { authState } from '@/auth'

const user = computed(() => ({
  name: authState.profile.fullName || 'Loading...',
  role: authState.profile.category || 'Volunteer',
  bio: authState.profile.interests || '', 
  image: authState.profile.imageBase64 || authState.profile.image,
  stats: {
    actions: authState.profile.stats.actions,
    issuesResolved: authState.profile.stats.issuesReported,
    posts: 0 
  }
}))

const isLoading = computed(() => authState.isInitialLoad)
</script>

<template>
  <div v-if="!isLoading" class="min-h-full bg-gray-50/50 pb-6">
    <!-- Header -->
    <AppHeader/>

    <div class="px-5 pb-2 rounded-2xl shadow-sm mb-5">
      <div class="flex flex-col items-center p-2 px-4 text-center">
        <!-- Avatar -->
        <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 border-4 border-white shadow-lg mb-4">
          <img 
            :src="user.image" 
            class="w-full h-full object-cover" 
            onerror="this.src='https://ui-avatars.com/api/?name=fallback_avatar'"
          />
        </div>
        
        <h1 class="text-2xl font-bold text-gray-900">{{ user.name }}</h1>
        <p class="text-blue-600 font-semibold text-sm mt-1">{{ user.role }}</p>
        
        <!-- Bio: Skips rendering entirely if interest/bio is null or empty -->
        <p 
          v-if="user.bio" 
          class="text-gray-500 italic text-sm mt-4 px-2 tracking-wide leading-relaxed"
        >
          {{ user.bio }}
        </p>

        <!-- Tags (Kept static as per design) -->
        <div class="flex items-center space-x-3 mt-6">
          <div class="bg-blue-50/80 px-4 py-2 rounded-2xl flex flex-col items-center shadow-sm border border-blue-100/50">
            <Droplets class="w-5 h-5 text-blue-500 mb-1" />
            <span class="text-[11px] font-bold text-gray-700">Water</span>
          </div>
          <div class="bg-amber-50/80 px-4 py-2 rounded-2xl flex flex-col items-center shadow-sm border border-amber-100/50">
            <Leaf class="w-5 h-5 text-amber-600 mb-1" />
            <span class="text-[11px] font-bold text-gray-700">Cleanliness</span>
          </div>
          <div class="bg-rose-50/80 px-4 py-2 rounded-2xl flex flex-col items-center shadow-sm border border-rose-100/50">
            <BookOpen class="w-5 h-5 text-rose-500 mb-1" />
            <span class="text-[11px] font-bold text-gray-700">Education</span>
          </div>
        </div>

      </div>
    </div>

    <!-- Impact Summary -->
    <div class="px-5 mb-5">
      <div class="flex items-center space-x-2 mb-4">
        <span class="text-xl">🌟</span>
        <h3 class="font-bold text-gray-900 text-lg">Impact Summary</h3>
      </div>
      
      <div class="grid grid-cols-3 gap-3">
        <div class="bg-white border border-gray-100 rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.actions }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">Actions</span>
        </div>
        <div class="bg-white border border-gray-100  rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.issuesResolved }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">Issues Resolved</span>
        </div>
        <div class="bg-white border border-gray-100  rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.posts }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">Posts</span>
        </div>
      </div>
    </div>

    <!-- Badges -->
    <div class="px-5 mb-20">
      <div class="flex items-center space-x-2 mb-4">
        <span class="text-xl">🥇</span>
        <h3 class="font-bold text-gray-900 text-lg">Badges Earned</h3>
      </div>
      <div class="bg-white border border-gray-100 p-6 rounded-2xl shadow-sm italic text-gray-400 text-sm text-center">
        no badges earned
      </div>
    </div>
  </div>

  <!-- Loading State -->
  <div v-else class="h-screen flex items-center justify-center bg-white">
    <div class="flex flex-col items-center space-y-4">
       <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
       <p class="text-gray-500 font-medium tracking-wide">fallback_syncing_status</p>
    </div>
  </div>
</template>