<script setup>
import { Bell, CheckCircle } from 'lucide-vue-next'

const announcements = [
  {
    id: 1,
    title: 'New Event: River Cleanup Drive',
    desc: 'Join us this Saturday for a community cleanup along the riverbed.',
    time: '1h ago',
    read: false
  },
  {
    id: 2,
    title: 'Milestone Reached!',
    desc: 'Our community just crossed 10,000 resolved issues. Thank you to all the volunteers.',
    time: '1d ago',
    read: true
  }
]
</script>

<template>
  <div class="min-h-full bg-gray-50/50 pb-6 text-gray-800">
    <header class="bg-white px-5 py-4 flex items-center justify-between sticky top-0 z-20 shadow-sm border-b border-gray-100">
      <h2 class="font-bold text-gray-900 text-xl">Announcements</h2>
      <button class="bg-gray-50 text-gray-600 text-[11px] font-bold px-3 py-1.5 rounded-lg hover:bg-gray-100">
        Mark All Read
      </button>
    </header>

    <div class="px-5 mt-4 space-y-3">
      <div 
        v-for="item in announcements" :key="item.id"
        class="bg-white p-4 rounded-2xl border shadow-sm flex items-start space-x-4"
        :class="item.read ? 'border-gray-100 opacity-80' : 'border-primary-100 shadow-primary-500/5'"
      >
        <div class="mt-1">
          <div v-if="!item.read" class="w-10 h-10 rounded-full bg-primary-50 flex items-center justify-center text-primary-600">
            <Bell class="w-5 h-5" />
          </div>
          <div v-else class="w-10 h-10 rounded-full bg-gray-50 flex items-center justify-center text-gray-400">
            <CheckCircle class="w-5 h-5" />
          </div>
        </div>
        <div class="flex-1">
          <div class="flex items-start justify-between">
            <h4 class="font-bold text-gray-900 text-[15px]" :class="!item.read ? 'text-gray-900' : 'text-gray-700'">
              {{ item.title }}
            </h4>
          </div>
          <p class="text-sm mt-1 leading-relaxed" :class="!item.read ? 'text-gray-600' : 'text-gray-500'">
            {{ item.desc }}
          </p>
          <span class="text-xs font-semibold mt-3 block" :class="!item.read ? 'text-primary-600' : 'text-gray-400'">
            {{ item.time }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
