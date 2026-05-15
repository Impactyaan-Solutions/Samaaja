<script setup>
import { ref, onMounted } from "vue"
import { ArrowRightCircle, Loader2 } from "lucide-vue-next"
import { getActiveAnnouncements, recordInteraction } from "@/services/api"
import { authState } from "@/auth"
import AppHeader from "@/components/common/AppHeader.vue"

const announcements = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    announcements.value = await getActiveAnnouncements()

    // Track viewed announcements to decrement counter locally
    for (const a of announcements.value) {
      const res = await recordInteraction(a.name, "View")
      if (res && res.data && res.data.status === "success") {
        // Decrement the local unread count if it was unread
        if (authState.unreadAlertsCount > 0) {
          authState.unreadAlertsCount--
        }
      }
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const handleInteraction = (item) => {
  if (item.url_link) {
    recordInteraction(item.name, "Click")
    window.open(item.url_link, "_blank")
  }
}

const formatDate = (timeStr) => {
  if (!timeStr) return ""
  const date = new Date(timeStr)
  return date.toLocaleDateString([], { day: "2-digit", month: "short", year: "numeric" })
}
</script>

<template>
  <div class="min-h-full bg-gray-50/50 pb-6 text-gray-800">
    <AppHeader />

    <div v-if="loading" class="px-5 mt-10 text-center text-gray-500 flex flex-col items-center">
      <Loader2 class="w-8 h-8 animate-spin text-primary-500 mb-2" />
      <span>Loading announcements...</span>
    </div>

    <div v-else-if="error" class="px-5 mt-10 text-center text-red-500">
      {{ error }}
    </div>

    <div v-else-if="announcements.length === 0" class="px-5 mt-10 text-center text-gray-500">
      No active announcements.
    </div>

    <div v-else class="px-5 mt-4 space-y-4">
      <div
        v-for="item in announcements" :key="item.name"
        @click="handleInteraction(item)"
        class="bg-white rounded-3xl overflow-hidden border border-gray-100 shadow-sm flex flex-col cursor-pointer active:scale-[0.99] transition-transform"
      >
        <!-- Hero Image -->
        <div v-if="item.image" class="w-full h-48 bg-gray-200">
          <img :src="item.image" class="w-full h-full object-cover" />
        </div>
        <div v-else class="w-full h-12 bg-primary-50"></div>

        <!-- Content Area -->
        <div class="p-5 flex items-start justify-between gap-4">
          <div class="flex-1">
            <h4 class="font-bold text-gray-900 text-lg leading-tight mb-1">
              {{ item.title }}
            </h4>

            <div class="text-sm text-gray-600 announcement-content mb-3" v-html="item.message">
            </div>

            <div class="flex flex-wrap items-center text-[11px] font-bold uppercase tracking-wider text-primary-600 gap-1">
              <span>{{ formatDate(item.valid_from) }}</span>
              <span v-if="item.valid_to" class="text-gray-400">-</span>
              <span v-if="item.valid_to">{{ formatDate(item.valid_to) }}</span>
            </div>
          </div>

          <!-- Action Button -->
          <div class="flex-shrink-0 mt-1">
            <ArrowRightCircle class="w-8 h-8 text-primary-600 hover:text-primary-700" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.announcement-content :deep(p) {
  margin-bottom: 0.25rem;
  line-height: 1.5;
}
.announcement-content :deep(p:last-child) {
  margin-bottom: 0;
}
</style>
