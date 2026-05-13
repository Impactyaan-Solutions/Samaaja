<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { 
  ChevronDown, 
  Leaf, 
  Droplets, 
  BookOpen, 
  Settings, 
  LogOut 
} from 'lucide-vue-next'
import AppHeader from '@/components/common/AppHeader.vue'
import { authState } from '@/auth'
import { getProfile } from '@/services/api'

const { t } = useI18n()

// --- Menu Logic ---
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const handleLogout = () => {
  console.log("Logging out...")
  isMenuOpen.value = false
}

const goToSettings = () => {
  console.log("Navigating to settings...")
  isMenuOpen.value = false
}

// --- User Logic ---
const route = useRoute()
const externalProfile = ref(null)
const isExternalLoading = ref(false)

const loadExternalProfile = async (email) => {
  isExternalLoading.value = true
  try {
    const data = await getProfile(email)
    externalProfile.value = data
  } catch (err) {
    console.error("Failed to load user profile", err)
    externalProfile.value = null
  } finally {
    isExternalLoading.value = false
  }
}

onMounted(() => {
  if (route.query.user_email) {
    loadExternalProfile(route.query.user_email)
  }
})

watch(() => route.query.user_email, (newEmail) => {
  if (newEmail) {
    loadExternalProfile(newEmail)
  } else {
    externalProfile.value = null
  }
})

const user = computed(() => {
  if (externalProfile.value) {
    const p = externalProfile.value
    return {
      name: p.full_name,
      role: p.user_category,
      bio: p.bio,
      image: p.user_image,
      stats: {
        actions: p.action_count || 0,
        issuesResolved: p.issues_reported || 0,
        posts: p.posts || 0,
        hours: p.hours_invested || 0
      },
      interests: p.interests,
      badges: p.badges
    }
  }

  return {
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
    interests: authState.profile.interests,
    badges: authState.profile.badges
  }
})

const isLoading = computed(() => authState.isInitialLoad || isExternalLoading.value)
</script>

<template>
  <div v-if="!isLoading" class="min-h-full bg-gray-50/50 pb-6 relative">
    
    <AppHeader @menuClick="toggleMenu" />

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
          <button 
            @click="goToSettings" 
            class="flex items-center space-x-3 px-4 py-3 hover:bg-gray-50 text-gray-700 transition-colors"
          >
            <Settings class="w-4 h-4 text-gray-500" />
            <span class="text-sm font-medium">{{ t('profile.settings') }}</span>
          </button>
          
          <div class="border-t border-gray-100 mx-2"></div>
          
          <button 
            @click="handleLogout" 
            class="flex items-center space-x-3 px-4 py-3 hover:bg-red-50 text-red-600 transition-colors"
          >
            <LogOut class="w-4 h-4" />
            <span class="text-sm font-medium">{{ t('profile.logout') }}</span>
          </button>
        </div>
      </div>
    </transition>

    <div v-if="isMenuOpen" @click="isMenuOpen = false" class="fixed inset-0 z-40"></div>

    <div class="px-5 pb-2 rounded-2xl shadow-sm mb-5">
      <div class="flex flex-col items-center p-2 px-4 text-center">
        <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 border-4 border-white shadow-lg mb-4">
          <img v-if="user.image" :src="user.image" class="w-full h-full object-cover" @error="user.image = null" />
          <svg v-else viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="60" cy="60" r="60" fill="#EEF2FF"/>
            <circle cx="60" cy="60" r="52" fill="#E0E7FF"/>
            <circle cx="60" cy="42" r="20" fill="#6366F1"/>
            <path d="M30 98C30 80.3269 43.3269 67 61 67C78.6731 67 92 80.3269 92 98V120H30V98Z" fill="#6366F1"/>
            <circle cx="52" cy="36" r="4" fill="#A5B4FC" fill-opacity="0.7"/>
          </svg>
        </div>
        
        <h1 class="text-2xl font-bold text-gray-900">{{ user.name }}</h1>
        <p class="text-blue-600 font-semibold text-sm mt-1">{{ user.role }}</p>
        
        <p v-if="user.bio" class="text-gray-500 italic text-sm mt-4 px-2 tracking-wide leading-relaxed">
          {{ user.bio }}
        </p>

        <div class="flex items-center space-x-3 mt-6">
          <div v-for="(interest, index) in user.interests" :key="index" class="bg-blue-50/80 px-4 py-2 rounded-2xl flex flex-col items-center shadow-sm border border-blue-100/50">
            <img :src="interest.icon" class="w-8 h-8 mb-1 rounded-full"/>
            <span class="text-[11px] font-bold text-gray-700">{{ interest.action_category?.trim() }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="px-5 mb-5">
      <div class="flex items-center space-x-2 mb-4">
        <span class="text-xl">🌟</span>
        <h3 class="font-bold text-gray-900 text-lg">{{ t('profile.impact_summary') }}</h3>
      </div>
      
      <div class="grid grid-cols-3 gap-3">
        <div class="bg-white border border-gray-100 rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.actions }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ t('profile.actions') }}</span>
        </div>
        <div class="bg-white border border-gray-100 rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.hours }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ t('profile.hours') }}</span>
        </div>
        <div class="bg-white border border-gray-100 rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-blue-600 mb-1">{{ user.stats.posts }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ t('profile.posts') }}</span>
        </div>
      </div>
    </div>

    <div class="px-5 mb-20">
      <div class="flex items-center space-x-2 mb-4">
        <span class="text-xl">🥇</span>
        <h3 class="font-bold text-gray-900 text-lg">{{ t('profile.badges_earned') }}</h3>
      </div>
      <div v-if="user.badges && user.badges.length > 0" class="grid grid-cols-3 gap-3">
        <div v-for="(badge, index) in user.badges" :key="index" class="flex flex-col justify-center items-center text-center">
          <img :src="badge.badge_icon" class="w-8 h-8 mb-1 rounded-full"/>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">{{ badge.badge_name }}</span>
        </div>
      </div>
      <div v-else class="bg-white border border-gray-100 p-6 rounded-2xl shadow-sm italic text-gray-400 text-sm text-center">
        {{ t('profile.no_badges') }}
      </div>
    </div>
  </div>

  <div v-else class="h-screen flex items-center justify-center bg-white">
    <div class="flex flex-col items-center space-y-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="text-gray-500 font-medium tracking-wide">{{ t('profile.syncing') }}</p>
    </div>
  </div>
</template>