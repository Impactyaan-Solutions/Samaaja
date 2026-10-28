
<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  ArrowLeft,
  Share2,
  Loader2,
  CheckCircle2,
  ClipboardList,
  CalendarDays,
  Clock3,
  MapPin,
  Users,
  Wrench,
} from 'lucide-vue-next'

import {
  getVolunteerOpportunity,
  checkVolunteerApplication,
  get_project,
  claimProjectTask,
} from '@/services/api'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

const opportunity = ref(null)
const projectData = ref(null)
const application = ref(null)
const alreadyApplied = ref(false)

const loading = ref(true)
const error = ref('')
const shareError = ref('')
const taskError = ref('')
const claimingTask = ref(null)

const unwrapResponse = (response) => {
  let result = response

  for (let i = 0; i < 4; i++) {
    if (result?.data !== undefined) {
      result = result.data
    } else if (result?.message?.data !== undefined) {
      result = result.message.data
    } else if (result?.message !== undefined) {
      result = result.message
    } else {
      break
    }
  }

  return result
}

const isProject = computed(
  () => Number(opportunity.value?.is_project) === 1
)

const isSelected = computed(
  () =>
    String(application.value?.workflow_state || '')
      .trim()
      .toLowerCase() === 'selected'
)

const projectTasks = computed(() => {
  const tasks =
    projectData.value?.tasks ||
    projectData.value?.project_tasks ||
    opportunity.value?.project_tasks

  return Array.isArray(tasks) ? tasks : []
})

const teamAvailabilityConfigured = computed(
  () => Number(opportunity.value?.team_size || 0) > 0
)

const teamFillPercentage = computed(() => {
  const total = Number(opportunity.value?.team_size || 0)
  const selected = Number(opportunity.value?.selected_count || 0)

  if (total <= 0) return 0

  return Math.round(Math.min((selected / total) * 100, 100))
})

const remainingPositions = computed(() => {
  const total = Number(opportunity.value?.team_size || 0)
  const selected = Number(opportunity.value?.selected_count || 0)

  return Math.max(
    Number(
      opportunity.value?.remaining_positions ??
      Math.max(total - selected, 0)
    ),
    0
  )
})

const title = computed(
  () =>
    opportunity.value?.title ||
    opportunity.value?.opportunity_title ||
    opportunity.value?.name ||
    ''
)

const category = computed(
  () =>
    opportunity.value?.category ||
    opportunity.value?.category_name ||
    opportunity.value?.type ||
    ''
)

const location = computed(
  () => opportunity.value?.location || ''
)

const commitment = computed(
  () => opportunity.value?.expected_time_commitment || '—'
)

const skills = computed(() => {
  const value = opportunity.value?.skills_needed

  if (Array.isArray(value)) {
    return value
      .map((skill) =>
        typeof skill === 'string'
          ? skill
          : skill?.skill || skill?.skill_name || skill?.name || ''
      )
      .filter(Boolean)
      .join(', ')
  }

  if (typeof value === 'string') {
    return value.trim()
  }

  return ''
})

const formatDate = (value, includeYear = true) => {
  if (!value) return ''

  const date = new Date(`${value}`.slice(0, 10) + 'T12:00:00')

  if (Number.isNaN(date.getTime())) return value

  return new Intl.DateTimeFormat(
    locale.value === 'hi' ? 'hi-IN' : 'en',
    {
      month: 'short',
      day: 'numeric',
      ...(includeYear ? { year: 'numeric' } : {}),
    }
  ).format(date)
}

const timeline = computed(() => {
  const start = opportunity.value?.start_date
  const end = opportunity.value?.end_date

  if (start && end) {
    const startDate = new Date(`${start}`.slice(0, 10) + 'T12:00:00')
    const endDate = new Date(`${end}`.slice(0, 10) + 'T12:00:00')

    if (
      !Number.isNaN(startDate.getTime()) &&
      !Number.isNaN(endDate.getTime()) &&
      startDate.getFullYear() === endDate.getFullYear()
    ) {
      return `${formatDate(start, false)} – ${formatDate(end)}`
    }

    return `${formatDate(start)} – ${formatDate(end)}`
  }

  if (start) return `Starts ${formatDate(start)}`
  if (end) return `Ends ${formatDate(end)}`

  return '—'
})

const taskStatus = (task) =>
  task?.display_status || task?.status || 'Open'

const normalizedStatus = (task) =>
  String(taskStatus(task)).trim().toLowerCase()

const taskIsCompleted = (task) =>
  normalizedStatus(task) === 'completed'

const taskIsOpen = (task) =>
  normalizedStatus(task) === 'open' && !task?.assignee

const taskIsAssignedToCurrentUser = (task) =>
  Boolean(task?.is_assigned_to_current_user)

const taskCanBeClaimed = (task) =>
  isSelected.value &&
  taskIsOpen(task) &&
  !taskIsCompleted(task)

const taskCanBeCompleted = (task) =>
  isSelected.value &&
  taskIsAssignedToCurrentUser(task) &&
  !taskIsCompleted(task)

const fetchOpportunity = async () => {
  loading.value = true
  error.value = ''
  taskError.value = ''
  application.value = null
  projectData.value = null
  alreadyApplied.value = false

  try {
    const opportunityResponse = await getVolunteerOpportunity(
      route.params.id
    )

    const opportunityResult = unwrapResponse(opportunityResponse)

    opportunity.value =
      opportunityResult?.opportunity ||
      opportunityResult?.data?.opportunity ||
      opportunityResult

    if (
      !opportunity.value ||
      opportunityResponse?.status === 'error' ||
      opportunityResponse?.status_code >= 400
    ) {
      throw new Error('Could not load opportunity details.')
    }

    if (isProject.value) {
      const projectResponse = await get_project(route.params.id)
      const projectResult = unwrapResponse(projectResponse)

      if (
        projectResponse?.status === 'error' ||
        projectResponse?.status_code >= 400
      ) {
        throw new Error(
          projectResponse?.message || 'Could not load project details.'
        )
      }

      const project =
        projectResult?.project || projectResult?.data?.project

      const tasks =
        projectResult?.tasks || projectResult?.data?.tasks || []

      if (project) {
        opportunity.value = {
          ...opportunity.value,
          ...project,
        }
      }

      projectData.value = {
        ...(project || {}),
        tasks: Array.isArray(tasks) ? tasks : [],
      }

      application.value =
        projectResult?.application ||
        projectResult?.data?.application ||
        null

      alreadyApplied.value = Boolean(application.value)
    } else {
      const applicationResponse = await checkVolunteerApplication(
        route.params.id
      )

      const applicationResult = unwrapResponse(applicationResponse)

      if (
        applicationResponse?.status === 'error' ||
        applicationResponse?.status_code >= 400
      ) {
        throw new Error('Could not check application status.')
      }

      alreadyApplied.value = Boolean(
        applicationResult?.already_applied ??
        applicationResult?.data?.already_applied ??
        false
      )

      application.value =
        applicationResult?.application ||
        applicationResult?.data?.application ||
        null
    }
  } catch (err) {
    console.error('Failed to load opportunity:', err)
    error.value = err?.message || 'Failed to load opportunities.'
  } finally {
    loading.value = false
  }
}

const applyForOpportunity = () => {
  if (alreadyApplied.value) return

  router.push({
    name: 'volunteer-application',
    params: { id: route.params.id },
  })
}

const claimTask = async (task) => {
  if (!taskCanBeClaimed(task)) return
  if (!task?.name || claimingTask.value) return

  claimingTask.value = task.name
  taskError.value = ''

  try {
    await claimProjectTask({
      volunteer_opportunity: route.params.id,
      task_name: task.name,
    })

    await fetchOpportunity()
  } catch (err) {
    console.error('Failed to claim task:', err)

    taskError.value =
      err?.message ||
      'Could not claim this task. It may already be assigned.'

    await fetchOpportunity()
  } finally {
    claimingTask.value = null
  }
}

const markComplete = (task) => {
  if (!taskCanBeCompleted(task)) return

  router.push({
    name: 'log-action',
    query: {
      volunteer_opportunity: route.params.id,
      task_name: task.name,
    },
  })
}

const shareOpportunity = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    shareError.value = ''

    alert(
      isProject.value
        ? 'Project link copied!'
        : 'Opportunity link copied!'
    )
  } catch (err) {
    console.error('Failed to copy link:', err)
    shareError.value = 'Could not copy the link. Please try again.'
  }
}

const goBack = () => router.back()

onMounted(async () => {
  await nextTick()

  window.scrollTo({
    top: 0,
    left: 0,
    behavior: 'instant',
  })

  document.querySelector('main')?.scrollTo({
    top: 0,
    left: 0,
    behavior: 'instant',
  })

  await fetchOpportunity()
})
</script>

<template>
  <main class="min-h-full bg-gray-50 pb-32 text-gray-900">
    <!-- Header -->
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

      <h2 class="text-lg font-bold text-gray-900">
        {{ isProject ? 'Project' : 'Opportunity' }}
      </h2>

      <button
        type="button"
        class="-mr-2 rounded-full p-2 transition-colors hover:bg-gray-100"
        :aria-label="isProject ? 'Share project' : 'Share opportunity'"
        @click="shareOpportunity"
      >
        <Share2 class="h-5 w-5 text-gray-600" />
      </button>
    </header>

    <!-- Loading -->
    <div
      v-if="loading"
      class="flex flex-col items-center justify-center px-5 pt-16 text-center"
    >
      <Loader2 class="mb-3 h-7 w-7 animate-spin text-primary-500" />

      <p class="text-sm text-gray-500">
        Loading opportunity...
      </p>
    </div>

    <!-- Error -->
    <div
      v-else-if="error && !opportunity"
      class="px-5 pt-12 text-center"
    >
      <p class="text-sm text-red-500">{{ error }}</p>

      <button
        type="button"
        class="mt-3 text-sm font-semibold text-primary-600 underline"
        @click="fetchOpportunity"
      >
        Try again
      </button>
    </div>

    <template v-else-if="opportunity">
      <!-- Title and metadata -->
      <div class="px-5 pt-4">
        <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-[0_2px_10px_rgba(0,0,0,0.04)]">
          <h1 class="text-lg font-bold leading-snug text-gray-900">
            {{ title }}
          </h1>

          <div class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1.5">
            <span
              v-if="location"
              class="inline-flex items-center gap-1.5 text-xs text-gray-500"
            >
              <MapPin :size="14" class="shrink-0 text-gray-400" />
              {{ location }}
            </span>
            <span
              v-if="isProject"
              class="inline-flex items-center gap-1.5 rounded-md bg-[#E2F7E8] px-2 py-1 text-[10px] font-semibold text-[#159447]"
            >
              <Users class="h-3 w-3" />
              Team-based
            </span>
          </div>

          <div v-if="category" class="mt-3 flex flex-wrap gap-2">
            <span
              class="inline-flex items-center gap-1.5 rounded-md bg-blue-100 px-2 py-1 text-[10px] font-semibold text-blue-800"
            >
              {{ category }}
            </span>
          </div>

          <div
            v-if="shareError"
            class="mt-4 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600"
          >
            {{ shareError }}
          </div>
        </div>
      </div>

      <!-- Information cards -->
      <div class="px-5 pt-3">
        <div class="grid grid-cols-2 gap-3">
          <article
            class="flex min-w-0 flex-col rounded-xl border border-gray-100 bg-white p-3.5 shadow-[0_2px_10px_rgba(0,0,0,0.04)]"
          >
            <div
              class="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
            >
              <CalendarDays :size="15" />
            </div>

            <p class="text-[10px] font-semibold uppercase tracking-wide text-gray-500">
              Timeline
            </p>

            <p class="mt-1 break-words text-xs font-medium leading-5 text-gray-900">
              {{ timeline }}
            </p>
          </article>

          <article
            class="flex min-w-0 flex-col rounded-xl border border-gray-100 bg-white p-3.5 shadow-[0_2px_10px_rgba(0,0,0,0.04)]"
          >
            <div
              class="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
            >
              <Clock3 :size="15" />
            </div>

            <p class="text-[10px] font-semibold uppercase tracking-wide text-gray-500">
              Commitment
            </p>

            <p class="mt-1 break-words text-xs font-medium leading-5 text-gray-900">
              {{ commitment }}
            </p>
          </article>

          <article
            class="flex min-w-0 flex-col rounded-xl border border-gray-100 bg-white p-3.5 shadow-[0_2px_10px_rgba(0,0,0,0.04)]"
          >
            <div
              class="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
            >
              <MapPin :size="15" />
            </div>

            <p class="text-[10px] font-semibold uppercase tracking-wide text-gray-500">
              Location
            </p>

            <p class="mt-1 break-words text-xs font-medium leading-5 text-gray-900">
              {{ location || '—' }}
            </p>
          </article>

          <article
            class="flex min-w-0 flex-col rounded-xl border border-gray-100 bg-white p-3.5 shadow-[0_2px_10px_rgba(0,0,0,0.04)]"
          >
            <div
              class="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
            >
              <Wrench :size="15" />
            </div>

            <p class="text-[10px] font-semibold uppercase tracking-wide text-gray-500">
              Skills
            </p>

            <p class="mt-1 break-words text-xs font-medium leading-5 text-gray-900">
              {{ skills || '—' }}
            </p>
          </article>
        </div>
      </div>

      <!-- Team Availability: projects only -->
      <div
        v-if="isProject && teamAvailabilityConfigured"
        class="px-5 pt-3"
      >
        <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-[0_2px_10px_rgba(0,0,0,0.04)]">
          <div class="flex items-start justify-between gap-3">
            <div>
              <h2 class="text-sm font-bold text-gray-900">
                Team Availability
              </h2>

              <p class="mt-1 text-xs text-gray-500">
                {{ opportunity.selected_count || 0 }} of
                {{ opportunity.team_size }} positions filled
              </p>
            </div>

            <span
              class="shrink-0 rounded-full px-3 py-1 text-[10px] font-bold"
              :class="
                remainingPositions > 0
                  ? 'bg-blue-50 text-blue-700'
                  : 'bg-purple-50 text-purple-700'
              "
            >
              {{
                remainingPositions > 0
                  ? `${remainingPositions} ${
                      remainingPositions === 1 ? 'position' : 'positions'
                    } left`
                  : 'Team full'
              }}
            </span>
          </div>

          <div
            class="mt-4 h-2 overflow-hidden rounded-full bg-gray-100"
            role="progressbar"
            :aria-valuenow="teamFillPercentage"
            aria-valuemin="0"
            aria-valuemax="100"
            :aria-label="`Team filled: ${teamFillPercentage}%`"
          >
            <div
              class="h-full rounded-full bg-primary-600 transition-all duration-300"
              :style="{ width: `${teamFillPercentage}%` }"
            ></div>
          </div>

          <div
            class="mt-2 flex items-center justify-between text-[10px] text-gray-500"
          >
            <span>Team progress</span>

            <span class="font-bold text-gray-700">
              {{ teamFillPercentage }}%
            </span>
          </div>
        </div>
      </div>

      <!-- About -->
      <div class="px-5 pt-5">
        <h2 class="text-sm font-bold text-gray-900">
          {{ isProject ? 'About the Project' : 'About the Opportunity' }}
        </h2>

        <p class="mt-2 whitespace-pre-line text-sm leading-6 text-gray-500">
          {{ opportunity.description || 'No opportunity description available.' }}
        </p>
      </div>

      <!-- What happens after I apply: preserved from the old page -->
      <div class="px-5 pt-5">
        <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-[0_2px_10px_rgba(0,0,0,0.04)]">
          <h2 class="text-sm font-bold text-gray-900">
            {{ t('volunteerOpportunityDetail.whatHappensAfterApply') }}
          </h2>

          <p class="mt-2 text-sm leading-6 text-gray-500">
            {{ t('volunteerOpportunityDetail.afterApplyDescription') }}
          </p>
        </div>
      </div>

      <!-- Tasks and roles: projects only -->
      <div v-if="isProject" class="px-5 pt-5">
        <div class="mb-3 flex items-center justify-between gap-3">
          <h2 class="text-sm font-bold text-gray-900">
            Tasks &amp; Roles
          </h2>

          <span
            class="rounded-full bg-blue-50 px-3 py-1 text-[11px] font-bold text-blue-700"
          >
            {{ projectTasks.length }}
            {{ projectTasks.length === 1 ? 'task' : 'tasks' }}
          </span>
        </div>

        <p
          v-if="taskError"
          class="mb-3 rounded-lg border border-red-200 bg-red-50 p-3 text-xs text-red-700"
        >
          {{ taskError }}
        </p>

        <div v-if="projectTasks.length" class="space-y-2.5">
          <article
            v-for="task in projectTasks"
            :key="task.name || task.idx"
            class="rounded-xl border border-gray-100 bg-white p-3.5 shadow-[0_2px_10px_rgba(0,0,0,0.04)]"
          >
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0 flex-1">
                <h3 class="text-xs font-bold leading-5 text-gray-900">
                  {{ task.task || 'Untitled task' }}
                </h3>
              </div>

              <span
                class="shrink-0 rounded-full px-2 py-1 text-[10px] font-bold"
                :class="{
                  'bg-blue-50 text-blue-700':
                    taskStatus(task) === 'Open',
                  'bg-purple-50 text-purple-700':
                    taskStatus(task) === 'Assigned',
                  'bg-green-50 text-green-700':
                    taskStatus(task) === 'Completed',
                }"
              >
                {{ taskStatus(task) }}
              </span>
            </div>

            <p
              v-if="task.description"
              class="mt-1.5 whitespace-pre-line text-[11px] leading-[1.65] text-gray-500"
            >
              {{ task.description }}
            </p>

            <div
              class="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-gray-100 pt-2.5"
            >
              <p class="min-w-0 text-[10px] text-gray-500">
                <span class="font-semibold">
                  {{
                    task.assignee_name ||
                    task.assignee ||
                    'Unassigned'
                  }}
                </span>
              </p>

              <!-- Only selected applicants can perform task actions -->
              <template v-if="isSelected && !taskIsCompleted(task)">
                <button
                  v-if="taskCanBeCompleted(task)"
                  type="button"
                  class="inline-flex items-center gap-1.5 rounded-lg bg-gray-100 px-2.5 py-1.5 text-[10px] font-bold text-gray-700 transition hover:bg-gray-200"
                  @click="markComplete(task)"
                >
                  <CheckCircle2 :size="13" />
                  Mark Complete
                </button>

                <button
                  v-else-if="taskCanBeClaimed(task)"
                  type="button"
                  class="rounded-lg bg-primary-600 px-3 py-1.5 text-[10px] font-bold text-white transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50"
                  :disabled="claimingTask !== null"
                  @click="claimTask(task)"
                >
                  {{
                    claimingTask === task.name
                      ? 'Claiming...'
                      : 'Claim Task'
                  }}
                </button>
              </template>

              <span
                v-if="taskIsCompleted(task)"
                class="inline-flex items-center gap-1 rounded-full bg-green-50 px-2 py-1 text-[10px] font-bold text-green-700"
              >
                <CheckCircle2 :size="13" />
                Completed
              </span>
            </div>
          </article>
        </div>

        <div
          v-else
          class="rounded-xl border border-dashed border-gray-200 bg-white p-6 text-center"
        >
          <ClipboardList :size="25" class="mx-auto text-gray-400" />

          <h3 class="mt-2 text-xs font-bold text-gray-700">
            No tasks available yet
          </h3>

          <p class="mt-1 text-[11px] text-gray-500">
            No tasks have been added to this opportunity yet.
          </p>
        </div>
      </div>

      <!-- Bottom application button -->
      <div
        class="fixed inset-x-0 bottom-[88px] z-40 border-t border-gray-100 bg-white/95 px-4 py-3 backdrop-blur"
      >
        <button
          v-if="!alreadyApplied"
          type="button"
          @click="applyForOpportunity"
          class="mx-auto block w-full max-w-md rounded-xl bg-primary-600 px-6 py-3.5 text-base font-bold text-white shadow-md transition hover:bg-primary-700 active:scale-[0.99]"
        >
          {{ t('volunteerOpportunityDetail.applyNow') }}
        </button>

        <button
          v-else
          type="button"
          disabled
          class="mx-auto block w-full max-w-md cursor-not-allowed rounded-xl bg-gray-100 px-6 py-3.5 text-base font-bold text-gray-400"
        >
          Applied
        </button>
      </div>
    </template>
  </main>
</template>
