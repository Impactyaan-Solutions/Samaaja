<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { 
  User, Bell, Lock, Globe, Moon, HelpCircle, 
  LogOut, ChevronRight, Check
} from 'lucide-vue-next'
import AppHeader from '@/components/common/AppHeader.vue'
import { getProfile, logout } from '@/services/api.js'

// Initialize router and i18n
const { t, locale } = useI18n()
const router = useRouter()

const isLanguageMenuOpen = ref(false)
const languages = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिन्दी' }
]

const currentLanguageLabel = computed(() => {
  return languages.find(l => l.code === locale.value)?.label || 'English'
})

const changeLanguage = (code) => {
  locale.value = code
  localStorage.setItem('lang', code)
  isLanguageMenuOpen.value = false
}

// Reactive states
const notifications = ref(false)
const darkMode = ref(false)
const isLoading = ref(true)

const user = ref({
  name: '',
  role: 'Volunteer',
  email: '',
  avatar: null
})

const fetchUserProfile = async () => {
  try {
    isLoading.value = true
    const currentUserEmail = localStorage.getItem('user_email') || 'rudransh20septmber@gmail.com'
    const profileData = await getProfile(currentUserEmail)
    
    if (profileData) {
      user.value = {
        name: profileData.full_name,
        email: profileData.email,
        role: profileData.user_category || 'Volunteer' 
      }
    }
  } catch (error) {
    console.error("Profile Load Error:", error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchUserProfile()
})

const handleLogout = async () => {
  try {
    await logout()
  } catch (error) {
    console.error("Logout request failed, proceeding with local cleanup:", error)
  } finally {
    localStorage.removeItem('user_email')
    localStorage.removeItem('token')
    router.push('/login')
  }
}
</script>

<template>
  <div class="min-h-full bg-gray-50/50 pb-10 relative">
    <AppHeader />

    <div class="px-5 mt-8">
      <h3 class="font-bold text-gray-900 mb-4 px-1 text-lg">{{ t('settings.title') }}</h3>
      
      <div class="space-y-3">
        <div class="bg-white border border-gray-100 p-4 rounded-2xl flex items-center justify-between shadow-sm">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-blue-50 text-blue-500 rounded-xl">
              <Bell class="w-5 h-5" />
            </div>
            <div>
              <p class="text-[14px] font-semibold text-gray-800">{{ t('settings.push_notifications') }}</p>
              <p class="text-[11px] text-gray-500">{{ t('settings.push_desc') }}</p>
            </div>
          </div>
          <button 
            @click="notifications = !notifications"
            class="w-11 h-6 rounded-full transition-colors relative"
            :class="notifications ? 'bg-primary-500' : 'bg-gray-200'"
          >
            <div 
              class="absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-transform"
              :class="notifications ? 'translate-x-5' : 'translate-x-0'"
            ></div>
          </button>
        </div>

        <div class="relative">
          <button 
            @click="isLanguageMenuOpen = !isLanguageMenuOpen"
            class="w-full bg-white border border-gray-100 p-4 rounded-2xl flex items-center justify-between shadow-sm hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-orange-50 text-orange-500 rounded-xl">
                <Globe class="w-5 h-5" />
              </div>
              <div class="text-left">
                <p class="text-[14px] font-semibold text-gray-800">{{ t('settings.language') }}</p>
                <p class="text-[11px] text-gray-500">{{ currentLanguageLabel }}</p>
              </div>
            </div>
            <ChevronRight class="w-5 h-5 text-gray-300 transition-transform" :class="{'rotate-90': isLanguageMenuOpen}" />
          </button>

          <div 
            v-if="isLanguageMenuOpen" 
            class="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-100 rounded-2xl shadow-lg z-50 overflow-hidden"
          >
            <button 
              v-for="lang in languages" 
              :key="lang.code"
              @click="changeLanguage(lang.code)"
              class="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 text-[14px] font-medium"
            >
              {{ lang.label }}
              <Check v-if="locale === lang.code" class="w-4 h-4 text-primary-500" />
            </button>
          </div>
        </div>

        <div class="bg-white border border-gray-100 p-4 rounded-2xl flex items-center justify-between shadow-sm">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-purple-50 text-purple-500 rounded-xl">
              <Moon class="w-5 h-5" />
            </div>
            <div>
              <p class="text-[14px] font-semibold text-gray-800">{{ t('settings.dark_mode') }}</p>
              <p class="text-[11px] text-gray-500">{{ t('settings.dark_mode_desc') }}</p>
            </div>
          </div>
          <button 
            @click="darkMode = !darkMode"
            class="w-11 h-6 rounded-full transition-colors relative"
            :class="darkMode ? 'bg-primary-500' : 'bg-gray-200'"
          >
            <div 
              class="absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-transform"
              :class="darkMode ? 'translate-x-5' : 'translate-x-0'"
            ></div>
          </button>
        </div>
      </div>
    </div>

    <div class="px-5 mt-8">
      <h3 class="font-bold text-gray-900 mb-4 px-1 text-lg">{{ t('settings.support_title') }}</h3>
      <div class="bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm">
        <button class="w-full px-4 py-4 flex items-center justify-between border-b border-gray-50 hover:bg-gray-50 transition-colors">
          <div class="flex items-center space-x-3">
            <HelpCircle class="w-5 h-5 text-gray-400" />
            <span class="text-[14px] font-medium text-gray-700">{{ t('settings.help_center') }}</span>
          </div>
          <ChevronRight class="w-4 h-4 text-gray-300" />
        </button>
        <button class="w-full px-4 py-4 flex items-center justify-between border-b border-gray-50 hover:bg-gray-50 transition-colors">
          <div class="flex items-center space-x-3">
            <Lock class="w-5 h-5 text-gray-400" />
            <span class="text-[14px] font-medium text-gray-700">{{ t('settings.privacy_policy') }}</span>
          </div>
          <ChevronRight class="w-4 h-4 text-gray-300" />
        </button>
        <button 
          @click="handleLogout"
          class="w-full px-4 py-4 flex items-center space-x-3 text-red-500 hover:bg-red-50 transition-colors"
        >
          <LogOut class="w-5 h-5" />
          <span class="text-[14px] font-bold">{{ t('settings.logout') }}</span>
        </button>
      </div>
    </div>
  </div>
</template>