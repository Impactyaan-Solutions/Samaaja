<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { MoreHorizontal, MessageSquare, Heart, Share2, Award } from 'lucide-vue-next'
import { getTimeSinceCreation } from '@/utils/utils'
defineProps({
  post: {
    type: Object,
    required: true
  }
})

const isVisible = ref(true)
const containerRef = ref(null)
const savedHeight = ref(0)
let observer = null

onMounted(() => {
  observer = new IntersectionObserver((entries) => {
    const entry = entries[0]
    if (entry.isIntersecting) {
      isVisible.value = true
    } else {
      // Save exact height before unmounting child DOM to prevent layout shift jumping
      if (containerRef.value) {
        savedHeight.value = containerRef.value.getBoundingClientRect().height
      }
      isVisible.value = false
    }
  }, { rootMargin: '600px' }) // Buffer zone: Keep nodes alive if they are within 600px of visible screen

  if (containerRef.value) {
    observer.observe(containerRef.value)
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>

<template>
  <div 
    ref="containerRef" 
    class="bg-white rounded-2xl shadow-[0_2px_12px_rgba(0,0,0,0.04)] mb-4 border border-gray-100"
    :style="{ minHeight: !isVisible && savedHeight ? `${savedHeight}px` : 'auto' }"
  >
    <!-- Hiding via CSS: When off-screen, it hides the DOM to reduce rendering load, but keeps nodes in memory to prevent image re-fetching -->
    <div v-show="isVisible">
    <!-- Header -->
    <div class="p-4 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-gray-200 overflow-hidden">
          <img v-if="post.user_profile?.user_image" :src="post.user_profile.user_image" alt="Avatar" class="w-full h-full object-cover"/>
          <div v-else class="w-full h-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold">
            {{ post.user_profile?.full_name?.charAt(0) || '?' }}
          </div>
        </div>
        <div>
          <div class="flex items-center space-x-1">
            <h4 class="font-semibold text-gray-900 text-sm">{{ post.user_profile?.full_name || 'Unknown User' }}</h4>
            <Award v-if="post.user_profile?.user_type" class="w-3.5 h-3.5 text-green-500" />
          </div>
          <p class="text-xs text-gray-500">{{ post.user_profile?.user_category || '' }}</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-xs text-gray-400 font-medium">{{ getTimeSinceCreation(post.creation) }}</span>
      </div>
    </div>

    <!-- Content -->
    <div class="px-4 pb-3">
      <p class="text-gray-800 text-sm leading-relaxed mb-3">
        {{ post.title }}
      </p>
      <p v-if = "post.description" class="text-gray-800 text-sm leading-relaxed mb-3">
        {{ post.description }}
      </p>
      <!-- Media -->
      <div v-if="post.media" class="rounded-xl overflow-hidden mb-3 max-h-64 bg-gray-100">
        <img :src="post.media" class="w-full h-full object-cover" />
      </div>

      <!-- Tags -->
      <div class="flex items-center space-x-2 mb-2">
        <span class="px-2.5 py-1 bg-blue-50 text-blue-600 rounded-lg text-[10px] font-bold tracking-wide uppercase">
          {{ post.tag }}
        </span>
      </div>
    </div>

    <!-- Actions Footer -->
    <div class="px-4 py-3 border-t border-gray-50 flex items-center justify-between">
      <div class="flex items-center space-x-6">
        <button class="flex items-center space-x-1.5 text-gray-500 hover:text-red-500 transition-colors">
          <Heart class="w-5 h-5" />
          <span class="text-xs font-semibold">{{ post.like_count }}</span>
        </button>
        <button class="flex items-center space-x-1.5 text-gray-500 hover:text-primary-500 transition-colors">
          <MessageSquare class="w-5 h-5" />
          <span class="text-xs font-semibold">{{ post.comment_count }}</span>
        </button>
      </div>
    </div>
    </div>
  </div>
</template>
