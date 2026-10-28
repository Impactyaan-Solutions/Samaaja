<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import {
  CheckCircle2,
  XCircle,
  ArrowLeft,
  Loader2,
  RefreshCw,
} from "lucide-vue-next"
import { useI18n } from "vue-i18n"
import { checkInEvent } from "@/services/api"

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const loading = ref(true)
const retrying = ref(false)
const resultMessage = ref("")
const checkedInOn = ref(null)
const registered = ref(false)
const checkedIn = ref(false)
const error = ref(false)

const eventId = computed(() => String(route.params.id || ""))

const statusTitle = computed(() => {
  if (loading.value) return t("eventCheckIn.markingAttendance")

  if (
    checkedIn.value &&
    resultMessage.value.toLowerCase().includes("already")
  ) {
    return t("eventCheckIn.alreadyCheckedIn")
  }

  if (checkedIn.value) return t("eventCheckIn.attendanceConfirmed")

  return t("eventCheckIn.checkInUnsuccessful")
})

const statusDescription = computed(() => {
  if (loading.value) {
    return t("eventCheckIn.pleaseWait")
  }

  return resultMessage.value || t("eventCheckIn.unableToMarkAttendance")
})

const formattedCheckInTime = computed(() => {
  if (!checkedInOn.value) return ""

  const date = new Date(checkedInOn.value)

  if (Number.isNaN(date.getTime())) {
    return checkedInOn.value
  }

  return date.toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  })
})

function extractResponse(response) {
  let data = response

  for (let i = 0; i < 6; i++) {
    if (!data || typeof data !== "object") break

    if (
      data.checked_in !== undefined ||
      data.registered !== undefined ||
      data.checked_in_on !== undefined
    ) {
      return data
    }

    if (data.data && typeof data.data === "object") {
      data = data.data
    } else if (data.message && typeof data.message === "object") {
      data = data.message
    } else {
      break
    }
  }

  return data || {}
}

function extractMessage(response, fallback) {
  let data = response

  for (let i = 0; i < 6; i++) {
    if (!data || typeof data !== "object") break

    if (typeof data.message === "string" && data.message) {
      return data.message
    }

    if (typeof data.data === "string" && data.data) {
      return data.data
    }

    if (data.data && typeof data.data === "object") {
      data = data.data
    } else if (data.message && typeof data.message === "object") {
      data = data.message
    } else {
      break
    }
  }

  return fallback
}

function extractErrorMessage(exception) {
  const responseData = exception?.response?.data

  if (typeof responseData?.message === "string") {
    return responseData.message
  }

  if (typeof responseData?._server_messages === "string") {
    try {
      const messages = JSON.parse(responseData._server_messages)
      const firstMessage = JSON.parse(messages[0])

      if (firstMessage?.message) {
        return firstMessage.message
      }
    } catch {
      // Use the translated fallback below.
    }
  }

  return t("eventCheckIn.unableToMarkAttendance")
}

async function markPresent() {
  loading.value = true
  error.value = false
  resultMessage.value = ""
  checkedIn.value = false
  registered.value = false
  checkedInOn.value = null

  try {
    if (!eventId.value) {
      throw new Error(t("eventCheckIn.eventIdMissing"))
    }

    const response = await checkInEvent(eventId.value)
    const data = extractResponse(response)

    checkedIn.value = data.checked_in === true
    registered.value = data.registered === true
    checkedInOn.value = data.checked_in_on || null

    resultMessage.value = extractMessage(
      response,
      checkedIn.value
        ? t("eventCheckIn.checkInSuccess")
        : t("eventCheckIn.serverNotConfirmed")
    )

    if (!checkedIn.value) {
      error.value = true
    }
  } catch (exception) {
    console.error("Failed to mark attendance:", exception)

    error.value = true
    resultMessage.value =
      exception?.message === t("eventCheckIn.eventIdMissing")
        ? t("eventCheckIn.eventIdMissing")
        : extractErrorMessage(exception)
  } finally {
    loading.value = false
    retrying.value = false
  }
}

async function retryCheckIn() {
  if (retrying.value || loading.value) return

  retrying.value = true
  await markPresent()
}

function goBack() {
  router.push({ name: "announcements" })
}

onMounted(() => {
  markPresent()
})
</script>

<template>
  <main class="min-h-screen bg-slate-50 px-4 py-8 text-gray-900">
    <header class="mx-auto mb-6 max-w-md">
      <button
        type="button"
        class="inline-flex items-center gap-2 text-sm font-medium text-gray-600 transition hover:text-blue-600"
        @click="goBack"
      >
        <ArrowLeft :size="18" />
        {{ t("eventCheckIn.backToEvents") }}
      </button>
    </header>

    <section
      class="mx-auto w-full max-w-md overflow-hidden rounded-2xl border border-gray-200 bg-white p-6 text-center shadow-sm sm:p-8"
    >
      <div
        v-if="loading"
        class="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-full bg-blue-50 text-blue-600"
      >
        <Loader2 :size="38" class="animate-spin" />
      </div>

      <div
        v-else
        class="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-full"
        :class="
          checkedIn
            ? 'bg-green-100 text-green-600'
            : 'bg-red-100 text-red-600'
        "
      >
        <CheckCircle2 v-if="checkedIn" :size="40" />
        <XCircle v-else :size="40" />
      </div>

      <p
        class="mb-2 text-xs font-bold uppercase tracking-[0.2em] text-gray-500"
      >
        {{ t("eventCheckIn.headerTitle") }}
      </p>

      <h1 class="text-2xl font-bold tracking-tight text-gray-900">
        {{ statusTitle }}
      </h1>

      <p
        class="mx-auto mt-3 max-w-sm break-words text-sm leading-6 text-gray-500"
      >
        {{ statusDescription }}
      </p>

      <div
        class="mt-7 rounded-xl border border-gray-200 bg-gray-50 p-4 text-left"
      >
        <p class="text-xs font-medium text-gray-500">
          {{ t("eventCheckIn.eventId") }}
        </p>

        <p class="mt-1 break-all text-lg font-bold text-gray-900">
          {{ eventId || t("eventCheckIn.notAvailable") }}
        </p>
      </div>

      <div
        v-if="!loading && checkedIn"
        class="mt-5 rounded-xl border border-gray-200 px-4 text-left"
      >
        <div class="flex items-center justify-between gap-3 py-3 text-sm">
          <span class="text-gray-500">
            {{ t("eventCheckIn.registration") }}
          </span>

          <span class="font-semibold text-gray-900">
            {{
              registered
                ? t("eventCheckIn.confirmed")
                : t("eventCheckIn.notConfirmed")
            }}
          </span>
        </div>

        <div
          class="flex items-center justify-between gap-3 border-t border-gray-100 py-3 text-sm"
        >
          <span class="text-gray-500">
            {{ t("eventCheckIn.attendance") }}
          </span>

          <span class="font-semibold text-green-600">
            {{ t("eventCheckIn.present") }}
          </span>
        </div>

        <div
          v-if="formattedCheckInTime"
          class="flex items-start justify-between gap-3 border-t border-gray-100 py-3 text-sm"
        >
          <span class="shrink-0 text-gray-500">
            {{ t("eventCheckIn.checkedInAt") }}
          </span>

          <span class="text-right font-medium text-gray-900">
            {{ formattedCheckInTime }}
          </span>
        </div>
      </div>

      <div
        v-if="!loading && error"
        class="mt-5 flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-left text-red-700"
      >
        <XCircle :size="20" class="mt-0.5 shrink-0" />

        <p class="break-words text-sm leading-6">
          {{ resultMessage }}
        </p>
      </div>

      <button
        v-if="!loading && error"
        type="button"
        :disabled="retrying"
        class="mt-5 inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        @click="retryCheckIn"
      >
        <Loader2 v-if="retrying" :size="18" class="animate-spin" />
        <RefreshCw v-else :size="18" />
        {{ retrying ? t("eventCheckIn.retrying") : t("eventCheckIn.retry") }}
      </button>

      <p class="mt-8 border-t border-gray-100 pt-5 text-xs text-gray-400">
        {{ t("eventCheckIn.footer") }}
      </p>
    </section>
  </main>
</template>
