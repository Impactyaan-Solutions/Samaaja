<script setup>
import { ref, onMounted } from 'vue'
import { Search, Filter, Menu, Award } from 'lucide-vue-next'
import { getLeaderboard } from '@/services/api' // Adjust path if necessary
import { ref } from 'vue'
import { Search, Filter, Award } from 'lucide-vue-next'
import AppHeader from '@/components/common/AppHeader.vue'

const scope = ref('organisation')
const list = ref([])
const isLoading = ref(true)

// Fetch data on component mount
onMounted(async () => {
  try {
    const data = await getLeaderboard()
    
    // Map the API data to your UI format
    list.value = data.map((item, index) => ({
      rank: index + 1,
      name: item.full_name || 'Anonymous',
      // Fallback to "Member" if user_category is null
      role: item.user_category || 'Community Member',
      actions: item.contributions,
      // Use user_image if available, otherwise use the first letter of name
      avatar: item.user_image || (item.full_name ? item.full_name.charAt(0) : '?'),
      verified: false, // Set default or based on other logic
      email: item.user,
      // Logic for current user could be added here if you have auth state
      isCurrentUser: false 
    }))
  } catch (error) {
    console.error("Error loading leaderboard:", error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="min-h-full bg-gray-50/50 pb-6">
    <AppHeader />

    <!-- Toggle & Search -->
    <div class="px-5 mt-4">
      <div class="flex items-center bg-gray-100/80 p-1 rounded-xl mb-4 shadow-inner">
        <button 
          @click="scope = 'organisation'"
          class="flex-1 py-2 text-sm font-semibold rounded-lg transition-all"
          :class="scope === 'organisation' ? 'bg-white text-primary-600 shadow-sm' : 'text-gray-500'"
        >
          Organisation
        </button>
        <button 
          @click="scope = 'global'"
          class="flex-1 py-2 text-sm font-semibold rounded-lg transition-all"
          :class="scope === 'global' ? 'bg-white text-primary-600 shadow-sm' : 'text-gray-500'"
        >
          Global
        </button>
      </div>

      <div class="relative flex items-center">
        <Search class="absolute left-4 w-5 h-5 text-gray-400" />
        <input 
          type="text" 
          placeholder="Search City or Country..." 
          class="w-full bg-white border border-gray-200 rounded-2xl py-3.5 pl-11 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-shadow shadow-sm"
        />
        <button class="absolute right-4 text-gray-400 hover:text-gray-600">
          <Filter class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="px-5 mt-10 text-center text-gray-400">
      <p class="text-sm">Loading leaderboard...</p>
    </div>

    <!-- List -->
    <div class="px-5 mt-6 space-y-3">
      <div 
        v-for="user in list" :key="user.rank"
        class="bg-white p-4 rounded-2xl flex items-center justify-between border shadow-[0_2px_10px_rgba(0,0,0,0.02)] transition-shadow"
        :class="user.isCurrentUser ? 'border-primary-200 shadow-primary-100' : 'border-gray-100'"
      >
        <div class="flex items-center space-x-4">
          <span class="w-5 text-center font-bold text-gray-400 text-sm" :class="{'text-yellow-500': user.rank === 1, 'text-gray-400': user.rank === 2, 'text-amber-600': user.rank === 3}">
            {{ user.rank }}
          </span>
          <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 overflow-hidden">
            <img v-if="user.avatar.length > 2" :src="user.avatar" class="w-full h-full object-cover" />
            <span v-else class="font-bold">{{ user.avatar }}</span>
          </div>
          <div>
            <div class="flex items-center space-x-1">
              <h4 class="font-bold text-gray-900 text-sm">{{ user.name }}</h4>
              <Award v-if="user.verified" class="w-3.5 h-3.5 text-green-500" />
            </div>
            <p class="text-xs text-gray-500 mt-0.5">{{ user.role }}</p>
          </div>
        </div>
        
        <div class="bg-blue-50/70 border border-blue-50 text-primary-600 px-3 py-2 rounded-xl flex flex-col items-center min-w-[3.5rem]">
          <span class="font-bold text-sm leading-none">{{ user.actions }}</span>
          <span class="text-[8px] uppercase font-bold tracking-wider mt-1 opacity-70">Actions</span>
        </div>
      </div>
    </div>
  </div>
</template>
