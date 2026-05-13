<script setup>
import { ref, onMounted } from 'vue'
import { 
  User, 
  Bell, 
  Lock, 
  Globe, 
  Moon, 
  HelpCircle, 
  LogOut, 
  ChevronRight,
  Loader2
} from 'lucide-vue-next'
import AppHeader from '@/components/common/AppHeader.vue'
import { getProfile, logout } from '@/services/api.js'
import router from '../router'

// Reactive states
const notifications = ref(false) // Push notifications off by default
const darkMode = ref(false)
const isLoading = ref(true)

const user = ref({
  name: '',
  role: 'Volunteer', // Default category
  email: '',
  avatar: null
})

const fetchUserProfile = async () => {
  try {
    isLoading.value = true
    
    // Attempt to get email from localStorage (typical flow) 
    // or fallback to the provided example email
    const currentUserEmail = localStorage.getItem('user_email') || 'rudransh20septmber@gmail.com'
    
    const profileData = await getProfile(currentUserEmail)
    
    if (profileData) {
      user.value = {
        name: profileData.full_name,
        email: profileData.email,
        // Using user_category from API for the role badge
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
    // Call the API service logout method
    await logout()
  } catch (error) {
    console.error("Logout request failed, proceeding with local cleanup:", error)
  } finally {
    // Always clear local session data and redirect regardless of API status
    localStorage.removeItem('user_email')
    localStorage.removeItem('token') // Ensure this matches your auth token key
    
    // Redirect to login page
    router.push('/login')
  }
}
</script>

<template>
  <div class="min-h-full bg-gray-50/50 pb-10 relative">
    <AppHeader />

    <!-- Settings Groups -->
    <div class="px-5 mt-8">
      <h3 class="font-bold text-gray-900 mb-4 px-1 text-lg">App Settings</h3>
      
      <div class="space-y-3">
        <!-- Notification Toggle -->
        <div class="bg-white border border-gray-100 p-4 rounded-2xl flex items-center justify-between shadow-sm">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-blue-50 text-blue-500 rounded-xl">
              <Bell class="w-5 h-5" />
            </div>
            <div>
              <p class="text-[14px] font-semibold text-gray-800">Push Notifications</p>
              <p class="text-[11px] text-gray-500">Activity and alerts</p>
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

        <!-- Language Selection -->
        <button class="w-full bg-white border border-gray-100 p-4 rounded-2xl flex items-center justify-between shadow-sm hover:bg-gray-50 transition-colors">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-orange-50 text-orange-500 rounded-xl">
              <Globe class="w-5 h-5" />
            </div>
            <div class="text-left">
              <p class="text-[14px] font-semibold text-gray-800">Language</p>
              <p class="text-[11px] text-gray-500">English (US)</p>
            </div>
          </div>
          <ChevronRight class="w-5 h-5 text-gray-300" />
        </button>

        <!-- Dark Mode Toggle -->
        <div class="bg-white border border-gray-100 p-4 rounded-2xl flex items-center justify-between shadow-sm">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-purple-50 text-purple-500 rounded-xl">
              <Moon class="w-5 h-5" />
            </div>
            <div>
              <p class="text-[14px] font-semibold text-gray-800">Dark Mode</p>
              <p class="text-[11px] text-gray-500">Reduce eye strain</p>
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

    <!-- Support Section -->
    <div class="px-5 mt-8">
      <h3 class="font-bold text-gray-900 mb-4 px-1 text-lg">Support</h3>
      <div class="bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm">
        <button class="w-full px-4 py-4 flex items-center justify-between border-b border-gray-50 hover:bg-gray-50 transition-colors">
          <div class="flex items-center space-x-3">
            <HelpCircle class="w-5 h-5 text-gray-400" />
            <span class="text-[14px] font-medium text-gray-700">Help Center</span>
          </div>
          <ChevronRight class="w-4 h-4 text-gray-300" />
        </button>
        <button class="w-full px-4 py-4 flex items-center justify-between border-b border-gray-50 hover:bg-gray-50 transition-colors">
          <div class="flex items-center space-x-3">
            <Lock class="w-5 h-5 text-gray-400" />
            <span class="text-[14px] font-medium text-gray-700">Privacy Policy</span>
          </div>
          <ChevronRight class="w-4 h-4 text-gray-300" />
        </button>
        <button 
          @click="handleLogout"
          class="w-full px-4 py-4 flex items-center space-x-3 text-red-500 hover:bg-red-50 transition-colors"
        >
          <LogOut class="w-5 h-5" />
          <span class="text-[14px] font-bold">Log Out</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.translate-x-5 {
  transform: translateX(1.25rem);
}
</style>