<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Zap, X, MessageSquareText } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const emit = defineEmits(['close'])
const router = useRouter()

// Computed allows the list to update automatically when language changes
const actions = computed(() => [
  {
    title: t('action_sheet.log_action.title'),
    description: t('action_sheet.log_action.desc'),
    icon: Zap,
    colorClass: 'bg-green-100 text-green-600',
    path: '/log-action'
  },
  {
    title: t('action_sheet.add_post.title'),
    description: t('action_sheet.add_post.desc'),
    icon: MessageSquareText,
    colorClass: 'bg-blue-100 text-blue-600',
    path: '/add-post'
  }
])

const handleAction = (path) => {
  emit('close')
  router.push(path)
}
</script>

<template>
  <div class="absolute inset-0 z-50 flex items-end">
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="emit('close')"></div>
    
    <div class="relative w-full max-w-md mx-auto bg-white rounded-t-3xl p-6 pb-12 shadow-2xl transition-transform animate-slideUp">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h3 class="text-xl font-bold text-gray-900">{{ t('action_sheet.title') }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ t('action_sheet.subtitle') }}</p>
        </div>
        <button @click="emit('close')" class="p-2 bg-gray-100 rounded-full hover:bg-gray-200">
          <X class="w-5 h-5 text-gray-600" />
        </button>
      </div>

      <div class="space-y-3 mt-4">
        <button 
          v-for="action in actions" 
          :key="action.title"
          @click="handleAction(action.path)"
          class="w-full flex items-center p-4 bg-white border border-gray-100 rounded-2xl shadow-sm hover:shadow-md transition-shadow text-left"
        >
          <div :class="['w-12 h-12 flex-shrink-0 rounded-full flex items-center justify-center mr-4', action.colorClass]">
            <component :is="action.icon" class="w-6 h-6" />
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