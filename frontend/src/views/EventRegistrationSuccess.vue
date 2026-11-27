
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Check,
  CalendarDays,
  MapPin,
  CalendarPlus,
  ArrowRight,
  Loader2
} from 'lucide-vue-next'
import { getAnnouncementDetail } from '@/services/api'
import { authState } from '@/auth'

const route = useRoute()
const router = useRouter()

const event = ref(null)
const loading = ref(true)
const error = ref('')

// Use the current user's available profile data as a fallback.
// A registration API should supply the saved registration record.
const registration = ref({
  full_name: authState.profile?.fullName || '',
  contact_number: authState.profile?.mobileNumber || '',
  email: authState.email || '',
  age: ''
})

const eventTitle = computed(
  () => event.value?.title ||
        event.value?.announcement_title ||
        'Event'
)

const eventLocation = computed(
  () => event.value?.location ||
        event.value?.venue ||
        'Location to be announced'
)

const formattedDate = computed(() => {
  const date = event.value?.starts_on || event.value?.start_date

  if (!date) return 'Date to be announced'

  const parsedDate = new Date(date)

  if (Number.isNaN(parsedDate.getTime())) return date

  return parsedDate.toLocaleString('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
})

const confirmationNumber = computed(
  () => registration.value?.name ||
        registration.value?.registration_id ||
        registration.value?.event_registration ||
        'Registration confirmed'
)

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

    if (!event.value || typeof event.value !== 'object') {
      throw new Error('Event details could not be loaded.')
    }
  } catch (e) {
    error.value = e.message || 'Unable to load event details.'
  } finally {
    loading.value = false
  }
})

function addToCalendar() {
  const start = event.value?.starts_on || event.value?.start_date

  if (!start) return

  const startDate = new Date(start)
  if (Number.isNaN(startDate.getTime())) return

  const endDate = new Date(startDate.getTime() + 2 * 60 * 60 * 1000)

  const formatDate = date =>
    date.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')

  const escapeText = value =>
    String(value || '')
      .replace(/\\/g, '\\\\')
      .replace(/,/g, '\\,')
      .replace(/;/g, '\\;')
      .replace(/\n/g, '\\n')

  const content = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Samaaja//Event Registration//EN',
    'BEGIN:VEVENT',
    `UID:${confirmationNumber.value}@samaaja`,
    `DTSTAMP:${formatDate(new Date())}`,
    `DTSTART:${formatDate(startDate)}`,
    `DTEND:${formatDate(endDate)}`,
    `SUMMARY:${escapeText(eventTitle.value)}`,
    `LOCATION:${escapeText(eventLocation.value)}`,
    'END:VEVENT',
    'END:VCALENDAR'
  ].join('\r\n')

  const blob = new Blob([content], {
    type: 'text/calendar;charset=utf-8'
  })

  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'event-registration.ics'
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}

function exploreMore() {
  router.push({ name: 'announcements' })
}
</script>

<template>
  <main class="mx-auto max-w-2xl space-y-5 px-4 py-6">
    <div v-if="loading" class="flex justify-center py-10">
      <Loader2 class="h-7 w-7 animate-spin text-primary-600" />
    </div>

    <p v-else-if="error" class="text-sm text-red-600">
      {{ error }}
    </p>

    <div v-else class="success-page">
      <div class="success-content">
        <div class="success-icon">
          <Check :size="34" :stroke-width="2.5" />
        </div>

        <h1>Registration Confirmed!</h1>
        <p class="subtitle">You're all set for the event.</p>

        <section class="details-card">
          <h2>{{ t('eventDetails.eventDetailsTitle') }}</h2>

          <div class="detail-row">
            <div class="detail-icon">
              <CalendarDays :size="19" />
            </div>
            <div>
              <p class="detail-label">Date &amp; Time</p>
              <p class="detail-value">{{ formattedDate }}</p>
            </div>
          </div>

          <div class="detail-row">
            <div class="detail-icon">
              <MapPin :size="19" />
            </div>
            <div>
              <p class="detail-label">Location</p>
              <p class="detail-value">{{ eventLocation }}</p>
            </div>
          </div>
        </section>

        <section class="details-card">
          <h2>YOUR REGISTRATION</h2>

          <div class="registration-row">
            <span>Name</span>
            <strong>{{ registration.full_name || 'Not available' }}</strong>
          </div>

          <div class="registration-row">
            <span>Age</span>
            <strong>{{ registration.age || 'Not available' }}</strong>
          </div>

          <div class="registration-row">
            <span>Contact</span>
            <strong>{{ registration.contact_number || 'Not available' }}</strong>
          </div>

          <div class="registration-row">
            <span>Email</span>
            <strong>{{ registration.email || 'Not available' }}</strong>
          </div>
        </section>

        <div class="confirmation-box">
          <p>CONFIRMATION NUMBER</p>
          <strong>{{ confirmationNumber }}</strong>
        </div>
      </div>

      <footer class="success-actions">
        <button
          class="primary-button"
          type="button"
          :disabled="!event?.starts_on && !event?.start_date"
          @click="addToCalendar"
        >
          <CalendarPlus :size="18" />
          Add to Calendar
        </button>

        <button
          class="secondary-button"
          type="button"
          @click="exploreMore"
        >
          Explore More
          <ArrowRight :size="17" />
        </button>
      </footer>
    </div>
  </main>
</template>

<style scoped>
.success-page {
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  overflow: hidden;
  background: #f8f9fb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  color: #111827;
}

.success-content {
  padding: 28px 16px 16px;
}

.success-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #3674f9;
  color: white;
  border-radius: 50%;
}

h1 {
  margin: 0;
  text-align: center;
  font-size: 21px;
  font-weight: 700;
}

.subtitle {
  margin: 5px 0 28px;
  color: #6b7280;
  font-size: 13px;
  text-align: center;
}

.details-card {
  margin-bottom: 16px;
  padding: 16px 13px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 11px;
}

.details-card h2 {
  margin: 0 0 14px;
  color: #6b7280;
  font-size: 11px;
  font-weight: 700;
}

.detail-row {
  display: flex;
  align-items: flex-start;
  gap: 11px;
}

.detail-row + .detail-row {
  margin-top: 14px;
}

.detail-icon {
  flex-shrink: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3674f9;
  background: #eaf2ff;
  border-radius: 7px;
}

.detail-label {
  margin: 1px 0 4px;
  color: #6b7280;
  font-size: 11px;
}

.detail-value {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  overflow-wrap: anywhere;
}

.registration-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 0;
  font-size: 12px;
}

.registration-row span {
  color: #6b7280;
}

.registration-row strong {
  text-align: right;
  overflow-wrap: anywhere;
}

.confirmation-box {
  padding: 16px 10px;
  text-align: center;
  background: #eaf2ff;
  border-radius: 7px;
}

.confirmation-box p {
  margin: 0 0 6px;
  font-size: 10px;
  font-weight: 600;
}

.confirmation-box strong {
  color: #3674f9;
  font-size: 15px;
  overflow-wrap: anywhere;
}

.success-actions {
  display: grid;
  gap: 8px;
  padding: 14px 16px 18px;
  border-top: 1px solid #e5e7eb;
}

.primary-button,
.secondary-button {
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 0;
  border-radius: 7px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.primary-button {
  background: #3674f9;
  color: white;
}

.primary-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.secondary-button {
  background: #eaf2ff;
  color: #17396d;
}
</style>
