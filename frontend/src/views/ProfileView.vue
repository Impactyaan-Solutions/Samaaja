<script setup>
import { ref, onMounted } from 'vue'
import { ChevronDown, Leaf, Droplets, BookOpen, Settings } from 'lucide-vue-next'

// 1. Initialize user as a reactive ref
const user = ref({
  name: 'Loading...',
  role: 'Volunteer @ XYZ Organisation',
  bio: '',
  image: '',
  stats: {
    actions: 0,
    issuesResolved: 0,
    posts: 0
  }
})

const isLoading = ref(true)

// 2. Fetch function
const fetchUserData = async () => {
  try {
    const response = await fetch('https://dev.samaaja.impactyaan.com/api/method/samaaja.api.leaderboard.user_leaderboard')
    const result = await response.json()

    if (result.status === 'success') {
      const apiData = result.data
      
      // 3. Map API data to our state
      user.value = {
        name: apiData.full_name || apiData.name,
        role: 'Volunteer @ XYZ Organisation', // Static as API doesn't provide this
        // Use interest from API or a default bio
        bio: apiData.interest || "Working on water conservation and community mobilization", 
        // Use user_image from API or a fallback placeholder
        image: apiData.user_image || "https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=200&q=80",
        stats: {
          actions: 24, // Placeholders as API doesn't provide stats yet
          issuesResolved: 10,
          posts: 8
        }
      }
    }
  } catch (error) {
    console.error("Error fetching profile:", error)
  } finally {
    isLoading.value = false
  }
}

// 4. Trigger fetch when component loads
onMounted(() => {
  fetchUserData()
})
</script>

<template>
  <div v-if="!isLoading" class="min-h-full bg-gray-50/50 pb-6">
    <!-- Header -->
    <header class="bg-white px-5 py-4 flex items-center justify-between sticky top-0 z-20 shadow-sm">
      <h2 class="font-bold text-gray-900 text-xl">Profile</h2>
      <button class="w-9 h-9 bg-gray-50 rounded-full flex items-center justify-center hover:bg-gray-100">
        <Settings class="w-5 h-5 text-gray-600" />
      </button>
    </header>

    <div class="bg-white pb-6 rounded-b-[2rem] shadow-sm mb-6 border-b border-gray-100">
      <div class="flex flex-col items-center pt-8 px-6 text-center">
        <!-- Avatar -->
        <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 border-4 border-white shadow-lg mb-4">
          <img :src="user.image" class="w-full h-full object-cover" />
        </div>
        
        <h1 class="text-2xl font-bold text-gray-900">{{ user.name }}</h1>
        <p class="text-primary-600 font-semibold text-sm mt-1">{{ user.role }}</p>
        <p class="text-gray-500 italic text-sm mt-4 px-2 tracking-wide leading-relaxed">"{{ user.bio }}"</p>

        <!-- Tags -->
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

        <button class="mt-8 border border-gray-200 rounded-2xl px-6 py-3.5 flex items-center space-x-3 w-full justify-between hover:bg-gray-50 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
          <span class="font-bold text-gray-800 text-sm pl-2">Switch Layer (Volunteer)</span>
          <ChevronDown class="w-5 h-5 text-gray-400" />
        </button>
      </div>
    </div>

    <!-- Impact Summary -->
    <div class="px-5">
      <div class="flex items-center space-x-2 mb-4">
        <span class="text-xl">🌟</span>
        <h3 class="font-bold text-gray-900 text-lg">Impact Summary</h3>
      </div>
      
      <div class="grid grid-cols-3 gap-3">
        <div class="bg-white border border-gray-100 p-4 rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-primary-600 mb-1">{{ user.stats.actions }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">Actions</span>
        </div>
        <div class="bg-white border border-gray-100 p-4 rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-primary-600 mb-1">{{ user.stats.issuesResolved }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">Issues<br/>Resolved</span>
        </div>
        <div class="bg-white border border-gray-100 p-4 rounded-2xl flex flex-col justify-center items-center text-center shadow-sm">
          <span class="text-3xl font-bold text-primary-600 mb-1">{{ user.stats.posts }}</span>
          <span class="text-[11px] text-gray-500 font-medium leading-tight">Posts</span>
        </div>
      </div>
    </div>

    <!-- Badges Earned -->
    <div class="px-5 mt-8 mb-20">
      <div class="flex items-center space-x-2 mb-4">
        <span class="text-xl">🥇</span>
        <h3 class="font-bold text-gray-900 text-lg">Badges Earned</h3>
      </div>
      <div class="bg-white border border-gray-100 p-6 rounded-2xl shadow-sm italic text-gray-400 text-sm text-center">
        No badges earned yet. Keep contributing!
      </div>
    </div>
  </div>

  <!-- Loading State -->
  <div v-else class="h-screen flex items-center justify-center">
    <p class="text-gray-500 font-medium">Fetching profile...</p>
  </div>
</template>