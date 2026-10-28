<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Loader2 } from 'lucide-vue-next'
import {
  getAnnouncementDetail,
  registerForEvent
} from '@/services/api'
import { authState } from '@/auth'
import { useI18n } from 'vue-i18n'
import Form from '@/components/common/Form.vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const event = ref(null)
const loading = ref(true)
const formLoading = ref(false)
const error = ref('')
const formError = ref(null)
const success = ref(null)

const fields = ref([
  {
    key: 'full_name',
    label: 'Full Name',
    type: 'text',
    value: authState.profile.fullName,
    editable: false,
    required: true
  },
  {
    key: 'age',
    label: 'Age',
    type: 'number',
    min: 18,
    required: true
  },
  {
    key: 'contact_number',
    label: 'Contact Number',
    type: 'tel',
    value: authState.profile.mobileNumber,
    editable: false,
    required: true
  },
  {
    key: 'email',
    label: 'Email (Optional)',
    type: 'email',
    value: authState.email,
    editable: false,
    required: false
  }
])

onMounted(async () => {
  try {
    const result = await getAnnouncementDetail(route.params.id)

    event.value =
      result?.data?.data ||
      result?.data?.message?.data ||
      result?.message?.data ||
      result?.data ||
      result?.message ||
      result
  } catch (e) {
    error.value = e.message || 'Unable to load event details.'
  } finally {
    loading.value = false
  }
})

const handleFormSubmit = async (formData) => {
  try {
    formLoading.value = true
    formError.value = null
    if (!event.value?.event_id) {
  throw new Error('Event ID is missing.')
}
    const result = await registerForEvent({
      event: event.value.event_id
    })

    success.value = result.message || 'Registration successful!'
  } catch (e) {
    formError.value =
      e.message || 'Failed to register for the event.'
  } finally {
    formLoading.value = false
  }
}

const goBack = () => router.back()
const exploreMore = () => router.push({ name: 'announcements' })
</script>

<template>
  <main class="mx-auto max-w-2xl space-y-5 px-4 py-6">
    <header class="flex items-center gap-3">
      <button
        type="button"
        @click="goBack"
        aria-label="Go back"
        class="rounded-lg bg-white p-2"
      >
        <ArrowLeft class="h-5 w-5" />
      </button>

      <h1 class="text-lg font-bold text-gray-900">
        {{ t('eventRegistration.headerTitle') }}
      </h1>
    </header>

    <div
      v-if="loading"
      class="flex justify-center py-10"
    >
      <Loader2 class="h-7 w-7 animate-spin text-primary-600" />
       <span class="sr-only">
        {{ t('eventRegistration.loading') }}
      </span>
    </div>

    <p v-else-if="error" class="text-sm text-red-600">
      {{ error }}
    </p>

    <template v-else-if="event && !success">
      <section class="rounded-lg bg-primary-600 p-5 text-white">
        <p class="text-xs uppercase">
         {{ event.event_format || t('eventRegistration.eventType') }}
        </p>

        <h2 class="mt-2 text-xl font-bold">
          {{ event.title }}
        </h2>

        <p class="mt-2 text-sm">
          {{ event.location || t('eventRegistration.locationToBeAnnounced') }}
        </p>
      </section>

      <section class="rounded-lg bg-white p-5 shadow-sm">
        <h2 class="mb-5 font-semibold text-gray-900">
        {{ t('eventRegistration.yourDetails') }}
        </h2>

        <Form
          :fields="fields"
          submit-label="Confirm Registration"
          :loading="formLoading"
          :error="formError"
          @submit="handleFormSubmit"
        />
      </section>
    </template>

    <section
      v-else-if="success"
      class="rounded-lg bg-white p-6 text-center shadow-sm"
    >
      <div class="mb-3 text-4xl text-green-600">✓</div>

      <h2 class="text-xl font-bold text-gray-900">
        {{ t('eventRegistration.registrationConfirmed') }}
      </h2>

      <p class="mt-2 text-sm text-gray-500">
        {{ t('eventRegistration.successDescription') }}
      </p>

      <h3 class="mt-5 font-semibold">
        {{ event?.title }}
      </h3>

      <button
        type="button"
        @click="exploreMore"
        class="mt-6 w-full rounded-lg bg-primary-600 px-5 py-3 font-semibold text-white"
      >
       {{ t('eventRegistration.exploreMore') }}
      </button>
    </section>
  </main>
</template>