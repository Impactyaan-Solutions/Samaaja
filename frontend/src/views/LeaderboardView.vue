<script setup>
import { ref } from 'vue'
import { Search, Filter, Menu, Award } from 'lucide-vue-next'

const scope = ref('organisation') // 'organisation' or 'global'

const list = [
  { rank: 1, name: 'Meera Nair', role: 'Lead @ Save Earth', actions: 156, avatar: 'M', verified: true },
  { rank: 2, name: 'Vikram Singh', role: 'Volunteer @ Green City', actions: 142, avatar: 'V', verified: false },
  { rank: 3, name: 'Anjali Sharma', role: 'Volunteer @ EcoWarriors', actions: 128, avatar: 'A', verified: false, isCurrentUser: true },
  { rank: 4, name: 'Rahul Verma', role: 'Member @ Green City', actions: 94, avatar: 'R', verified: false },
  { rank: 5, name: 'Priya Patel', role: 'Resident @ Ward 45', actions: 87, avatar: 'P', verified: false },
  { rank: 6, name: 'Karan Desai', role: 'Volunteer @ EcoWarriors', actions: 62, avatar: 'K', verified: false }
]
</script>

<template>
  <div class="min-h-full bg-gray-50/50 pb-6">
    <!-- Header -->
    <header class="bg-white px-5 py-4 flex items-center justify-between sticky top-0 z-20 shadow-sm border-b border-gray-100 mb-1">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold">AS</div>
        <div>
          <h2 class="font-bold text-gray-900 text-[15px]">Anjali Sharma</h2>
          <p class="text-[11px] text-gray-500">Volunteer @ EcoWarriors</p>
        </div>
      </div>
      <button class="w-9 h-9 bg-gray-50 rounded-full flex items-center justify-center hover:bg-gray-100">
        <Menu class="w-5 h-5 text-gray-600" />
      </button>
    </header>

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
            <img v-if="user.avatar.length > 2" :src="user.avatar" />
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
