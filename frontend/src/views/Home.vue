<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Plus, Edit3, HelpCircle, Loader2 } from 'lucide-vue-next'
import CommunityPost from '../components/common/CommunityPost.vue'
import AppHeader from '@/components/common/AppHeader.vue'
import { getFeed } from '@/services/api'
import { authState } from '@/auth'

let actions_taken = 0
let posts_created = 0
let hours_invested = 0
if (authState.profile.stats){
  actions_taken = authState.profile.stats.actions || 0
  posts_created = authState.profile.stats.posts || 0
  hours_invested = authState.profile.stats.hours || 0
}
const posts = ref([])

const limit = 10
const offset = ref(0)

const hasMore = ref(true)


const startY = ref(0)
const currentY = ref(0)
const isRefreshing = ref(false)
const isPulling = ref(false)

const getScrollTop = (node) => {
  if (!node || node === document.body) return window.scrollY;
  const overflowY = window.getComputedStyle(node).overflowY;
  if ((overflowY === 'auto' || overflowY === 'scroll') && node.scrollHeight > node.clientHeight) {
    return node.scrollTop;
  }
  return getScrollTop(node.parentNode);
}

const handleTouchStart = (e) => {
  if (isRefreshing.value) return;
  const scrollTop = getScrollTop(e.target);
  if (scrollTop <= 0) {
    startY.value = e.touches[0].clientY;
    isPulling.value = true;
  }
}

const handleTouchMove = (e) => {
  if (!isPulling.value || isRefreshing.value) return;
  const y = e.touches[0].clientY;
  const deltaY = y - startY.value;
  if (deltaY > 0) {
    // Apply resistance
    currentY.value = deltaY * 0.4;
  } else {
    isPulling.value = false;
  }
}

const handleTouchEnd = () => {
  if (!isPulling.value) return;
  if (currentY.value > 60) {
    isRefreshing.value = true;
    currentY.value = 50;
    
    // Simulate API refresh
    setTimeout(() => {
      // Actually reset the posts array back to default 2 posts to simulate a true "fresh" pull
      posts.value = posts.value.slice(0, 2);
      
      isRefreshing.value = false;
      currentY.value = 0;
    }, 1500);
  } else {
    currentY.value = 0;
  }
}

const loadMoreSentinel = ref(null)
const isLoadingMore = ref(false)
let observer = null

const loadMorePosts = async () => {
  await fetchPosts();
}
const fetchPosts = async () => {
  if (isLoadingMore.value || !hasMore.value) return

  isLoadingMore.value = true

  try {
    const response = await getFeed(limit, offset.value)

    const newPosts = response.posts || []

    posts.value.push(...newPosts)

    offset.value += limit

    hasMore.value = response.has_more
  } catch (err) {
    console.error(err)
  } finally {
    isLoadingMore.value = false
  }
}

onMounted(async() => {
  const feed = await fetchPosts();
  if(feed){
       posts.value=feed;
   }
  observer = new IntersectionObserver((entries) => {
    if (
      entries[0].isIntersecting &&
      hasMore.value &&
      !isLoadingMore.value
    ) {
        loadMorePosts()
    }
  }, { rootMargin: '200px' }) // Trigger 200px before reaching the bottom
  
  if (loadMoreSentinel.value) {
    observer.observe(loadMoreSentinel.value)
  }
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect();
  }
})
</script>

<template>
  <div 
    class="min-h-full bg-gray-50/50 pb-6 relative"
    @touchstart.passive="handleTouchStart"
    @touchmove.passive="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <!-- Pull to Refresh Indicator -->
    <div 
      class="absolute left-0 right-0 flex justify-center pointer-events-none z-50 text-primary-600"
      :style="{ 
        transform: `translateY(${Math.max(0, currentY - 20)}px)`, 
        opacity: currentY > 5 || isRefreshing ? 1 : 0,
        transition: isPulling ? 'none' : 'all 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28)' 
      }"
    >
      <div class="bg-white rounded-full p-2.5 shadow-md flex items-center justify-center mt-2 border border-gray-100">
        <Loader2 class="w-5 h-5" :class="{ 'animate-spin': isRefreshing, 'rotate-180': currentY > 60 && !isRefreshing }" style="transition: transform 0.2s" />
      </div>
    </div>

    <AppHeader />

    <!-- Stats Grid -->
    <div class="px-5 mt-5 grid grid-cols-3 gap-3">
      <div class="bg-primary-700 text-white p-3 rounded-2xl flex flex-col items-center justify-center shadow-md shadow-primary-500/20">
        <span class="text-2xl font-bold">{{ actions_taken }}</span>
        <span class="text-[9px] uppercase tracking-wider opacity-80 mt-1 font-semibold">Actions</span>
      </div>
      <div class="bg-primary-600 text-white p-3 rounded-2xl flex flex-col items-center justify-center shadow-md shadow-primary-500/20">
        <span class="text-2xl font-bold">{{ posts_created }}</span>
        <span class="text-[9px] uppercase tracking-wider opacity-80 mt-1 font-semibold">Posts</span>
      </div>
      <div class="bg-primary-500 text-white p-3 rounded-2xl flex flex-col items-center justify-center shadow-md shadow-primary-500/20">
        <span class="text-2xl font-bold">{{ hours_invested }}h</span>
        <span class="text-[9px] uppercase tracking-wider opacity-80 mt-1 font-semibold">Invested</span>
      </div>
    </div>

    <!-- Quick Actions -->
<!--     <div class="px-5 mt-4 grid grid-cols-3 gap-3">
      <button class="bg-white border border-gray-100 py-2 rounded-xl flex items-center justify-center space-x-2 shadow-sm text-gray-700 hover:bg-gray-50">
        <Plus class="w-4 h-4 text-primary-500" />
        <span class="text-[11px] font-semibold">Action</span>
      </button>
      <button class="bg-white border border-gray-100 py-2 rounded-xl flex items-center justify-center space-x-2 shadow-sm text-gray-700 hover:bg-gray-50">
        <Edit3 class="w-4 h-4 text-primary-500" />
        <span class="text-[11px] font-semibold">Post</span>
      </button>
      <button class="bg-white border border-gray-100 py-2 rounded-xl flex items-center justify-center space-x-2 shadow-sm text-gray-700 hover:bg-gray-50">
        <HelpCircle class="w-4 h-4 text-primary-500" />
        <span class="text-[11px] font-semibold">Ask Help</span>
      </button>
    </div> -->

    <!-- Feed -->
    <div class="px-5 mt-6">
      <h3 class="font-bold text-gray-900 mb-4 px-1 text-lg">Community Feed</h3>
      <CommunityPost v-for="post in posts" :key="post.id" :post="post" />
      
      <!-- Infinite Scroll Trigger Sentinel -->
      <div ref="loadMoreSentinel" class="py-8 flex justify-center items-center opacity-70">
        <Loader2 v-if="isLoadingMore" class="w-6 h-6 animate-spin text-primary-500" />
      </div>
      <div
        v-if="!hasMore"
        class="text-center text-sm text-gray-400 py-6"
      >
        No more posts
      </div>
    </div>
  </div>
</template>
