<script setup>
import { ref } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import BottomTabBar from './components/layout/BottomTabBar.vue'
import ActionBottomSheet from './components/Overlays/ActionBottomSheet.vue'

const route = useRoute()
const showActionSheet = ref(false)

const handleActClick = () => {
  showActionSheet.value = true
}
</script>

<template>
  <!-- Main Application Shell -->
  <div class="relative h-[100dvh] bg-gray-50 mx-auto max-w-md shadow-2xl overflow-hidden flex flex-col">
    <!-- Header/Content Area Wrapper -->
    <main class="flex-grow overflow-y-auto pb-24 relative">
      <RouterView />
    </main>

    <!-- Global Bottom Navigation Bar (Hidden on specific views like Form) -->
  <BottomTabBar 
    v-if="!route.meta.hideNavbar" 
    @act="handleActClick" 
  />

    <!-- Action Sheet Overlay -->
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
