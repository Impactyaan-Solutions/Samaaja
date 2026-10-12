<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

import {
  MapPin,
  Tag,
  SlidersHorizontal,
  X,
  Loader2
} from 'lucide-vue-next'

import AppHeader from '@/components/common/AppHeader.vue'
import {
  getVolunteerListings,
  getMetadataOptions
} from '@/services/api'

const { t } = useI18n()
const router = useRouter()

const listings = ref([])
const loading = ref(true)
const error = ref(null)
const loadMoreError = ref(null)
const fetchingListings = ref(false)

const PAGE_SIZE = 10
const offset = ref(0)
const hasMore = ref(true)
const loadingMore = ref(false)

const selectedLocation = ref('')
const selectedCategory = ref('')
const selectedSkill = ref('')

const locations = ref([])
const categories = ref([])
const skills = ref([])

const showLocationFilter = ref(false)
const showCategoryFilter = ref(false)
const showSkillFilter = ref(false)

const getFilters = () => {
  return {
    locations: selectedLocation.value
      ? [selectedLocation.value]
      : [],
    categories: selectedCategory.value
      ? [selectedCategory.value]
      : [],
    skills: selectedSkill.value
      ? [selectedSkill.value]
      : []
  }
}

const performFetch = async ({ reset }) => {
  if (reset) {
    if (fetchingListings.value || loadingMore.value) return
  } else {
    if (!hasMore.value || loadingMore.value) return
  }

  const targetOffset = reset ? 0 : offset.value + PAGE_SIZE

  if (reset) {
    fetchingListings.value = true
    loading.value = true
    error.value = null
  } else {
    loadingMore.value = true
    loadMoreError.value = null
  }

  try {
    const result = await getVolunteerListings(
      getFilters(),
      PAGE_SIZE,
      targetOffset
    )

    listings.value = reset
      ? result.opportunities
      : [...listings.value, ...result.opportunities]

    offset.value = targetOffset
    hasMore.value = result.has_more
  } catch (e) {
    const message = e.message || t(
      reset 
        ? 'volunteerListings.loadError' : 
        'volunteerListings.loadMoreError'
    )

    if (reset) {
      error.value = message
    } else {
      loadMoreError.value = message
    }
    
    console.error('Failed to load more volunteer opportunities:', e)
  } finally {
    if (reset) {
      fetchingListings.value = false
      loading.value = false
    } else {
      loadingMore.value = false
    }
  }
}

const fetchListings = () => performFetch({ reset: true })
const loadMoreListings = () => performFetch({ reset: false })

const loadMoreSentinel = ref(null)
let observer = null

const setupIntersectionObserver = () => {
  if (observer) {
    observer.disconnect()
  }

  observer = new IntersectionObserver(
    (entries) => {
      if (
        entries[0].isIntersecting &&
        hasMore.value &&
        !loadingMore.value
      ) {
        loadMoreListings()
      }
    },
    {
      rootMargin: '200px'
    }
  )

  if (loadMoreSentinel.value) {
    observer.observe(loadMoreSentinel.value)
  }
}

const fetchMetadataOptions = async () => {
  try {
    const [locationOptions, categoryOptions, skillOptions] = await Promise.all([
      getMetadataOptions('Location'),
      getMetadataOptions('Category'),
      getMetadataOptions('Skill')
    ])

    locations.value = locationOptions
    categories.value = categoryOptions
    skills.value = skillOptions
  } catch (e) {
    console.error('Failed to load volunteer filter options:', e)
  }
}

onMounted(() => {
  fetchMetadataOptions()
  fetchListings()
})

watch(loadMoreSentinel, (newSentinel) => {
  if (newSentinel) {
    setupIntersectionObserver()
  }
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})


const getLocation = (item) => {
  /*
   * Location backend/doctype mapping abhi available nahi hai.
   * Isliye Figma ke according placeholder rakha hai.
   */
  if (typeof item.location === 'object') {
    return (
      item.location?.city ||
      item.location?.name ||
      t('volunteerListings.location')
    )
  }

  return item.location || t('volunteerListings.location')
}

const hasFilters = computed(() => {
  return Boolean(
    selectedLocation.value ||
    selectedCategory.value ||
    selectedSkill.value
  )
})

/* -----------------------------
   Filter toggle functions
----------------------------- */

const toggleLocationFilter = () => {
  showLocationFilter.value = !showLocationFilter.value
  showCategoryFilter.value = false
  showSkillFilter.value = false
}

const toggleCategoryFilter = () => {
  showCategoryFilter.value = !showCategoryFilter.value
  showLocationFilter.value = false
  showSkillFilter.value = false
}

const toggleSkillFilter = () => {
  showSkillFilter.value = !showSkillFilter.value
  showLocationFilter.value = false
  showCategoryFilter.value = false
}

/* -----------------------------
   Filter selection functions
----------------------------- */

const selectLocation = async (value) => {
  selectedLocation.value = value
  showLocationFilter.value = false
  offset.value = 0

  await fetchListings()
}

const selectCategory = async (value) => {
  selectedCategory.value = value
  showCategoryFilter.value = false
  offset.value = 0

  await fetchListings()
}

const selectSkill = async (value) => {
  selectedSkill.value = value
  showSkillFilter.value = false
  offset.value = 0

  await fetchListings()
}

/* -----------------------------
   Clear filters
----------------------------- */

const clearFilters = async () => {
  selectedLocation.value = ''
  selectedCategory.value = ''
  selectedSkill.value = ''

  showLocationFilter.value = false
  showCategoryFilter.value = false
  showSkillFilter.value = false
  offset.value = 0

  await fetchListings()
}

/* -----------------------------
   Description
----------------------------- */

const goToDetail = (item) => {
  if (!item.name) return

  router.push(`/volunteer-listings/${item.name}`)
}

const formatDescription = (description) => {
  if (!description) {
    return t('volunteerListings.defaultDescription')
  }

  if (description.length > 95) {
    return `${description.substring(0, 95)}...`
  }

  return description
}
</script>

<template>
  <div class="min-h-full bg-[#f7f9fb] pb-24 text-[#172033]">

    <AppHeader />

    <!-- =========================
         FILTERS
    ========================== -->
    <div class="relative px-5 pt-4">

      <div class="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-hide">

        <!-- Location -->
        <button
          @click="toggleLocationFilter"
          class="flex h-9 shrink-0 items-center gap-1.5 rounded-lg border px-3 text-xs font-medium transition"
          :class="
            selectedLocation
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 bg-white text-gray-700'
          "
        >
          <MapPin class="h-3.5 w-3.5" />

          <span>
            {{ selectedLocation || t('volunteerListings.location') }}
          </span>
        </button>

        <!-- Category -->
        <button
          @click="toggleCategoryFilter"
          class="flex h-9 shrink-0 items-center gap-1.5 rounded-lg border px-3 text-xs font-medium transition"
          :class="
            selectedCategory
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 bg-white text-gray-700'
          "
        >
          <Tag class="h-3.5 w-3.5" />

          <span>
            {{ selectedCategory || t('volunteerListings.category') }}
          </span>
        </button>

        <!-- Skills -->
        <button
          @click="toggleSkillFilter"
          class="flex h-9 shrink-0 items-center gap-1.5 rounded-lg border px-3 text-xs font-medium transition"
          :class="
            selectedSkill
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 bg-white text-gray-700'
          "
        >
          <SlidersHorizontal class="h-3.5 w-3.5" />

          <span>
            {{ selectedSkill || t('volunteerListings.skills') }}
          </span>
        </button>

        <!-- Clear filters -->
        <button
          @click="clearFilters"
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500"
          :aria-label="t('volunteerListings.clearFilters')"
        >
          <X class="h-4 w-4" />
        </button>

      </div>

      <!-- =========================
           LOCATION DROPDOWN
      ========================== -->
      <div
        v-if="showLocationFilter"
        class="absolute left-5 right-5 top-14 z-30 rounded-xl border border-gray-100 bg-white p-2 shadow-lg"
      >
        <button
          @click="selectLocation('')"
          class="w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-gray-50"
        >
          {{ t('volunteerListings.allLocations') }}
        </button>

        <button
          v-for="location in locations"
          :key="location"
          @click="selectLocation(location)"
          class="w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-gray-50"
        >
          {{ location }}
        </button>

        <div
          v-if="locations.length === 0"
          class="px-3 py-2 text-sm text-gray-400"
        >
          {{ t('volunteerListings.noLocations') }}
        </div>
      </div>

      <!-- =========================
           CATEGORY DROPDOWN
      ========================== -->
      <div
        v-if="showCategoryFilter"
        class="absolute left-5 right-5 top-14 z-30 rounded-xl border border-gray-100 bg-white p-2 shadow-lg"
      >
        <button
          @click="selectCategory('')"
          class="w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-gray-50"
        >
          {{ t('volunteerListings.allCategories') }}
        </button>

        <button
          v-for="category in categories"
          :key="category"
          @click="selectCategory(category)"
          class="w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-gray-50"
        >
          {{ category }}
        </button>

        <div
          v-if="categories.length === 0"
          class="px-3 py-2 text-sm text-gray-400"
        >
          {{ t('volunteerListings.noCategories') }}
        </div>
      </div>

      <!-- =========================
           SKILLS DROPDOWN
      ========================== -->
      <div
        v-if="showSkillFilter"
        class="absolute left-5 right-5 top-14 z-30 max-h-64 overflow-y-auto rounded-xl border border-gray-100 bg-white p-2 shadow-lg"
      >
        <button
          @click="selectSkill('')"
          class="w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-gray-50"
        >
          {{ t('volunteerListings.allSkills') }}
        </button>

        <button
          v-for="skill in skills"
          :key="skill"
          @click="selectSkill(skill)"
          class="w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-gray-50"
        >
          {{ skill }}
        </button>

        <div
          v-if="skills.length === 0"
          class="px-3 py-2 text-sm text-gray-400"
        >
          {{ t('volunteerListings.noSkills') }}
        </div>
      </div>

    </div>

    <!-- =========================
         LOADING
    ========================== -->
    <div
      v-if="loading"
      class="flex flex-col items-center justify-center px-5 pt-16 text-center"
    >
      <Loader2
        class="mb-3 h-7 w-7 animate-spin text-primary-500"
      />

      <p class="text-sm text-gray-500">
        {{ t('volunteerListings.loading') }}
      </p>
    </div>

    <!-- =========================
         ERROR
    ========================== -->
    <div
      v-else-if="error"
      class="px-5 pt-12 text-center"
    >
      <p class="text-sm text-red-500">
        {{ error }}
      </p>
    </div>

    <!-- =========================
         EMPTY
    ========================== -->
    <div
      v-else-if="listings.length === 0"
      class="px-5 pt-12 text-center"
    >
      <div
        class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-gray-100"
      >
        <SlidersHorizontal class="h-6 w-6 text-gray-400" />
      </div>

      <h3 class="mt-4 text-base font-semibold text-gray-800">
        {{ t('volunteerListings.noOpportunities') }}
      </h3>

      <p class="mt-1 text-sm text-gray-500">
        {{ t('volunteerListings.tryChangingFilters') }}
      </p>
    </div>

    <!-- =========================
         OPPORTUNITY CARDS
    ========================== -->
    <div
      v-else
      class="space-y-3 px-5 pb-6 pt-4"
    >

      <div
        v-for="item in listings"
        :key="item.name || item.title"
        class="rounded-xl border border-gray-100 bg-white p-3.5 shadow-[0_2px_10px_rgba(0,0,0,0.04)]"
      >

        <!-- Category -->
        <div
          class="inline-flex rounded-md bg-blue-50 px-2 py-1 text-[10px] font-semibold text-blue-700"
        >
          {{ item.category || t('volunteerListings.community') }}
        </div>

        <!-- Title -->
        <h2 class="mt-2 text-sm font-bold leading-5 text-gray-900">
          {{ item.title || t('volunteerListings.opportunity') }}
        </h2>

        <!-- Description -->
        <p class="mt-1.5 text-xs leading-5 text-gray-500">
          {{ formatDescription(item.description) }}
        </p>

        <!-- Bottom row -->
        <div class="mt-3 flex items-center justify-between gap-3">

          <!-- Location -->
          <div
            class="flex min-w-0 items-center gap-1.5 text-xs text-gray-500"
          >
            <MapPin
              class="h-3.5 w-3.5 shrink-0 text-gray-400"
            />

            <span class="truncate">
              {{ getLocation(item) }}
            </span>
          </div>

          <!-- View Details -->
          <button
            @click="goToDetail(item)"
            class="shrink-0 rounded-md bg-primary-600 px-4 py-2 text-[11px] font-semibold text-white transition hover:bg-primary-700"
            
          >
            {{ t('volunteerListings.viewDetails') }}
          </button>

        </div>

      </div>
      <!-- Infinite Scroll Trigger -->
      <div
        ref="loadMoreSentinel"
        class="flex items-center justify-center py-8"
      >
        <!-- Loading more -->
        <Loader2
          v-if="loadingMore"
          class="h-6 w-6 animate-spin text-primary-500"
        />

        <!-- Load more error -->
        <p
          v-else-if="loadMoreError"
          class="text-xs text-red-500"
        >
          {{ loadMoreError }}
        </p>

        <!-- No more opportunities -->
        <p
          v-else-if="!hasMore"
          class="text-sm text-gray-400"
        >
          {{ t('volunteerListings.noMoreOpportunities') }}
        </p>
      </div>

    </div>

  </div>
</template>