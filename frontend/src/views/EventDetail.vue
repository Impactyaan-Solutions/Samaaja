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
import { getAnnouncementDetail , checkRegisterForEvent } from "@/services/api"
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
    const result = await getAnnouncementDetail(route.params.id)

    // Handle Axios responses and direct API responses.
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
  try {
    registering.value = true
    const result = await checkRegisterForEvent(item.event_id)
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
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-800">
    <!-- Loading -->
    <div
      v-if="loading"
      class="flex min-h-screen flex-col items-center justify-center gap-3 text-gray-500"
    >
      <CalendarDays class="h-10 w-10 animate-pulse text-blue-500" />
      <p>{{ t('eventDetails.loading') }}</p>
    </div>

    <!-- Error -->
    <div
      v-else-if="error"
      class="flex min-h-screen flex-col items-center justify-center px-5 text-center"
    >
      <CalendarDays class="mb-3 h-12 w-12 text-gray-400" />

      <h2 class="text-xl font-bold text-gray-900">
          {{ t('eventDetails.loadErrorTitle') }}
      </h2>

      <p class="mt-2 text-sm text-red-600">
        {{ error }}
      </p>

      <div class="mt-5 flex gap-3">
        <button
          type="button"
          @click="goBack"
          class="rounded-xl bg-gray-100 px-4 py-3 text-sm font-semibold hover:bg-gray-200"
        >
          Back to Announcements
        </button>

        <button
          type="button"
          @click="loadEvent"
          class="rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    </div>

    <!-- Event Details -->
    <template v-else-if="event">
      <!-- Header -->
      <header
        class="sticky top-0 z-20 flex items-center justify-between border-b border-gray-100 bg-white px-4 py-4"
      >
        <button
          type="button"
          aria-label="Back to announcements"
          @click="goBack"
          class="rounded-xl bg-gray-100 p-2 hover:bg-gray-200"
        >
          <ArrowLeft class="h-5 w-5" />
        </button>

        <h1 class="text-base font-bold text-gray-900">
         {{ t('eventDetails.headerTitle') }}
        </h1>

        <button
          type="button"
          aria-label="Share event"
          @click="shareEvent"
          class="rounded-xl bg-gray-100 p-2 hover:bg-gray-200"
        >
          <Share2 class="h-5 w-5" />
        </button>
      </header>

      <!-- Event Image -->
      <div class="h-56 w-full overflow-hidden bg-blue-50 sm:h-72">
        <img
          v-if="event.image"
          :src="event.image"
          :alt="eventTitle"
          class="h-full w-full object-cover"
        />

        <div
          v-else
          class="flex h-full items-center justify-center bg-gradient-to-br from-blue-100 to-indigo-100"
        >
          <CalendarDays class="h-16 w-16 text-blue-400" />
        </div>
      </div>

      <!-- Main Content -->
      <main class="mx-auto max-w-3xl space-y-6 px-5 py-6">
        <!-- Tags -->
        <div class="flex flex-wrap gap-2">
          <span
            class="rounded-md bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-800"
          >
            {{ event.announcement_type || "Event" }}
          </span>

          <span
            class="rounded-md bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-800"
          >
            {{ eventFormat }}
          </span>
        </div>

        <!-- Title -->
        <section>
          <h2
            class="text-2xl font-bold leading-tight text-gray-900 sm:text-3xl"
          >
            {{ eventTitle }}
          </h2>
        </section>

        <!-- Event Information -->
        <section
          class="space-y-4 rounded-2xl border border-gray-100 bg-white p-5 shadow-sm"
        >
          <!-- Date -->
          <div class="flex items-start gap-3">
            <div class="rounded-lg bg-blue-50 p-2">
              <CalendarDays class="h-5 w-5 text-blue-600" />
            </div>

            <div class="min-w-0 flex-1">
              <p
                class="text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                Date &amp; Time
              </p>

              <p class="mt-1 text-sm font-medium text-gray-900">
                {{ eventDate }}
              </p>
            </div>
          </div>

          <div class="border-t border-gray-100"></div>

          <!-- Venue -->
          <div class="flex items-start gap-3">
            <div class="rounded-lg bg-blue-50 p-2">
              <MapPin class="h-5 w-5 text-blue-600" />
            </div>

            <div class="min-w-0 flex-1">
              <p
                class="text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                Venue
              </p>

              <p
                class="mt-1 break-words text-sm font-medium text-gray-900"
              >
                {{ eventLocation }}
              </p>
            </div>
          </div>

          <!-- Expected Attendees -->
          <template v-if="event.expected_attendees">
            <div class="border-t border-gray-100"></div>

            <div class="flex items-start gap-3">
              <div class="rounded-lg bg-blue-50 p-2">
                <Users class="h-5 w-5 text-blue-600" />
              </div>

              <div>
                <p
                  class="text-xs font-semibold uppercase tracking-wide text-gray-500"
                >
                  Expected Attendees
                </p>

                <p class="mt-1 text-sm font-medium text-gray-900">
                  {{ event.expected_attendees }}
                </p>
              </div>
            </div>
          </template>
        </section>

        <!-- Description -->
        <section>
          <h3
            class="mb-3 text-sm font-bold uppercase tracking-wide text-gray-900"
          >
          {{ t('eventDetails.aboutEvent') }}
          </h3>

          <!-- Use text interpolation instead of v-html for safety. -->
         <div
  class="text-sm text-gray-700 event-description mb-3"
  v-html="eventDescription"
></div>
        </section>

        <!-- Online Meeting -->
        <section
          v-if="event.online_meeting_link"
          class="rounded-xl border border-blue-100 bg-blue-50 p-4"
        >
          <p class="text-sm font-semibold text-gray-900">
            Online Meeting
          </p>

          <a
            :href="event.online_meeting_link"
            target="_blank"
            rel="noopener noreferrer"
            class="mt-2 inline-block break-all text-sm text-blue-700 underline"
          >
            Join meeting
          </a>
        </section>
      </main>

      <!-- Bottom Actions -->
      <footer
        class="sticky bottom-0 z-10 border-t border-gray-100 bg-white px-5 py-4"
      >
        <div class="mx-auto flex max-w-3xl gap-3">
          <button
  type="button"
  @click.stop="registerEvent(event)"
  :disabled="event.registered || registering"
  class="px-4 py-2 rounded-xl bg-primary-600 text-white
         font-semibold text-sm hover:bg-primary-700
         disabled:opacity-50 disabled:cursor-not-allowed
         transition-colors"
>
   {{
        event.registered
          ? t('announcements.registered')
          : registering
            ? t('announcements.registering')
            : t('announcements.register')
      }}
</button>

          <button
            type="button"
            @click="exploreMore"
            class="flex-1 rounded-xl bg-blue-50 px-4 py-3 text-sm font-semibold text-blue-900 transition hover:bg-blue-100"
          >
           {{ t('eventDetails.exploreMore') }}
          </button>
        </div>
      </footer>
    </template>
  </div>
</template>

<style scoped>
.event-description {
  overflow-wrap: anywhere;
}
</style>
