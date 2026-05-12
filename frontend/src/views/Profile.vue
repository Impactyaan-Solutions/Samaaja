<script setup>
import { ref, computed } from 'vue'
import { 
  ChevronDown, 
  Leaf, 
  Droplets, 
  BookOpen, 
  Settings, 
  LogOut // Added for the menu
} from 'lucide-vue-next'
import AppHeader from '@/components/common/AppHeader.vue'
import { authState } from '@/auth'

// --- Menu Logic ---
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const handleLogout = () => {
  // Replace with your actual logout logic (e.g., authState.logout())
  console.log("Logging out...")
  isMenuOpen.value = false
}

const goToSettings = () => {
  // Replace with your navigation logic (e.g., router.push('/settings'))
  console.log("Navigating to settings...")
  isMenuOpen.value = false
}

// --- Original User Logic ---
const user = computed(() => ({
  name: authState.profile.fullName,
  role: authState.profile.category,
  bio: authState.profile.bio, 
  image: authState.profile.imageBase64 || authState.profile.image,
  stats: {
    actions: authState.profile.stats.actions,
    issuesResolved: authState.profile.stats.issuesReported || 0,
    posts: authState.profile.stats.posts || 0,
    hours: authState.profile.stats.hours || 0
  },
  interests:authState.profile.interests,
  badges:authState.profile.badges
}))

const isLoading = computed(() => authState.isInitialLoad)
</script>

<template>
  <div v-if="!isLoading" class="min-h-full bg-gray-50/50 pb-6 relative">
    
    <!-- Header: Now listening for the @menuClick event -->
    <AppHeader @menuClick="toggleMenu" />

    <!-- Dropdown Menu -->
    <transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div 
        v-if="isMenuOpen" 
        class="absolute right-5 top-16 w-48 bg-white rounded-2xl shadow-xl border border-gray-100 z-50 overflow-hidden"
      >
        <div class="flex flex-col py-1">
          <!-- Settings Tab -->
          <button 
            @click="goToSettings" 
            class="flex items-center space-x-3 px-4 py-3 hover:bg-gray-50 text-gray-700 transition-colors"
          >
            <Settings class="w-4 h-4 text-gray-500" />
            <span class="text-sm font-medium">Settings</span>
          </button>
          
          <div class="border-t border-gray-100 mx-2"></div>
          
          <!-- Logout Tab -->
          <button 
            @click="handleLogout" 
            class="flex items-center space-x-3 px-4 py-3 hover:bg-red-50 text-red-600 transition-colors"
          >
            <LogOut class="w-4 h-4" />
            <span class="text-sm font-medium">Logout</span>
          </button>
        </div>
      </div>
    </transition>

    <!-- Invisible Backdrop: Closes menu when clicking anywhere else -->
    <div 
      v-if="isMenuOpen" 
      @click="isMenuOpen = false" 
      class="fixed inset-0 z-40"
    ></div>

    <!-- Original Profile Content -->
    <div class="px-5 pb-2 rounded-2xl shadow-sm mb-5">
      <div class="flex flex-col items-center p-2 px-4 text-center">
        <!-- Avatar -->
        <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 border-4 border-white shadow-lg mb-4">

          <!-- User Image -->
          <img 
            v-if="user.image"
            :src="user.image" 
            class="w-full h-full object-cover"
            @error="user.image = null"
          />

          <!-- Fallback SVG -->
          <svg
          v-else
          viewBox="0 0 120 120"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <!-- Background -->
          <circle cx="60" cy="60" r="60" fill="#EEF2FF"/>

          <!-- Decorative Circle -->
          <circle cx="60" cy="60" r="52" fill="#E0E7FF"/>

          <!-- Head -->
          <circle cx="60" cy="42" r="20" fill="#6366F1"/>

          <!-- Body -->
          <path
            d="M30 98C30 80.3269 43.3269 67 61 67C78.6731 67 92 80.3269 92 98V120H30V98Z"
            fill="#6366F1"
          />

          <!-- Shine -->
          <circle cx="52" cy="36" r="4" fill="#A5B4FC" fill-opacity="0.7"/>
        </svg>

        </div>
        
        <h1 class="text-2xl font-bold text-gray-900">{{ user.name }}</h1>
        <p class="text-blue-600 font-semibold text-sm mt-1">{{ user.role }}</p>
        
        <p 
          v-if="user.bio" 
          class="text-gray-500 italic text-sm mt-4 px-2 tracking-wide leading-relaxed"
        >
          {{ user.bio }}
        </p>

        <!-- Tags -->
        <div class="flex items-center space-x-3 mt-6">
          <!-- Render interests -->
          <div 
            v-for="(interest, index) in user.interests"
            :key="index"
            class="bg-blue-50/80 px-4 py-2 rounded-2xl flex flex-col items-center shadow-sm border border-blue-100/50"
          >
            <img :src="interest.icon" class="w-8 h-8 mb-1 rounded-full"/>
            <span class="text-[11px] font-bold text-gray-700">{{ interest.action_category?.trim() }}</span>
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
          <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.hours }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">Hours</span>
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
      <div v-if="user.badges" class="grid grid-cols-3 gap-3">
        <div v-for="(badge, index) in user.badges" :key="index" class="flex flex-col justify-center items-center text-center">
          <img :src="badge.badge_icon" class="w-8 h-8 mb-1 rounded-full"/>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ badge.badge_name }}</span>
        </div>
      </div>
      <div v-else class="bg-white border border-gray-100 p-6 rounded-2xl shadow-sm italic text-gray-400 text-sm text-center">
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