<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, Loader2, CalendarDays, Clock3, Sparkles } from 'lucide-vue-next'
import AppHeader from '@/components/common/AppHeader.vue'
import { createVolunteerInterest, getVolunteerListings } from '@/services/api'
import { authState } from '@/auth'

const listings = ref([])
const loading = ref(true)
const error = ref(null)
const query = ref('')
const interestedIds = ref([])

onMounted(async () => {
  try {
    listings.value = await getVolunteerListings()
  } catch (e) {
    error.value = e.message || 'Failed to load volunteer opportunities.'
  } finally {
    loading.value = false
  }
})

const filteredListings = computed(() => {
  const term = query.value.trim().toLowerCase()
  if (!term) return listings.value

  return listings.value.filter((item) => {
    const haystack = [
      item.title,
      item.description,
      item.category,
      item.type,
      item.start_date,
      item.end_date
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase()

    return haystack.includes(term)
  })
})

const formatDate = (value) => {
  if (!value) return 'Flexible schedule'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  return date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const typeStyles = (type) => {
  switch (type) {
    case 'Ongoing':
      return 'bg-green-50 text-green-700 border border-green-100'
    case 'One-time':
      return 'bg-amber-50 text-amber-700 border border-amber-100'
    default:
      return 'bg-blue-50 text-blue-700 border border-blue-100'
  }
}

const handleInterest = async (item) => {
  const opportunityId = item?.name

  if (!opportunityId) {
    console.error('Volunteer opportunity missing name/id', item)
    return
  }

  const user = authState.email || localStorage.getItem('user')

  if (!user) {
    console.error('No logged-in user found for volunteer interest submission')
    return
  }

  if (interestedIds.value.includes(opportunityId)) return

  try {
    interestedIds.value.push(opportunityId)
    await createVolunteerInterest({
      user,
      volunteer_opportunity: opportunityId
    })
  } catch (err) {
    console.error('Failed to submit volunteer interest', err)
    interestedIds.value = interestedIds.value.filter((id) => id !== opportunityId)
  }
}
</script>

<template>
  <div class="min-h-full bg-gray-50/50 pb-8 text-gray-800">
    <AppHeader title="Volunteer Opportunities" />

    <div class="px-5 mt-4">
      <div class="relative">
        <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          v-model="query"
          type="text"
          placeholder="Search opportunity or category"
          class="w-full bg-white border border-gray-200 rounded-2xl py-3.5 pl-11 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent shadow-sm"
        />
      </div>
    </div>

    <div v-if="loading" class="px-5 mt-10 text-center text-gray-500 flex flex-col items-center">
      <Loader2 class="w-8 h-8 animate-spin text-primary-500 mb-2" />
      <span>Loading volunteer opportunities...</span>
    </div>

    <div v-else-if="error" class="px-5 mt-10 text-center text-red-500">
      {{ error }}
    </div>

    <div v-else-if="filteredListings.length === 0" class="px-5 mt-10 text-center text-gray-500">
      No volunteer opportunities available yet.
    </div>

    <div v-else class="px-5 mt-5 space-y-4">
      <div
        v-for="item in filteredListings"
        :key="item.name || item.title"
        class="bg-white rounded-3xl border border-gray-100 shadow-[0_4px_18px_rgba(17,24,39,0.04)] p-4"
      >
        <div class="flex items-center justify-between gap-3">
          <span class="inline-flex items-center rounded-full bg-primary-50 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.08em] text-primary-700">
            {{ item.category || 'Community' }}
          </span>
          <span :class="['inline-flex items-center rounded-full px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.08em]', typeStyles(item.type)]">
            {{ item.type || 'Open' }}
          </span>
        </div>

        <h3 class="mt-4 text-xl font-bold text-gray-900 leading-tight">
          {{ item.title }}
        </h3>

        <p class="mt-2 text-sm leading-6 text-gray-600">
          {{ item.description }}
        </p>

        <div class="mt-4 space-y-2 text-sm text-gray-600">
          <div class="flex items-center gap-2">
            <CalendarDays class="w-4 h-4 text-primary-500" />
            <span>{{ formatDate(item.start_date) }}</span>
            <span v-if="item.end_date" class="text-gray-400">→</span>
            <span v-if="item.end_date">{{ formatDate(item.end_date) }}</span>
          </div>

          <div class="flex items-center gap-2">
            <Clock3 class="w-4 h-4 text-primary-500" />
            <span>{{ item.type || 'Flexible timing' }}</span>
          </div>
        </div>

        <div class="mt-4 flex items-center justify-between border-t border-gray-100 pt-3">
          <div class="flex items-center gap-2 text-xs text-gray-500">
            <Sparkles class="w-4 h-4 text-amber-500" />
            <span>Posted by {{ item.owner || 'Administrator' }}</span>
          </div>

          <button
            @click="handleInterest(item)"
            :disabled="interestedIds.includes(item.name)"
            class="bg-primary-600 text-white px-4 py-2 rounded-xl text-sm font-semibold shadow-sm hover:bg-primary-700 transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {{ interestedIds.includes(item.name) ? 'Interested' : 'I’m interested' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
