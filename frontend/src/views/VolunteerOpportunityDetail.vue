<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  ArrowLeft,
  Share2,
  Loader2,
  Leaf,
  MapPin,
  Globe,
  CalendarDays,
  Clock3,
  MapPinned,
  Wrench,
} from 'lucide-vue-next'

import { getVolunteerOpportunity } from '@/services/api'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

const opportunity = ref(null)
const loading = ref(true)
const error = ref(null)
const shareError = ref(null)

const formatDate = (timeStr) => {
  if (!timeStr) return ''

  const date = new Date(timeStr)

  return date.toLocaleDateString(
    locale.value === 'hi' ? 'hi-IN' : 'en-US',
    { day: '2-digit', month: 'short', year: 'numeric' }
  )
}

const fetchOpportunity = async () => {
  try {
    loading.value = true
    error.value = null

    const result = await getVolunteerOpportunity(route.params.id)
    opportunity.value = result
  } catch (e) {
    error.value = e.message || t('volunteerOpportunityDetail.loadError')
  } finally {
    loading.value = false
  }
}

const shareOpportunity = async () => {
  const url = window.location.href

  try {
    await navigator.clipboard.writeText(url)
    alert(t('volunteerOpportunityDetail.linkCopied'))
  } catch (e) {
    console.error('Failed to copy link:', e)
    shareError.value = t('volunteerOpportunityDetail.shareError')
  }
}

const applyForOpportunity = () => {
  router.push({
    name: 'volunteer-application',
    params: { id: route.params.id },
  })
}

onMounted(() => {
  fetchOpportunity()
})
</script>

<template>
  <div class="min-h-full bg-[#f4f9f5] text-[#17251a]">
    <!-- Header -->
    <header
      class="sticky top-0 z-20 flex items-center border-b border-[#e1eee3] bg-white px-5 py-4"
    >
      <button
        type="button"
        @click="router.back()"
        class="-ml-1 rounded-xl bg-[#edf5ef] p-2.5 transition hover:bg-[#e0eee3]"
        aria-label="Go back"
      >
        <ArrowLeft class="h-5 w-5 text-[#243d2b]" />
      </button>

      <div class="mx-auto flex items-center gap-2">
        <span
          class="flex h-8 w-8 items-center justify-center rounded-full bg-[#198b45]"
        >
          <Leaf class="h-4 w-4 text-white" />
        </span>
        <span class="text-xl font-extrabold tracking-tight text-[#198b45]">
          samaaja
        </span>
      </div>

      <button
        type="button"
        class="rounded-xl bg-[#edf5ef] p-2.5 transition hover:bg-[#e0eee3]"
        :aria-label="t('volunteerOpportunityDetail.share')"
        @click="shareOpportunity"
      >
        <Share2 class="h-5 w-5 text-[#52705a]" />
      </button>
    </header>

    <main class="mx-auto max-w-4xl pb-40">
      <!-- Loading -->
      <div
        v-if="loading"
        class="flex min-h-[55vh] flex-col items-center justify-center px-5 text-center"
      >
        <Loader2 class="mb-3 h-8 w-8 animate-spin text-[#198b45]" />
        <p class="text-sm text-[#617565]">
          {{ t('volunteerOpportunityDetail.loading') }}
        </p>
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="flex min-h-[55vh] items-center justify-center px-5 text-center text-red-600"
      >
        {{ error }}
      </div>

      <!-- Opportunity -->
      <div v-else-if="opportunity">
        <!-- Opportunity title and metadata -->
        <section class="border-b border-[#e0eee2] bg-white px-5 pb-5 pt-6">
          <h1 class="text-2xl font-extrabold leading-tight tracking-tight text-[#17251a]">
            {{ opportunity.title || t('volunteerListings.opportunity') }}
          </h1>

          <div class="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-[#617565]">
            <span
              v-if="opportunity.location"
              class="inline-flex items-center gap-1.5"
            >
              <MapPin class="h-4 w-4 shrink-0 text-[#198b45]" />
              {{ opportunity.location }}
            </span>

            <span
              v-if="opportunity.volunteer_format"
              class="inline-flex items-center gap-1.5"
            >
              <Globe class="h-4 w-4 shrink-0 text-[#198b45]" />
              {{ opportunity.volunteer_format }}
            </span>
          </div>

          <div v-if="opportunity.category" class="mt-4 flex flex-wrap gap-2">
            <span
              class="inline-flex items-center rounded-full bg-[#e4f4e8] px-3 py-1.5 text-xs font-semibold text-[#198b45]"
            >
              <Leaf class="mr-1 h-3.5 w-3.5" />
              {{ opportunity.category }}
            </span>
          </div>

          <div
            v-if="shareError"
            class="mt-4 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600"
          >
            {{ shareError }}
          </div>
        </section>

        <!-- Information cards -->
        <section class="grid grid-cols-1 gap-3 px-4 py-5 sm:grid-cols-2">
          <!-- Date range -->
          <div class="min-w-0 rounded-2xl border border-[#d5ead9] bg-white p-4">
            <span class="mb-2 flex h-9 w-9 items-center justify-center rounded-xl bg-[#e5f4e9]">
              <CalendarDays class="h-5 w-5 text-[#198b45]" />
            </span>

            <p class="text-xs font-semibold uppercase tracking-wide text-[#617565]">
              DATE
            </p>

            <p class="mt-2 break-words text-sm font-bold leading-5 text-[#17251a]">
              <template v-if="opportunity.start_date && opportunity.end_date">
                {{ formatDate(opportunity.start_date).replace(/,?\s*\d{4}$/, '') }}
                – {{ formatDate(opportunity.end_date) }}
              </template>
              <template v-else-if="opportunity.start_date">
                {{ formatDate(opportunity.start_date) }}
              </template>
              <template v-else-if="opportunity.end_date">
                {{ formatDate(opportunity.end_date) }}
              </template>
              <template v-else>—</template>
            </p>
          </div>
          <!-- Time commitment -->
          <div class="min-w-0 rounded-2xl border border-[#d5ead9] bg-white p-4">
            <span class="mb-2 flex h-9 w-9 items-center justify-center rounded-xl bg-[#e5f4e9]">
              <Clock3 class="h-5 w-5 text-[#198b45]" />
            </span>

            <p class="text-xs font-semibold uppercase tracking-wide text-[#617565]">
              TIME COMMITMENT
            </p>

            <p class="mt-2 break-words text-sm font-bold leading-5 text-[#17251a]">
              {{ opportunity.expected_time_commitment || '—' }}
            </p>
          </div>

          <!-- Location -->
          <div class="min-w-0 rounded-2xl border border-[#d5ead9] bg-white p-4">
            <span class="mb-2 flex h-9 w-9 items-center justify-center rounded-xl bg-[#e5f4e9]">
              <MapPinned class="h-5 w-5 text-[#198b45]" />
            </span>

            <p class="text-xs font-semibold uppercase tracking-wide text-[#617565]">
              {{ t('volunteerListings.location') }}
            </p>

            <p class="mt-2 break-words text-sm font-bold leading-5 text-[#17251a]">
              {{ opportunity.location || '—' }}
            </p>
          </div>

          <!-- Skills -->
          <div class="min-w-0 rounded-2xl border border-[#d5ead9] bg-white p-4">
            <span class="mb-2 flex h-9 w-9 items-center justify-center rounded-xl bg-[#e5f4e9]">
              <Wrench class="h-5 w-5 text-[#198b45]" />
            </span>

            <p class="text-xs font-semibold uppercase tracking-wide text-[#617565]">
              SKILLS
            </p>

            <div v-if="opportunity.skills_needed?.length" class="mt-2 flex flex-wrap gap-1.5">
              <span
                v-for="skill in opportunity.skills_needed"
                :key="skill"
                class="text-sm font-bold leading-5 text-[#17251a]"
              >
                {{ skill }}<template v-if="skill !== opportunity.skills_needed[opportunity.skills_needed.length - 1]">, </template>
              </span>
            </div>

            <p v-else class="mt-2 text-sm font-bold text-[#17251a]">—</p>
          </div>
        </section>

        <!-- About this Opportunity -->
        <section class="mt-1 border-t-8 border-[#edf5ef] bg-[#f4f9f5] px-5 py-6">
          <h2 class="text-lg font-extrabold text-[#17251a]">
            {{ t('volunteerOpportunityDetail.aboutOpportunity') }}
          </h2>

          <p class="mt-3 whitespace-pre-line text-sm leading-6 text-[#617565]">
            {{ opportunity.description || t('volunteerListings.opportunity') }}
          </p>
        </section>

        <!-- What happens after I apply: kept from existing UI -->
        <section class="mx-4 mb-6 rounded-2xl border border-[#d5ead9] bg-white p-5">
          <h2 class="text-base font-bold text-[#17251a]">
            {{ t('volunteerOpportunityDetail.whatHappensAfterApply') }}
          </h2>

          <p class="mt-3 text-sm leading-6 text-[#617565]">
            {{ t('volunteerOpportunityDetail.afterApplyDescription') }}
          </p>
        </section>

        <!-- Apply button: same route and behavior -->
        <div
          class="fixed inset-x-0 bottom-[88px] z-40 border-t border-[#dceade] bg-white/95 px-4 py-3 backdrop-blur"
        >
          <button
            type="button"
            @click="applyForOpportunity"
            class="mx-auto block w-full max-w-md rounded-xl bg-[#198b45] px-6 py-3.5 text-base font-bold text-white shadow-md transition hover:bg-[#14783a] active:scale-[0.99]"
          >
            {{ t('volunteerOpportunityDetail.applyNow') }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>