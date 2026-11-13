<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Plus, Edit3, HelpCircle, Loader2 } from 'lucide-vue-next'
import CommunityPost from '../components/common/CommunityPost.vue'
import AppHeader from '@/components/common/AppHeader.vue'
import { getFeed } from '@/services/api'
import { authState } from '@/auth'

const { t } = useI18n()

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
    console.log(response)
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
    class="page-wrapper relative"
    @touchstart.passive="handleTouchStart"
    @touchmove.passive="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <!-- Pull to Refresh Indicator -->
    <div
      class="pull-refresh-indicator"
      :style="{
        transform: `translateY(${Math.max(0, currentY - 20)}px)`,
        opacity: currentY > 5 || isRefreshing ? 1 : 0,
        transition: isPulling ? 'none' : 'all 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28)'
      }"
    >
      <div class="pull-refresh-bubble">
        <Loader2
          class="icon-md"
          :class="{ 'animate-spin': isRefreshing, 'rotate-180': currentY > 60 && !isRefreshing }"
          style="transition: transform 0.2s"
        />
      </div>
    </div>

    <AppHeader />

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card stat-card--dark">
        <span class="stat-value">{{ actions_taken }}</span>
        <span class="stat-label">{{ t('home.actions') }}</span>
      </div>
      <div class="stat-card stat-card--mid">
        <span class="stat-value">{{ posts_created }}</span>
        <span class="stat-label">{{ t('home.posts') }}</span>
      </div>
      <div class="stat-card stat-card--light">
        <span class="stat-value">{{ hours_invested }}h</span>
        <span class="stat-label">{{ t('home.invested') }}</span>
      </div>
    </div>

    <!-- Quick Actions (commented out) -->
    <!--
    <div class="quick-actions-grid">
      <button class="quick-action-btn">
        <Plus class="icon-md text-primary-color" />
        <span class="quick-action-label">Action</span>
      </button>
      <button class="quick-action-btn">
        <Edit3 class="icon-md text-primary-color" />
        <span class="quick-action-label">Post</span>
      </button>
      <button class="quick-action-btn">
        <HelpCircle class="icon-md text-primary-color" />
        <span class="quick-action-label">Ask Help</span>
      </button>
    </div>
    -->

    <!-- Feed -->
    <div class="feed-section">
      <h3 class="feed-title">{{ t('home.communityFeed') }}</h3>
      <CommunityPost v-for="post in posts" :key="post.id" :post="post" />

      <!-- Infinite Scroll Sentinel -->
      <div ref="loadMoreSentinel" class="load-more-sentinel">
        <Loader2 v-if="isLoadingMore" class="spinner spinner-md" />
      </div>

      <div v-if="!hasMore" class="no-more-posts">
        {{ t('home.noMorePosts') }}
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Pull to Refresh */
.pull-refresh-indicator {
  @apply absolute left-0 right-0 flex-center pointer-events-none z-50 text-blue-600;
}

.pull-refresh-bubble {
  @apply bg-white rounded-full shadow-md flex-center mt-2 border border-gray-100;
  padding: 0.625rem;
}

/* Stats */
.stats-grid {
  @apply px-5 mt-5 grid grid-cols-3 gap-3;
}

.stat-card {
  @apply text-white p-3 rounded-2xl flex-col-center shadow-md;
}

.stat-card--dark {
  @apply bg-blue-700;
  box-shadow: 0 4px 6px -1px rgba(29, 78, 216, 0.25);
}

.stat-card--mid {
  @apply bg-blue-600;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.25);
}

.stat-card--light {
  @apply bg-blue-500;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.25);
}

.stat-value {
  @apply text-2xl font-bold;
}

.stat-label {
  @apply text-xs uppercase font-semibold opacity-80 mt-1;
  letter-spacing: 0.08em;
  font-size: 9px;
}

/* Quick Actions */
.quick-actions-grid {
  @apply px-5 mt-4 grid grid-cols-3 gap-3;
}

.quick-action-btn {
  @apply bg-white border border-gray-100 py-2 rounded-xl flex-center gap-2 shadow-sm text-body cursor-pointer transition;
}

.quick-action-btn:hover {
  @apply bg-gray-50;
}

.quick-action-label {
  @apply text-xs font-semibold;
}

/* Feed */
.feed-section {
  @apply px-5 mt-6;
}

.feed-title {
  @apply text-lg font-bold text-heading mb-4 px-1;
}

.load-more-sentinel {
  @apply py-8 flex-center opacity-70;
}

.no-more-posts {
  @apply text-center text-sm text-muted py-6;
}

/* Animations */
.rotate-180 {
  transform: rotate(180deg);
}
</style>
