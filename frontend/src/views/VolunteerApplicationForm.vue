<script setup>
import { nextTick, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ArrowLeft, Loader2 } from 'lucide-vue-next'
import { authState } from '@/auth'
import {
  checkVolunteerApplication,
  getVolunteerOpportunity,
  applyForVolunteerOpportunity
} from '@/services/api'
import Form from '@/components/common/Form.vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const volunteerOpportunityId = route.params.id
const opportunity = ref(null)

const loading = ref(true)
const alreadyApplied = ref(false)
const error = ref(null)
const success = ref(null)
const fields = ref([
  {
    key: 'fullName',
    label: t('volunteerApplication.fullName'),
    type: 'text',
    value: authState.profile.fullName,
    editable: false,
    required: true
  },
  {
    key: 'email',
    label: t('volunteerApplication.email'),
    type: 'email',
    value: authState.email,
    editable: false,
    required: true
  },
  {
    key: 'phoneNumber',
    label: t('volunteerApplication.phoneNumber'),
    type: 'tel',
    value: authState.profile.mobileNumber,
    editable: false,
    required: true    
  },
  {
    key: 'gender',
    label: t('volunteerApplication.gender'),
    type: 'text',
    value: authState.profile.gender,
    editable: false,
    required: true
  },
  {
    key: 'age',
    label: t('volunteerApplication.age'),
    type: 'number',
    editable: true,
    required: true
  },
  {
    key: 'preferredAvailableDays',
    label: t('volunteerApplication.preferredAvailableDays'),
    type: 'radio',
    required: true,
    options: [
      {
        value: 'Daily',
        label: t('volunteerApplication.daily')
      },
      {
        value: 'Few times a week',
        label: t('volunteerApplication.fewTimesAWeek')
      },
      {
        value: 'Only on Weekends',
        label: t('volunteerApplication.onlyOnWeekends')
      },
      {
        value: 'Flexible',
        label: t('volunteerApplication.flexible')
      }
    ]
  },
  {
    key: 'whyDoYouWantToVolunteer',
    label: t('volunteerApplication.whyVolunteer'),
    type: 'textarea',
    required: true,
    placeholder: t('volunteerApplication.whyVolunteerPlaceholder'),
    voiceInput: {
      enabled: true,
      label: t('volunteerApplication.addVoiceInput'),
      listeningLabel: t('volunteerApplication.listening'),
      stoppingLabel: t('volunteerApplication.stoppingVoiceInput'),
      notSupportedMessage: t('volunteerApplication.voiceInputNotSupported'),
      errorMessage: t('volunteerApplication.voiceInputError'),
      permissionDeniedMessage: t('volunteerApplication.voiceInputPermissionDenied')
    }
  },
  {
    key: 'privacyConsent',
    label: t('volunteerApplication.privacyConsentText'),
    type: 'consent',
    required: true,
    value: false
  }
])
const formLoading = ref(false)
const formError = ref(null)
const handleFormSubmit = async (formData) => {
  try {
    formLoading.value = true
    formError.value = null

    const result = await applyForVolunteerOpportunity({
      volunteer_opportunity: volunteerOpportunityId,
      age: formData.age,
      gender: formData.gender,
      preferred_available_days: formData.preferredAvailableDays,
      why_do_you_want_to_volunteer: formData.whyDoYouWantToVolunteer,
      privacy_consent: formData.privacyConsent
    })

    success.value =
      result.message || t('volunteerApplication.applicationSubmittedSuccess')
    await nextTick()
    document.querySelector('main')?.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  } catch (e) {
    formError.value =
      e.message || t('volunteerApplication.submitError')
  } finally {
    formLoading.value = false
  }
}

const goToVolunteerListings = () => {
  router.push('/volunteer-listings')
}

const goToHome = () => {
  router.push('/')
}
onMounted(async () => {
  try {
    const result = await checkVolunteerApplication(
      volunteerOpportunityId
    )

    alreadyApplied.value = result.already_applied
    opportunity.value = await getVolunteerOpportunity(
      volunteerOpportunityId
    )
  } catch (e) {
    error.value = e.message || t('volunteerApplication.loadError')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-full bg-gray-50">
    <main class="mx-auto max-w-4xl px-4 pb-28 pt-6 space-y-4">
    <div v-if="!success">
      <header
       class="sticky top-0 z-20 flex items-center border-b border-gray-50 bg-white px-5 py-5"
      >
       <button
        type="button"
        :aria-label="t('volunteerApplication.goBack')"
        @click="router.back()"
        class="-ml-2 rounded-full p-2 transition-colors hover:bg-gray-100"
      >
        <ArrowLeft class="h-6 w-6 text-gray-800" />
      </button>
       <h2 class="mx-auto -ml-2 text-lg font-bold text-gray-900">
         {{ t('volunteerApplication.headerTitle') }}
      </h2>
     </header>
     <div 
       v-if="opportunity" 
       class="rounded-lg bg-white p-4 shadow-sm"
     >
       <p class="text-sm text-gray-500">
         {{ t('volunteerApplication.applyingFor') }}
       </p>

       <h1 class="mt-1 text-lg font-semibold text-gray-900">
         {{ opportunity.title }}
       </h1>
     </div>
    </div>

    <div
      v-if="loading"
      class="flex flex-col items-center justify-center px-5 pt-16 text-center"
    >
      <Loader2
        class="mb-3 h-7 w-7 animate-spin text-primary-500"
      />

      <p class="text-sm text-gray-500">
        {{ t('volunteerApplication.checkingApplicationStatus') }}
      </p>
    </div>

    <div v-else-if="error">
      <p class="text-sm text-red-600">
        {{ error }}
      </p>
    </div>

    <div v-else-if="alreadyApplied">
      <section class="rounded-lg bg-white p-6 text-center shadow-sm">
        <p class="text-base font-semibold text-gray-900">
          {{ t('volunteerApplication.alreadyApplied') }}
        </p>
      </section>
    </div>
    <div v-else-if="success">
      <h1 class="text-lg font-normal text-gray-900">
        {{ t('volunteerApplication.applicationStatus') }}
      </h1>

      <div class="space-y-3">

      <!-- Application Submitted -->
      <section class="rounded-lg bg-white p-6 text-center shadow-sm">
        <div class="mb-3 text-center text-4xl font-light text-green-600">
          ✓
        </div>

        <h2 class="text-base font-semibold text-gray-900">
          {{ t('volunteerApplication.applicationSubmitted') }}
        </h2>

        <p class="mt-2 text-sm leading-5 text-gray-500">
         {{ t('volunteerApplication.applicationSubmittedDescription') }}
        </p>
      </section>

      <!-- Applicant Status -->
      <section class="rounded-lg bg-white px-4 py-5 shadow-sm">
        <div class="flex items-center justify-between">
          <p class="text-sm font-semibold text-gray-900">
            {{ authState.profile.fullName }}
          </p>

          <span class="flex items-center gap-2 rounded-lg bg-gray-100 px-3 py-1 text-xs font-medium text-gray-500">
            <span class="h-2 w-2 rounded-full bg-amber-500"></span>
            {{ t('volunteerApplication.underReview') }}
          </span>
        </div>
      </section>

      <!-- Application Summary -->
      <section class="rounded-lg bg-white px-4 py-5 shadow-sm">
        <h2 class="mb-4 text-xs font-semibold uppercase text-gray-500">
          {{ t('volunteerApplication.applicationSummary') }}
        </h2>

        <div class="space-y-3 text-sm">
          <div class="grid grid-cols-[96px_1fr] gap-4">
            <span class="text-gray-500">
              {{ t('volunteerApplication.organisation') }}
            </span>
            <span class="text-left text-gray-900">
              {{ opportunity?.organization || '-' }}
            </span>
          </div>

          <div class="grid grid-cols-[96px_1fr] gap-4">
            <span class="text-gray-500">
              {{ t('volunteerApplication.opportunity') }}
            </span>
            <span class="text-left text-gray-900">
              {{ opportunity?.title || '-' }}
            </span>
          </div>

          <div class="grid grid-cols-[96px_1fr] gap-4">
            <span class="text-gray-500">
              {{ t('volunteerApplication.contactVia') }}
            </span>
            <span class="text-left text-gray-900">
              {{ authState.email }}<br />
              {{ authState.profile.mobileNumber }}
            </span>
          </div>
        </div>
      </section>

      <!-- What happens next -->
      <section class="rounded-lg bg-white px-4 py-5 shadow-sm">
        <h2 class="mb-2 text-xs font-semibold uppercase text-gray-500">
          {{ t('volunteerApplication.whatHappensNext') }}
        </h2>

        <p class="text-sm leading-5 text-gray-700">
          {{ t('volunteerApplication.whatHappensNextDescription') }}
        </p>
      </section>
    </div>
    
  </div>
    <div
      v-if="alreadyApplied || success"
      class="space-y-4"
    >
      <button
        type="button"
        @click="goToVolunteerListings"
        class="w-full rounded-lg bg-primary-600 px-6 py-4 text-base font-semibold text-white"
      >
        {{ t('volunteerApplication.browseMoreOpportunities') }}
      </button>

      <button
        type="button"
        @click="goToHome"
        class="w-full rounded-lg border border-primary-600 bg-white px-6 py-4 text-base font-semibold text-primary-600"
      >
        {{ t('volunteerApplication.returnToHome') }}
      </button>
    </div>
    <div
      v-if="!loading && !error && !alreadyApplied && !success"
    >
    
  
      <Form
        :fields="fields"
        :submit-label="t('volunteerApplication.submit')"
        :loading="formLoading"
        :error="formError"
        @submit="handleFormSubmit"
      />
    </div>
  </main>
</div>
</template>