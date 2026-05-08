<script setup>
import { ref, computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import BottomTabBar from './components/layout/BottomTabBar.vue'
import ActionBottomSheet from './components/Overlays/ActionBottomSheet.vue'

const route = useRoute()
const showActionSheet = ref(false)

const handleActClick = () => {
  showActionSheet.value = true
}

// Define the paths where you want absolutely 0 top/bottom padding
// Update these paths if your router uses different URLs (e.g., '/landing')
const flushPages = ['/', '/login', '/signup']

// Computed property to check if current route matches the flush pages
const isFlushPage = computed(() => flushPages.includes(route.path))
</script>

<template>
  <div class="relative h-[100dvh] bg-gray-50 mx-auto max-w-md shadow-2xl overflow-hidden flex flex-col">
    
    <main 
      class="flex-grow overflow-y-auto relative"
      :class="[
        // Only apply the 96px bottom padding if the navbar is showing AND it's not a flush page
        { 'pb-24': !route.meta.hideNavbar && !isFlushPage },
        // Force 0 padding globally for these specific pages
        { 'p-0': isFlushPage }
      ]"
    >
      <RouterView />
    </main>

    <BottomTabBar 
      v-if="!route.meta.hideNavbar" 
      @act="handleActClick" 
    />

    <ActionBottomSheet 
      v-if="showActionSheet" 
      @close="showActionSheet = false" 
    />
  </div>
</template>

<style>
/* For hiding scrollbar in mobile-first views */
::-webkit-scrollbar {
  width: 0px;
  background: transparent;
}
</style>