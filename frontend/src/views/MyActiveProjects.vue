<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ArrowLeft, MapPin, Loader2, ClipboardCheck } from 'lucide-vue-next'

import { getMyActiveProjects } from '@/services/api'

const { t } = useI18n()
const router = useRouter()

const projects = ref([])
const loading = ref(true)
const error = ref('')

const fetchProjects = async () => {
  loading.value = true
  error.value = ''

  try {
    const result = await getMyActiveProjects()
    projects.value = result?.projects || []
  } catch (err) {
    console.error('Failed to load active projects:', err)
    error.value = err?.message || t('myProjects.loadError')
  } finally {
    loading.value = false
  }
}

const goBack = () => router.back()

const goToDetail = (item) => {
  if (!item.name) return

  router.push({ name: 'volunteer-opportunity-detail', params: { id: item.name } })
}

const formatDescription = (description) => {
  if (!description) return t('volunteerListings.defaultDescription')

  if (description.length > 95) {
    return `${description.substring(0, 95)}...`
  }

  return description
}

onMounted(fetchProjects)
</script>

<template>
  <main class="min-h-full bg-gray-50 text-gray-900">
    <header
      class="sticky top-0 z-20 flex items-center justify-between border-b border-gray-50 bg-white px-5 py-5"
    >
      <button
        type="button"
        @click="goBack"
        class="-ml-2 rounded-full p-2 transition-colors hover:bg-gray-100"
        aria-label="Go back"
      >
        <ArrowLeft class="h-6 w-6 text-gray-800" />
      </button>

      <h2 class="text-base font-bold text-gray-900">
        {{ t('myProjects.headerTitle') }}
      </h2>

      <div class="h-6 w-6"></div>
    </header>

    <!-- Loading -->
    <div
      v-if="loading"
      class="flex flex-col items-center justify-center px-5 pt-16 text-center"
    >
      <Loader2 class="mb-3 h-7 w-7 animate-spin text-primary-500" />

      <p class="text-sm text-gray-500">
        {{ t('myProjects.loading') }}
      </p>
    </div>

    <!-- Error -->
    <div
      v-else-if="error"
      class="px-5 pt-12 text-center"
    >
      <p class="text-sm text-red-500">{{ error }}</p>
    </div>

    <!-- Empty -->
    <div
      v-else-if="projects.length === 0"
      class="px-5 pt-16 text-center"
    >
      <div
        class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-gray-100"
      >
        <ClipboardCheck class="h-6 w-6 text-gray-400" />
      </div>

      <h3 class="mt-4 text-base font-semibold text-gray-800">
        {{ t('myProjects.noProjects') }}
      </h3>

      <p class="mt-1 text-sm text-gray-500">
        {{ t('myProjects.noProjectsHint') }}
      </p>
    </div>

    <!-- Project cards -->
    <div
      v-else
      class="space-y-3 px-5 pb-6 pt-4"
    >
      <div
        v-for="item in projects"
        :key="item.name"
        @click="goToDetail(item)"
        @keydown.enter="goToDetail(item)"
        @keydown.space.prevent="goToDetail(item)"
        role="link"
        tabindex="0"
        class="cursor-pointer rounded-xl border border-gray-100 bg-white p-3.5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] transition hover:border-primary-200 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-primary-500"
      >
        <div class="flex flex-wrap items-center gap-2">
          <span
            class="inline-flex items-center gap-1.5 rounded-md bg-blue-100 px-2 py-1 text-[10px] font-semibold text-blue-800"
          >
            {{ item.category || t('volunteerListings.community') }}
          </span>
        </div>

        <h2 class="mt-2 text-sm font-bold leading-5 text-gray-900">
          {{ item.title || t('volunteerListings.opportunity') }}
        </h2>

        <p class="mt-1.5 text-xs leading-5 text-gray-500">
          {{ formatDescription(item.description) }}
        </p>

        <div class="mt-3 flex items-center justify-between gap-3">
          <div class="flex min-w-0 items-center gap-1.5 text-xs text-gray-500">
            <MapPin class="h-3.5 w-3.5 shrink-0 text-gray-400" />

            <span class="truncate">
              {{ item.location || t('volunteerListings.location') }}
            </span>
          </div>

          <button
            @click.stop="goToDetail(item)"
            class="shrink-0 rounded-md bg-primary-600 px-4 py-2 text-[11px] font-semibold text-white transition hover:bg-primary-700"
          >
            {{ t('volunteerListings.viewDetails') }}
          </button>
        </div>
      </div>
    </div>
  </main>
</template>
