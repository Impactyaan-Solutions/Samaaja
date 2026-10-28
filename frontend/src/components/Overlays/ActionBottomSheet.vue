<script setup>
import { computed, ref } from 'vue'
import { Zap, X, MessageSquareText, ClipboardCheck, Loader2 } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { getMyActiveProjects } from '@/services/api'

const emit = defineEmits(['close'])
const router = useRouter()
const { t } = useI18n()

const loadingProjects = ref(false)

const actions = computed(() => [
  {
    key: 'log-action',
    title: t('actionSheet.logAction'),
    description: t('actionSheet.logActionDesc'),
    icon: Zap,
    colorClass: 'bg-green-100 text-green-600',
    path: '/log-action'
  },
  {
    key: 'add-post',
    title: t('actionSheet.addPost'),
    description: t('actionSheet.addPostDesc'),
    icon: MessageSquareText,
    colorClass: 'bg-blue-100 text-blue-600',
    path: '/add-post'
  },
  {
    key: 'complete-project',
    title: t('actionSheet.completeProject'),
    description: t('actionSheet.completeProjectDesc'),
    icon: ClipboardCheck,
    colorClass: 'bg-purple-100 text-purple-600'
  }
])

const goToActiveProjects = async () => {
  if (loadingProjects.value) return

  loadingProjects.value = true

  try {
    const result = await getMyActiveProjects()
    const projects = result?.projects || []

    emit('close')

    if (projects.length === 1) {
      router.push({
        name: 'volunteer-opportunity-detail',
        params: { id: projects[0].name }
      })
    } else if (projects.length === 0) {
      alert(t('actionSheet.noActiveProjects'))
    } else {
      router.push({ name: 'my-projects' })
    }
  } catch (err) {
    console.error('Failed to load active projects:', err)
    emit('close')
    alert(t('actionSheet.loadProjectsError'))
  } finally {
    loadingProjects.value = false
  }
}

const handleAction = (action) => {
  if (action.key === 'complete-project') {
    goToActiveProjects()
    return
  }

  emit('close')
  router.push(action.path)
}
</script>

<template>
  <div class="absolute inset-0 z-50 flex items-end">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="emit('close')"></div>
    
    <!-- Sheet -->
    <div class="relative w-full max-w-md mx-auto bg-white rounded-t-3xl p-6 pb-12 shadow-2xl transition-transform animate-slideUp">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h3 class="text-xl font-bold text-gray-900">{{ t('actionSheet.title') }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ t('actionSheet.subtitle') }}</p>
        </div>
        <button @click="emit('close')" class="p-2 bg-gray-100 rounded-full hover:bg-gray-200">
          <X class="w-5 h-5 text-gray-600" />
        </button>
      </div>

      <div class="space-y-3 mt-4">
        <button
          v-for="action in actions"
          :key="action.key"
          @click="handleAction(action)"
          :disabled="action.key === 'complete-project' && loadingProjects"
          class="w-full flex items-center p-4 bg-white border border-gray-100 rounded-2xl shadow-sm hover:shadow-md transition-shadow text-left disabled:cursor-not-allowed disabled:opacity-60"
        >
          <div :class="['w-12 h-12 flex-shrink-0 rounded-full flex items-center justify-center mr-4', action.colorClass]">
            <Loader2
              v-if="action.key === 'complete-project' && loadingProjects"
              class="w-6 h-6 animate-spin"
            />
            <component v-else :is="action.icon" class="w-6 h-6" />
          </div>
          <div>
            <h4 class="font-semibold text-gray-900">{{ action.title }}</h4>
            <p class="text-xs text-gray-500 mt-1">{{ action.description }}</p>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}
.animate-slideUp {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>
