<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
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
import { get_project, claimProjectTask } from '../services/api'

const route = useRoute()
const router = useRouter()

const project = ref(null)
const tasks = ref([])
const loading = ref(true)
const claimingTask = ref(null)
const error = ref('')
const shareError = ref('')

const loadProject = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await get_project(route.params.id)

    if (
      response?.status === 'error' ||
      response?.status_code >= 400
    ) {
      throw new Error(response.message || 'Could not load project.')
    }

    const data = response?.data || response?.message?.data || response

    project.value = data?.project || data?.data?.project || null
    tasks.value = data?.tasks || data?.data?.tasks || []
  } catch (err) {
    console.error('Failed to load project:', err)
    error.value = err.message || 'Could not load project details.'
  } finally {
    loading.value = false
  }
}

const claimTask = async (task) => {
  if (!task?.name || claimingTask.value) return

  claimingTask.value = task.name
  error.value = ''

  try {
    await claimProjectTask({
      volunteer_opportunity: route.params.id,
      task_name: task.name,
    })

    await loadProject()
  } catch (err) {
    console.error('Failed to claim task:', err)

    error.value =
      err.message || 'Could not claim this task. It may already be assigned.'

    await loadProject()
  } finally {
    claimingTask.value = null
  }
}

const markComplete = (task) => {
  router.push({
    name: 'log-action',
    query: {
      volunteer_opportunity: route.params.id,
      task_name: task.name,
    },
  })
}

// Share project link
const shareProject = async () => {
  const url = window.location.href

  try {
    await navigator.clipboard.writeText(url)
    shareError.value = ''
    alert('Project link copied!')
  } catch (err) {
    console.error('Failed to copy project link:', err)
    shareError.value = 'Could not copy the project link. Please try again.'
  }
}

const formatDate = (value, includeYear = true) => {
  if (!value) return ''

  const date = new Date(`${value}`.slice(0, 10) + 'T12:00:00')

  if (Number.isNaN(date.getTime())) return value

  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    ...(includeYear ? { year: 'numeric' } : {}),
  }).format(date)
}

const timeline = () => {
  const start = project.value?.start_date
  const end = project.value?.end_date

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
}

const commitment = () => {
  return project.value?.expected_time_commitment || '—'
}

const category = () => {
  return project.value?.category || project.value?.category_name || ''
}

const location = () => {
  return project.value?.location || ''
}

const skills = () => {
  const value = project.value?.skills_needed

  if (Array.isArray(value)) {
    return value
      .map((skill) =>
        typeof skill === 'string'
          ? skill
          : skill?.skill || skill?.skill_name || skill?.name || '',
      )
      .filter(Boolean)
      .join(', ')
  }

  if (typeof value === 'string') {
    return value.trim()
  }

  return ''
}

const taskStatus = (task) => {
  return task.display_status || task.status || 'Open'
}

// Team availability
const teamAvailabilityConfigured = () => {
  return Number(project.value?.team_size || 0) > 0
}

const teamFillPercentage = () => {
  const total = Number(project.value?.team_size || 0)
  const selected = Number(project.value?.selected_count || 0)

  if (total <= 0) return 0

  return Math.round(Math.min((selected / total) * 100, 100))
}

const remainingPositions = () => {
  const total = Number(project.value?.team_size || 0)
  const selected = Number(project.value?.selected_count || 0)

  return Math.max(
    Number(
      project.value?.remaining_positions ??
      Math.max(total - selected, 0),
    ),
    0,
  )
}

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

  await loadProject()

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
})
</script>

<template>
  <main class="min-h-screen bg-[#F3F8F3] pb-8 text-[#172B1D]">
    <!-- Header -->
    <header
      class="sticky top-0 z-20 flex items-center border-b border-[#E1EEE3] bg-white px-5 py-4"
    >
      <button
        type="button"
        @click="router.back()"
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

      <!-- Share button -->
      <button
        type="button"
        class="rounded-xl bg-[#EDF5EF] p-2.5 transition hover:bg-[#E0EEE3]"
        aria-label="Share project"
        @click="shareProject"
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
      v-else-if="error && !project"
      class="mx-auto mt-6 max-w-5xl px-4"
    >
      <div
        class="rounded-xl border border-red-200 bg-white p-5 text-sm text-red-700"
      >
        <p>{{ error }}</p>

        <button
          type="button"
          class="mt-3 font-semibold underline"
          @click="loadProject"
        >
          Try again
        </button>
      </div>
    </div>

    <template v-else-if="project">
      <div class="mx-auto max-w-5xl">
        <!-- Title and metadata -->
        <section
          class="border-b border-[#E0EAE0] bg-white px-4 py-5 sm:px-6"
        >
          <h1
            class="text-[23px] font-extrabold leading-tight tracking-[-0.5px] text-[#172B1D] sm:text-3xl"
          >
            {{ project.title || project.opportunity_title || project.name }}
          </h1>

          <div
            class="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-[#526D58]"
          >
            <span
              v-if="location()"
              class="inline-flex items-center gap-1.5"
            >
              <MapPin :size="14" class="shrink-0 text-[#198B45]" />
              {{ location() }}
            </span>

            <span class="inline-flex items-center gap-1.5">
              <Users :size="14" class="shrink-0 text-[#198B45]" />
              Team-based
            </span>
          </div>

          <div v-if="category()" class="mt-3 flex flex-wrap gap-2">
            <span
              class="inline-flex items-center gap-1 rounded-full bg-[#E4F4E8] px-3 py-1.5 text-[11px] font-semibold text-[#198B45]"
            >
              <Leaf :size="13" />
              {{ category() }}
            </span>
          </div>

          <!-- Share error -->
          <div
            v-if="shareError"
            class="mt-4 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600"
          >
            {{ shareError }}
          </div>
        </section>

        <!-- Four information cards -->
        <section class="px-4 py-4 sm:px-6">
          <div class="grid grid-cols-2 gap-2.5">
            <!-- Timeline -->
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

              <p class="mt-1 break-words text-xs font-bold leading-5 text-[#203A27]">
                {{ timeline() }}
              </p>
            </article>

            <!-- Commitment -->
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

              <p class="mt-1 break-words text-xs font-bold leading-5 text-[#203A27]">
                {{ commitment() }}
              </p>
            </article>

            <!-- Location -->
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

              <p class="mt-1 break-words text-xs font-bold leading-5 text-[#203A27]">
                {{ location() || '—' }}
              </p>
            </article>

            <!-- Skills -->
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

              <p class="mt-1 break-words text-xs font-bold leading-5 text-[#203A27]">
                {{ skills() || '—' }}
              </p>
            </article>
          </div>
        </section>

        <!-- Team Availability -->
        <section
          v-if="teamAvailabilityConfigured()"
          class="px-4 pb-4 sm:px-6"
        >
          <div class="rounded-xl border border-[#D4E8D5] bg-white p-4">
            <div class="flex items-start justify-between gap-3">
              <div>
                <h2 class="text-sm font-extrabold text-[#203A27]">
                  Team Availability
                </h2>

                <p class="mt-1 text-xs text-[#617765]">
                  {{ project.selected_count || 0 }} of
                  {{ project.team_size }} positions filled
                </p>
              </div>

              <span
                class="shrink-0 rounded-full px-3 py-1 text-[10px] font-bold"
                :class="
                  remainingPositions() > 0
                    ? 'bg-[#E1F4E5] text-[#238044]'
                    : 'bg-[#EEE7FF] text-[#6941C6]'
                "
              >
                {{
                  remainingPositions() > 0
                    ? `${remainingPositions()} ${
                        remainingPositions() === 1
                          ? 'position'
                          : 'positions'
                      } left`
                    : 'Team full'
                }}
              </span>
            </div>

            <!-- Progress bar -->
            <div
              class="mt-4 h-2 overflow-hidden rounded-full bg-[#EAF2EA]"
              role="progressbar"
              :aria-valuenow="teamFillPercentage()"
              aria-valuemin="0"
              aria-valuemax="100"
              :aria-label="`Team filled: ${teamFillPercentage()}%`"
            >
              <div
                class="h-full rounded-full bg-[#198B45] transition-all duration-300"
                :style="{ width: `${teamFillPercentage()}%` }"
              ></div>
            </div>

            <div
              class="mt-2 flex items-center justify-between text-[10px] text-[#617765]"
            >
              <span>Team progress</span>
              <span class="font-bold text-[#203A27]">
                {{ teamFillPercentage() }}%
              </span>
            </div>
          </div>
        </section>

        <!-- About the project -->
        <section
          class="border-y-[6px] border-[#EAF2EA] bg-[#F6FAF6] px-4 py-5 sm:px-6"
        >
          <h2 class="text-sm font-extrabold text-[#172B1D]">
            About the Project
          </h2>

          <p
            class="mt-3 whitespace-pre-line text-xs leading-[1.75] text-[#617765] sm:text-sm"
          >
            {{ project.description || 'No opportunity description available.' }}
          </p>
        </section>

        <!-- Tasks and roles -->
        <section class="px-4 py-5 sm:px-6">
          <div class="mb-4 flex items-center justify-between gap-3">
            <h2 class="text-sm font-extrabold text-[#172B1D]">
              Tasks &amp; Roles
            </h2>

            <span
              class="rounded-full bg-[#E0F1E2] px-3 py-1 text-[11px] font-bold text-[#315D3B]"
            >
              {{ tasks.length }} {{ tasks.length === 1 ? 'task' : 'tasks' }}
            </span>
          </div>

          <p
            v-if="error"
            class="mb-3 rounded-lg border border-red-200 bg-red-50 p-3 text-xs text-red-700"
          >
            {{ error }}
          </p>

          <div v-if="tasks.length" class="space-y-2.5">
            <article
              v-for="task in tasks"
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
                    {{ task.assignee_name || task.assignee || 'Unassigned' }}
                  </span>
                </p>

                <template v-if="taskStatus(task) !== 'Completed'">
                  <button
                    v-if="task.is_assigned_to_current_user"
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg bg-[#EDF4EE] px-2.5 py-1.5 text-[10px] font-bold text-[#203A27] transition hover:bg-[#DFEBE0] disabled:cursor-not-allowed disabled:opacity-50"
                    @click="markComplete(task)"
                  >
                    <CheckCircle2 :size="13" />
                    Mark Complete
                  </button>

                  <button
                    v-else-if="
                      !task.assignee &&
                      (task.status === 'Open' || !task.status)
                    "
                    type="button"
                    class="rounded-lg bg-[#198B45] px-3 py-1.5 text-[10px] font-bold text-white transition hover:bg-[#14783A] disabled:cursor-not-allowed disabled:opacity-50"
                    :disabled="claimingTask !== null"
                    @click="claimTask(task)"
                  >
                    {{ claimingTask === task.name ? 'Claiming...' : 'Claim Task' }}
                  </button>
                </template>

                <span
                  v-else
                  class="inline-flex items-center gap-1 rounded-full bg-[#E5EEFF] px-2 py-1 text-[10px] font-bold text-[#315A9B]"
                >
                  <CheckCircle2 :size="13" />
                  Completed
                </span>
              </div>
            </article>
          </div>

          <!-- Empty tasks state -->
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
    </template>
  </main>
</template>