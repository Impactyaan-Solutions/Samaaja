<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ArrowLeft, Share2, Loader2 } from 'lucide-vue-next'

import { getVolunteerOpportunity } from '@/services/api'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()
const opportunity = ref(null)
const loading = ref(true)
const error = ref(null)
const shareError = ref(null)

const formatDate = (timeStr) => {
  if (!timeStr) return ""
  const date = new Date(timeStr)
  return date.toLocaleDateString(
    locale.value === 'hi' ? 'hi-IN' : 'en-US',
    { day: "2-digit", month: "short", year: "numeric" }
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
    params: { id: route.params.id }
  })
}

onMounted(() => {
  fetchOpportunity()
})
</script>

<template>
  <div class="min-h-full bg-gray-50">
    <main class="mx-auto max-w-4xl px-4 pb-28 pt-6">
      <!-- Loading -->
      <div
        v-if="loading"
        class="flex flex-col items-center justify-center px-5 pt-16 text-center"
      >
        <Loader2
          class="mb-3 h-7 w-7 animate-spin text-primary-500"
        />

        <p class="text-sm text-gray-500">
          {{ t('volunteerOpportunityDetail.loading') }}
        </p>
      </div> 

      <!-- Error -->
      <div
        v-else-if="error"
        class="flex min-h-[60vh] items-center justify-center text-red-500"
      >
        {{ error }}
      </div>

      <!-- Opportunity -->
      <div v-else-if="opportunity">
      <!-- Header -->
      <header
        class="sticky top-0 z-20 flex items-center border-b border-gray-50 bg-white px-5 py-5"
      >
        <button
          type="button"
          @click="router.back()"
          class="-ml-2 rounded-full p-2 transition-colors hover:bg-gray-100"
        >
          <ArrowLeft class="h-6 w-6 text-gray-800" />
        </button>

        <h2 class="mx-auto -ml-2 text-lg font-bold text-gray-900">
          {{ t('volunteerOpportunityDetail.headerTitle') }}
        </h2>

        <button
          type="button"
          class="rounded-full p-2 transition-colors hover:bg-gray-100"
          :aria-label="t('volunteerOpportunityDetail.share')"
          @click="shareOpportunity"
        >
          <Share2 class="h-5 w-5 text-gray-800" />
        </button>
      </header>

      <div
        v-if="shareError"
        class="mb-3 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600"
      >
        {{ shareError }}
      </div>

        <!-- Opportunity Title Card -->
        <div class="rounded-2xl bg-white p-5 shadow-sm">
          <div class="mb-3">
            <span
              class="inline-flex rounded-full bg-primary-50 px-3 py-1 text-xs font-medium text-primary-600"
            >
              {{ opportunity.category || t('volunteerListings.community') }}
            </span>
          </div>
          <h1 class="text-xl font-bold text-gray-900">
            {{ opportunity.title || t('volunteerListings.opportunity') }}
          </h1>
          <div class="mt-3 flex items-center gap-2 text-sm text-gray-500">
            <span>{{ opportunity.location || t('volunteerListings.location') }}</span>
          </div>
        </div>

        <!-- About this Opportunity -->
        <div class="mt-5 rounded-2xl bg-white p-5 shadow-sm">
          <h2 class="text-sm font-semibold text-gray-900">
            {{ t('volunteerOpportunityDetail.aboutOpportunity') }}
          </h2>

          <p class="mt-3 text-sm leading-6 text-gray-600">
            {{ opportunity.description || t('volunteerListings.opportunity') }}
          </p>
        </div>
        <!-- What is Expected -->
        <div class="mt-5 rounded-2xl bg-white p-5 shadow-sm">
          <h2 class="text-sm font-semibold text-gray-900">
           {{ t('volunteerOpportunityDetail.whatIsExpected') }}
          </h2>
          <div class="mt-4 space-y-3 text-sm">
            <div class="flex">
              <span class="w-28 text-gray-500">
                {{ t('volunteerOpportunityDetail.time') }}
              </span>
              <span class="text-gray-900">
                {{ opportunity.expected_time_commitment }}
              </span>
            </div>

            <div class="flex">
             <span class="w-28 text-gray-500">
               {{ t('volunteerOpportunityDetail.start') }}
             </span>
             <span class="text-gray-900">
               {{ formatDate(opportunity.start_date) }}
             </span>
            </div>

            <div class="flex">
             <span class="w-28 text-gray-500">
               {{ t('volunteerOpportunityDetail.end') }}
             </span>
             <span class="text-gray-900">
               {{ formatDate(opportunity.end_date) }}
             </span>
            </div>

            <div class="flex">
             <span class="w-28 text-gray-500">
               {{ t('volunteerOpportunityDetail.format') }}
             </span>
             <span class="text-gray-900">
               {{ opportunity.volunteer_format }}
             </span>
            </div>

            <div class="flex">
             <span class="w-28 text-gray-500">
               {{ t('volunteerOpportunityDetail.compensation') }}
             </span>
             <span class="text-gray-900">
               {{ opportunity.compensation_type }}
             </span>
            </div>
           </div>
          </div>
        <!-- Skills Needed -->
         <div class="mt-5 rounded-2xl bg-white p-5 shadow-sm">
           <h2 class="text-sm font-semibold text-gray-900">
             {{ t('volunteerOpportunityDetail.skillsNeeded') }}
           </h2>

         <div class="mt-4 flex flex-wrap gap-2">
           <span
             v-for="skill in opportunity.skills_needed"
             :key="skill"
             class="rounded-md bg-gray-100 px-3 py-1.5 text-xs text-gray-600"
           >
             {{ skill }}
           </span>
          </div>
         </div>

         <!-- What happens after I apply -->
          <div class="mt-5 rounded-2xl bg-white p-5 shadow-sm">
            <h2 class="text-sm font-semibold text-gray-900">
              {{ t('volunteerOpportunityDetail.whatHappensAfterApply') }}
            </h2>

            <p class="mt-3 text-sm leading-6 text-gray-600">
              {{ t('volunteerOpportunityDetail.afterApplyDescription') }}
            </p>
         </div>

         <!-- Apply Now -->
         <button
           type="button"
           @click="applyForOpportunity"
           class="fixed bottom-32 left-1/2 z-30 w-[calc(100%-2rem)] max-w-md -translate-x-1/2 rounded-lg bg-primary-600 px-6 py-3 text-base font-semibold text-white shadow-lg transition hover:bg-primary-700"
         >
           {{ t('volunteerOpportunityDetail.applyNow') }}
         </button>

      </div>
    </main>
  </div>
</template>
