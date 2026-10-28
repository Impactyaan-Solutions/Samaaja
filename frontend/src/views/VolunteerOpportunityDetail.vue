
<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  ArrowLeft,
  Share2,
  LoaderCircle,
  CheckCircle2,
  ClipboardList,
  CalendarDays,
  Clock3,
  MapPin,
  Leaf,
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
  <main class="min-h-screen bg-[#F3F8F3] pb-32 text-[#172B1D]">
    <!-- Header -->
    <header
      class="sticky top-0 z-20 flex items-center border-b border-[#E1EEE3] bg-white px-5 py-4"
    >
      <button
        type="button"
        @click="goBack"
        class="-ml-1 rounded-xl bg-[#EDF5EF] p-2.5 transition hover:bg-[#E0EEE3]"
        aria-label="Go back"
      >
        <ArrowLeft class="h-5 w-5 text-[#243D2B]" />
      </button>

      <div class="mx-auto flex items-center gap-2">
        <span
          class="flex h-8 w-8 items-center justify-center rounded-full bg-[#198B45]"
        >
          <Leaf class="h-4 w-4 text-white" />
        </span>

        <span class="text-xl font-extrabold tracking-tight text-[#198B45]">
          samaaja
        </span>
      </div>

      <button
        type="button"
        class="rounded-xl bg-[#EDF5EF] p-2.5 transition hover:bg-[#E0EEE3]"
        :aria-label="isProject ? 'Share project' : 'Share opportunity'"
        @click="shareOpportunity"
      >
        <Share2 class="h-5 w-5 text-[#52705A]" />
      </button>
    </header>

    <!-- Loading -->
    <div
      v-if="loading"
      class="flex items-center justify-center gap-3 py-24 text-sm text-[#617363]"
    >
      <LoaderCircle class="animate-spin" :size="22" />
      Loading opportunity...
    </div>

    <!-- Error -->
    <div
      v-else-if="error && !opportunity"
      class="mx-auto mt-6 max-w-5xl px-4"
    >
      <div
        class="rounded-xl border border-red-200 bg-white p-5 text-sm text-red-700"
      >
        <p>{{ error }}</p>

        <button
          type="button"
          class="mt-3 font-semibold underline"
          @click="fetchOpportunity"
        >
          Try again
        </button>
      </div>
    </div>

    <template v-else-if="opportunity">
      <div class="mx-auto max-w-5xl">
        <!-- Title and metadata -->
        <section
          class="border-b border-[#E0EAE0] bg-white px-4 py-5 sm:px-6"
        >
          <h1
            class="text-[23px] font-extrabold leading-tight tracking-[-0.5px] text-[#172B1D] sm:text-3xl"
          >
            {{ title }}
          </h1>

          <div
            class="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-[#526D58]"
          >
            <span v-if="location" class="inline-flex items-center gap-1.5">
              <MapPin :size="14" class="shrink-0 text-[#198B45]" />
              {{ location }}
            </span>

            <span v-if="isProject" class="inline-flex items-center gap-1.5">
              <Users :size="14" class="shrink-0 text-[#198B45]" />
              Team-based
            </span>
          </div>

          <div v-if="category" class="mt-3 flex flex-wrap gap-2">
            <span
              class="inline-flex items-center gap-1 rounded-full bg-[#E4F4E8] px-3 py-1.5 text-[11px] font-semibold text-[#198B45]"
            >
              <Leaf :size="13" />
              {{ category }}
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
        <section class="px-4 py-4 sm:px-6">
          <div class="grid grid-cols-2 gap-2.5">
            <article
              class="min-w-0 rounded-xl border border-[#D4E8D5] bg-white p-3"
            >
              <div
                class="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-[#E4F4E8] text-[#23804A]"
              >
                <CalendarDays :size="15" />
              </div>

              <p
                class="text-[10px] font-semibold uppercase tracking-[0.7px] text-[#617765]"
              >
                Timeline
              </p>

              <p
                class="mt-1 break-words text-xs font-bold leading-5 text-[#203A27]"
              >
                {{ timeline }}
              </p>
            </article>

            <article
              class="min-w-0 rounded-xl border border-[#D4E8D5] bg-white p-3"
            >
              <div
                class="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-[#E4F4E8] text-[#23804A]"
              >
                <Clock3 :size="15" />
              </div>

              <p
                class="text-[10px] font-semibold uppercase tracking-[0.7px] text-[#617765]"
              >
                Commitment
              </p>

              <p
                class="mt-1 break-words text-xs font-bold leading-5 text-[#203A27]"
              >
                {{ commitment }}
              </p>
            </article>

            <article
              class="min-w-0 rounded-xl border border-[#D4E8D5] bg-white p-3"
            >
              <div
                class="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-[#E4F4E8] text-[#23804A]"
              >
                <MapPin :size="15" />
              </div>

              <p
                class="text-[10px] font-semibold uppercase tracking-[0.7px] text-[#617765]"
              >
                Location
              </p>

              <p
                class="mt-1 break-words text-xs font-bold leading-5 text-[#203A27]"
              >
                {{ location || '—' }}
              </p>
            </article>

            <article
              class="min-w-0 rounded-xl border border-[#D4E8D5] bg-white p-3"
            >
              <div
                class="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-[#E4F4E8] text-[#23804A]"
              >
                <Wrench :size="15" />
              </div>

              <p
                class="text-[10px] font-semibold uppercase tracking-[0.7px] text-[#617765]"
              >
                Skills
              </p>

              <p
                class="mt-1 break-words text-xs font-bold leading-5 text-[#203A27]"
              >
                {{ skills || '—' }}
              </p>
            </article>
          </div>
        </section>

        <!-- Team Availability: projects only -->
        <section
          v-if="isProject && teamAvailabilityConfigured"
          class="px-4 pb-4 sm:px-6"
        >
          <div class="rounded-xl border border-[#D4E8D5] bg-white p-4">
            <div class="flex items-start justify-between gap-3">
              <div>
                <h2 class="text-sm font-extrabold text-[#203A27]">
                  Team Availability
                </h2>

                <p class="mt-1 text-xs text-[#617765]">
                  {{ opportunity.selected_count || 0 }} of
                  {{ opportunity.team_size }} positions filled
                </p>
              </div>

              <span
                class="shrink-0 rounded-full px-3 py-1 text-[10px] font-bold"
                :class="
                  remainingPositions > 0
                    ? 'bg-[#E1F4E5] text-[#238044]'
                    : 'bg-[#EEE7FF] text-[#6941C6]'
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
              class="mt-4 h-2 overflow-hidden rounded-full bg-[#EAF2EA]"
              role="progressbar"
              :aria-valuenow="teamFillPercentage"
              aria-valuemin="0"
              aria-valuemax="100"
              :aria-label="`Team filled: ${teamFillPercentage}%`"
            >
              <div
                class="h-full rounded-full bg-[#198B45] transition-all duration-300"
                :style="{ width: `${teamFillPercentage}%` }"
              ></div>
            </div>

            <div
              class="mt-2 flex items-center justify-between text-[10px] text-[#617765]"
            >
              <span>Team progress</span>

              <span class="font-bold text-[#203A27]">
                {{ teamFillPercentage }}%
              </span>
            </div>
          </div>
        </section>

        <!-- About -->
        <section
          class="border-y-[6px] border-[#EAF2EA] bg-[#F6FAF6] px-4 py-5 sm:px-6"
        >
          <h2 class="text-sm font-extrabold text-[#172B1D]">
            {{ isProject ? 'About the Project' : 'About the Opportunity' }}
          </h2>

          <p
            class="mt-3 whitespace-pre-line text-xs leading-[1.75] text-[#617765] sm:text-sm"
          >
            {{ opportunity.description || 'No opportunity description available.' }}
          </p>
        </section>

        <!-- What happens after I apply: preserved from the old page -->
        <section
          class="mx-4 mb-6 rounded-2xl border border-[#D4E8D5] bg-white p-5 sm:mx-6"
        >
          <h2 class="text-base font-bold text-[#172B1D]">
            {{ t('volunteerOpportunityDetail.whatHappensAfterApply') }}
          </h2>

          <p class="mt-3 text-sm leading-6 text-[#617765]">
            {{ t('volunteerOpportunityDetail.afterApplyDescription') }}
          </p>
        </section>

        <!-- Tasks and roles: projects only -->
        <section v-if="isProject" class="px-4 py-5 sm:px-6">
          <div class="mb-4 flex items-center justify-between gap-3">
            <h2 class="text-sm font-extrabold text-[#172B1D]">
              Tasks &amp; Roles
            </h2>

            <span
              class="rounded-full bg-[#E0F1E2] px-3 py-1 text-[11px] font-bold text-[#315D3B]"
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
              class="rounded-xl border border-[#D4E8D5] bg-white p-3"
            >
              <div class="flex items-start justify-between gap-3">
                <div class="min-w-0 flex-1">
                  <h3 class="text-xs font-bold leading-5 text-[#203A27]">
                    {{ task.task || 'Untitled task' }}
                  </h3>
                </div>

                <span
                  class="shrink-0 rounded-full px-2 py-1 text-[10px] font-bold"
                  :class="{
                    'bg-[#E1F4E5] text-[#238044]':
                      taskStatus(task) === 'Open',
                    'bg-[#EEE7FF] text-[#6941C6]':
                      taskStatus(task) === 'Assigned',
                    'bg-[#E5EEFF] text-[#315A9B]':
                      taskStatus(task) === 'Completed',
                  }"
                >
                  {{ taskStatus(task) }}
                </span>
              </div>

              <p
                v-if="task.description"
                class="mt-1.5 whitespace-pre-line text-[11px] leading-[1.65] text-[#617765]"
              >
                {{ task.description }}
              </p>

              <div
                class="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-[#E2EDE2] pt-2.5"
              >
                <p class="min-w-0 text-[10px] text-[#617765]">
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
                    class="inline-flex items-center gap-1.5 rounded-lg bg-[#EDF4EE] px-2.5 py-1.5 text-[10px] font-bold text-[#203A27] transition hover:bg-[#DFEBE0]"
                    @click="markComplete(task)"
                  >
                    <CheckCircle2 :size="13" />
                    Mark Complete
                  </button>

                  <button
                    v-else-if="taskCanBeClaimed(task)"
                    type="button"
                    class="rounded-lg bg-[#198B45] px-3 py-1.5 text-[10px] font-bold text-white transition hover:bg-[#14783A] disabled:cursor-not-allowed disabled:opacity-50"
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
                  class="inline-flex items-center gap-1 rounded-full bg-[#E5EEFF] px-2 py-1 text-[10px] font-bold text-[#315A9B]"
                >
                  <CheckCircle2 :size="13" />
                  Completed
                </span>
              </div>
            </article>
          </div>

          <div
            v-else
            class="rounded-xl border border-dashed border-[#D4E1D3] bg-white p-6 text-center"
          >
            <ClipboardList :size="25" class="mx-auto text-[#789477]" />

            <h3 class="mt-2 text-xs font-bold text-[#203A27]">
              No tasks available yet
            </h3>

            <p class="mt-1 text-[11px] text-[#617765]">
              No tasks have been added to this opportunity yet.
            </p>
          </div>
        </section>
      </div>

      <!-- Bottom application button -->
      <div
        class="fixed inset-x-0 bottom-[88px] z-40 border-t border-[#dceade] bg-white/95 px-4 py-3 backdrop-blur"
      >
        <button
          v-if="!alreadyApplied"
          type="button"
          @click="applyForOpportunity"
          class="mx-auto block w-full max-w-md rounded-xl bg-[#198b45] px-6 py-3.5 text-base font-bold text-white shadow-md transition hover:bg-[#14783a] active:scale-[0.99]"
        >
          {{ t('volunteerOpportunityDetail.applyNow') }}
        </button>

        <button
          v-else
          type="button"
          disabled
          class="mx-auto block w-full max-w-md cursor-not-allowed rounded-xl bg-[#e4f4e8] px-6 py-3.5 text-base font-bold text-[#198b45]"
        >
          Applied
        </button>
      </div>
    </template>
  </main>
</template>
