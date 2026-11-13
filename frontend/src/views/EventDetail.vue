<script setup>
import { computed, ref, onMounted, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import {
  ArrowLeft,
  Share2,
  CalendarDays,
  MapPin,
  Users,
  ArrowRightCircle,
} from "lucide-vue-next"
import { getAnnouncementDetail , checkRegisterForEvent ,getEventDetail } from "@/services/api"
import { useI18n } from "vue-i18n"


const { t, locale } = useI18n()
const route = useRoute()
const router = useRouter()
const event = ref(null)
const loading = ref(true)
const error = ref("")
const registering = ref(false)

// Fetch the selected announcement/event using its document name.
const loadEvent = async () => {
  loading.value = true
  error.value = ""
  event.value = null

  try {
    console.log("this is " ,route.name)
    let result

    if (route.name === "event-detail") {
      // Fetch from Event DocType
      result = await getEventDetail(route.params.id)
    } else if (route.name === "announcement-detail") {
      // Fetch from Announcement DocType
      result = await getAnnouncementDetail(route.params.id)
    }
    const candidates = [
      result?.data?.data,
      result?.data?.message?.data,
      result?.message?.data,
      result?.message?.message?.data,
      result?.data,
      result,
    ]

    const details = candidates.find(
      (item) =>
        item &&
        typeof item === "object" &&
        !Array.isArray(item) &&
        item.name
    )

    if (details) {
      event.value = details
    } else {
      error.value =
        result?.data?.message ||
        result?.message ||
        "Event not found or is no longer available."
    }
  } catch (err) {
    console.error("Failed to load event details:", err)
    error.value = "Unable to load event details. Please try again."
  } finally {
    loading.value = false
  }
}
onMounted(loadEvent)

// Reload when navigating from one event to another.
watch(() => route.params.id, loadEvent)

const eventTitle = computed(
  () => event.value?.title || "Event Details"
)

const eventFormat = computed(
  () => event.value?.event_format || "Offline"
)

const eventLocation = computed(
  () => event.value?.location || "Location to be announced"
)

const eventDate = computed(() => {
  const value = event.value?.starts_on || event.value?.valid_from

  if (!value) return "Date to be announced"

  const date = new Date(String(value).replace(" ", "T"))

  if (Number.isNaN(date.getTime())) {
    return "Date to be announced"
  }

  return date.toLocaleString(
    locale.value === "hi" ? "hi-IN" : "en-IN",
    {
      weekday: "long",
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }
  )
})

const eventDescription = computed(
  () =>
    event.value?.message ||
    "More information about this event will be available soon."
)

const goBack = () => {
  router.push({ name: "announcements" })
}

const shareEvent = async () => {
  const shareData = {
    title: eventTitle.value,
    text: eventTitle.value,
    url: window.location.href,
  }

  try {
    if (navigator.share) {
      await navigator.share(shareData)
    } else if (navigator.clipboard) {
      await navigator.clipboard.writeText(shareData.url)
      window.alert("Event link copied!")
    } else {
      window.prompt("Copy this event link:", shareData.url)
    }
  } catch (err) {
    if (err.name !== "AbortError") {
      console.error("Unable to share event:", err)
    }
  }
}

const registerEvent = async (item) => {
  if (item.type !== "Event") {
    return
  }
  try {
    registering.value = true
    const result = await checkRegisterForEvent(item.name)
   console.log("Full result:", result)
    const isRegistered = result?.registered
    console.log("Is registered:", isRegistered)
    if (isRegistered===true) {
    console.log("this will render on another page")
      router.push({
        name: "event-registerd",
        params: { id: item.name }
      })
    } else {
      router.push({
        name: "event-register",
        params: { id: item.name }
      })
    }
  } catch (e) {
    console.error("Failed to check event registration:", e)
    error.value = e.message || "Unable to check registration status."
  } finally {
    registering.value = false
  }
}
const exploreMore = () => {
  router.push({ name: "announcements" })
}

const announcementType = computed(
  () => event.value?.type ||
        event.value?.type ||
        "General"
)

const eventAction = computed(() => {
  if (announcementType.value !== "Event") {
    return "none"
  }

  const now = new Date()

  const startValue = event.value?.starts_on || event.value?.valid_from
  const endValue = event.value?.ends_on || event.value?.valid_to

  if (!startValue) {
    return "register"
  }

  const start = new Date(String(startValue).replace(" ", "T"))
  const end = endValue
    ? new Date(String(endValue).replace(" ", "T"))
    : null

  if (Number.isNaN(start.getTime())) {
    return "register"
  }

  // Event is on today's date: show Check-in.
  const isToday =
    start.getFullYear() === now.getFullYear() &&
    start.getMonth() === now.getMonth() &&
    start.getDate() === now.getDate()

  if (isToday) {
    return "checkin"
  }

  // Event is currently in progress.
  if (end && !Number.isNaN(end.getTime()) &&
      now >= start && now <= end) {
    return "checkin"
  }

  // Event has already ended.
  if (end && !Number.isNaN(end.getTime()) && now > end) {
    return "none"
  }

  // Event is in the future.
  if (now < start) {
    return "register"
  }

  return "none"
})
function goToCheckIn(event) {
console.log("clciked")
  if ( event.checked_in) return

  router.push({
    name: "event-checkin",
    params: {
      id: event.event_id,
    },
  })
}
</script>

<template>
  <div class="page-wrapper bg-gray-50 text-body">
    <!-- Loading -->
    <div
      v-if="loading"
      class="loading-state"
    >
      <CalendarDays class="loading-icon text-blue-500" />
      <p>{{ t('eventDetails.loading') }}</p>
    </div>

    <!-- Error -->
    <div
      v-else-if="error"
      class="error-state"
    >
      <CalendarDays class="error-icon" />

      <h2 class="error-title">
          {{ t('eventDetails.loadErrorTitle') }}
      </h2>

      <p class="error-message">
        {{ error }}
      </p>

      <div class="error-actions">
        <button
          type="button"
          @click="goBack"
          class="btn btn-secondary"
        >
          Back to Announcements
        </button>

        <button
          type="button"
          @click="loadEvent"
          class="btn btn-primary"
        >
          Retry
        </button>
      </div>
    </div>

    <!-- Event Details -->
    <template v-else-if="event">
      <!-- Header -->
      <header
        class="event-header"
      >
        <button
          type="button"
          aria-label="Back to announcements"
          @click="goBack"
          class="btn-icon bg-gray-100 hover:bg-gray-200"
        >
          <ArrowLeft class="icon-md" />
        </button>

        <h1 class="event-header-title">
         {{ t('eventDetails.headerTitle') }}
        </h1>

        <button
          type="button"
          aria-label="Share event"
          @click="shareEvent"
          class="btn-icon bg-gray-100 hover:bg-gray-200"
        >
          <Share2 class="icon-md" />
        </button>
      </header>

      <!-- Event Image -->
      <div class="event-image-container">
        <img
          v-if="event.image"
          :src="event.image"
          :alt="eventTitle"
          class="event-image"
        />

        <div
          v-else
          class="event-image-placeholder"
        >
          <CalendarDays class="placeholder-icon" />
        </div>
      </div>

      <!-- Main Content -->
      <main class="event-main-content">
        <!-- Tags -->
        <div class="event-tags">
          <span
            class="badge badge-primary"
          >
            {{ event.announcement_type || "Event" }}
          </span>

          <span
            class="badge badge-primary"
          >
            {{ eventFormat }}
          </span>
        </div>

        <!-- Title -->
        <section>
          <h2
            class="event-title"
          >
            {{ eventTitle }}
          </h2>
        </section>

        <!-- Event Information -->
        <section
          class="event-info-card"
        >
          <!-- Date -->
          <div class="info-item">
            <div class="info-icon-wrapper">
              <CalendarDays class="icon-md text-blue-600" />
            </div>

            <div class="info-content">
              <p
                class="info-label"
              >
                Date &amp; Time
              </p>

              <p class="info-value">
                {{ eventDate }}
              </p>
            </div>
          </div>

          <template v-if="announcementType === 'Event'">
            <div class="divider"></div>

            <!-- Venue -->
            <div class="info-item">
              <div class="info-icon-wrapper">
                <MapPin class="icon-md text-blue-600" />
              </div>

              <div class="info-content">
                <p
                  class="info-label"
                >
                  Venue
                </p>

                <p
                  class="info-value"
                >
                  {{ eventLocation }}
                </p>
              </div>
            </div>
          </template>

          <!-- Expected Attendees -->
          <template v-if="event.expected_attendees">
            <div class="divider"></div>

            <div class="info-item">
              <div class="info-icon-wrapper">
                <Users class="icon-md text-blue-600" />
              </div>

              <div>
                <p
                  class="info-label"
                >
                  Expected Attendees
                </p>

                <p class="info-value">
                  {{ event.expected_attendees }}
                </p>
              </div>
            </div>
          </template>
        </section>

        <!-- Description -->
        <section>
          <h3
            class="section-title"
          >
          {{ t('eventDetails.aboutEvent') }}
          </h3>

          <!-- Use text interpolation instead of v-html for safety. -->
         <div
  class="event-description"
  v-html="eventDescription"
></div>
        </section>

        <!-- Online Meeting -->
        <section
          v-if="event.online_meeting_link"
          class="meeting-link-card"
        >
          <p class="meeting-label">
            Online Meeting
          </p>

          <a
            :href="event.online_meeting_link"
            target="_blank"
            rel="noopener noreferrer"
            class="meeting-link"
          >
            Join meeting
          </a>
        </section>
      </main>

      <!-- Bottom Actions -->
      <footer
        class="event-footer"
      >
        <div class="event-footer-content">
<button
  v-if="eventAction === 'register'"
  type="button"
  @click.stop="registerEvent(event)"
  :disabled="registering || event.registered"
  :class="[
    'btn',
    event.registered
      ? 'btn-secondary cursor-not-allowed'
      : 'btn-primary'
  ]"
>
  {{
    registering
      ? t('announcements.registering')
      : event.registered
        ? t('announcements.registered')
        : t('announcements.register')
  }}
</button>

<button
  v-else-if="eventAction === 'checkin'"
  type="button"
  :disabled="event.checked_in"
   @click="goToCheckIn(event)"
  :class="[
    'btn transition-colors',
    event.checked_in
      ? 'btn-secondary cursor-not-allowed'
      : 'btn-success'
  ]"
>
  {{
    event.checked_in
      ? 'Checked In'
      : 'Check-in'
  }}
</button>


          <button
            type="button"
            @click="exploreMore"
            class="explore-btn"
          >
           {{ t('eventDetails.exploreMore') }}
          </button>
        </div>
      </footer>
    </template>
  </div>
</template>

<style scoped>
/* Loading & Error States */
.loading-state {
  @apply flex min-h-screen flex-col items-center justify-center gap-3 text-subtle;
}

.loading-icon {
  @apply h-10 w-10 animate-pulse;
}

.error-state {
  @apply flex min-h-screen flex-col items-center justify-center px-5 text-center;
}

.error-icon {
  @apply mb-3 h-12 w-12 text-muted;
}

.error-title {
  @apply text-xl font-bold text-heading;
}

.error-message {
  @apply mt-2 text-sm text-error;
}

.error-actions {
  @apply mt-5 flex gap-3;
}

/* Event Header */
.event-header {
  @apply sticky top-0 z-20 flex-between border-b border-gray-100 bg-white px-4 py-4;
}

.event-header-title {
  @apply text-base font-bold text-heading;
}

/* Event Image */
.event-image-container {
  @apply h-56 w-full overflow-hidden bg-blue-50;
}

@media (min-width: 640px) {
  .event-image-container {
    @apply h-72;
  }
}

.event-image {
  @apply h-full w-full object-cover;
}

.event-image-placeholder {
  @apply flex-center h-full bg-gradient-to-br from-blue-100 to-indigo-100;
}

.placeholder-icon {
  @apply h-16 w-16 text-blue-400;
}

/* Main Content */
.event-main-content {
  @apply mx-auto max-w-3xl px-5 py-6;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Tags */
.event-tags {
  @apply flex flex-wrap gap-2;
}

/* Title */
.event-title {
  @apply text-2xl font-bold leading-tight text-heading;
}

@media (min-width: 640px) {
  .event-title {
    @apply text-3xl;
  }
}

/* Event Info Card */
.event-info-card {
  @apply rounded-2xl border border-gray-100 bg-white p-5 shadow-sm;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  @apply flex items-start gap-3;
}

.info-icon-wrapper {
  @apply rounded-lg bg-blue-50 p-2;
}

.info-content {
  @apply min-w-0 flex-1;
}

.info-label {
  @apply text-xs font-semibold uppercase tracking-wide text-subtle;
}

.info-value {
  @apply mt-1 text-sm font-medium text-heading break-words;
}

/* Section Title */
.section-title {
  @apply mb-3 text-sm font-bold uppercase tracking-wide text-heading;
}

/* Event Description */
.event-description {
  @apply text-sm text-body mb-3;
  overflow-wrap: anywhere;
}

/* Meeting Link Card */
.meeting-link-card {
  @apply rounded-xl border border-blue-100 bg-blue-50 p-4;
}

.meeting-label {
  @apply text-sm font-semibold text-heading;
}

.meeting-link {
  @apply mt-2 inline-block break-all text-sm text-blue-700 underline;
}

/* Footer */
.event-footer {
  @apply sticky bottom-0 z-10 border-t border-gray-100 bg-white px-5 py-4;
}

.event-footer-content {
  @apply mx-auto flex max-w-3xl gap-3;
}

.explore-btn {
  @apply flex-1 rounded-xl bg-blue-50 px-4 py-3 text-sm font-semibold text-blue-900 transition;
}

.explore-btn:hover {
  @apply bg-blue-100;
}
</style>
