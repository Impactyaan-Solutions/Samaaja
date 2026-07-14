<script setup>
import { X, Check } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { SUPPORTED_LOCALES, setLocale } from '@/i18n'

const { t, locale } = useI18n()

const emit = defineEmits(['close'])

const choose = (code) => {
  setLocale(code)
  emit('close')
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
          <h3 class="text-xl font-bold text-gray-900">{{ t('languagePicker.title') }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ t('languagePicker.subtitle') }}</p>
        </div>
        <button @click="emit('close')" class="p-2 bg-gray-100 rounded-full hover:bg-gray-200">
          <X class="w-5 h-5 text-gray-600" />
        </button>
      </div>

      <div class="space-y-3 mt-4">
        <button
          v-for="code in SUPPORTED_LOCALES"
          :key="code"
          @click="choose(code)"
          class="w-full flex items-center justify-between p-4 bg-white border border-gray-100 rounded-2xl shadow-sm hover:shadow-md transition-shadow text-left"
        >
          <span class="font-semibold text-gray-900">{{ t(`languages.${code}`) }}</span>
          <Check v-if="locale === code" class="w-5 h-5 text-primary-600" />
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
