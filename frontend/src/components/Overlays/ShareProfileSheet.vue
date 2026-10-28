<script setup>
import { ref, computed } from 'vue'
import { X, Link2, Check } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  shareUrl: { type: String, required: true }
})
const emit = defineEmits(['close'])
const { t } = useI18n()

const copied = ref(false)

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(props.shareUrl)
  } catch (e) {
    // Fallback for browsers/contexts without the async Clipboard API
    const input = document.createElement('textarea')
    input.value = props.shareUrl
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
  }
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

const canNativeShare = computed(() => typeof navigator !== 'undefined' && !!navigator.share)

const nativeShare = async () => {
  try {
    await navigator.share({ title: t('profile.shareText'), url: props.shareUrl })
  } catch (e) {
    // User cancelled or the share failed - leave the sheet open either way.
  }
}

const socialLinks = computed(() => {
  const text = t('profile.shareText')
  const url = props.shareUrl
  return [
    {
      name: 'WhatsApp',
      colorClass: 'bg-green-100 text-green-600',
      href: `https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`,
      path: 'M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.78.46 3.45 1.28 4.95L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0012.04 2zm0 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 012.41 5.82c0 4.54-3.7 8.23-8.24 8.23-1.48 0-2.93-.39-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.188 8.188 0 01-1.26-4.38c0-4.54 3.7-8.23 8.26-8.23zm-4.52 4.69c-.15 0-.4.06-.61.3-.21.24-.8.78-.8 1.9 0 1.12.82 2.2.93 2.35.12.15 1.6 2.52 3.95 3.47.55.23.98.37 1.32.47.55.17 1.06.15 1.46.09.44-.07 1.37-.56 1.57-1.1.19-.54.19-1.01.13-1.1-.06-.1-.21-.16-.44-.27-.24-.12-1.37-.68-1.59-.75-.21-.08-.37-.12-.52.12-.15.24-.6.75-.73.9-.14.15-.27.17-.51.06-.24-.12-1.02-.38-1.94-1.2-.72-.64-1.2-1.43-1.35-1.67-.14-.24-.01-.37.11-.49.11-.11.24-.28.37-.42.12-.14.16-.24.24-.4.08-.17.04-.31-.02-.43-.06-.12-.52-1.27-.72-1.73-.19-.46-.38-.4-.52-.4z'
    },
    {
      name: 'X',
      colorClass: 'bg-gray-100 text-gray-900',
      href: `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`,
      path: 'M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z'
    },
    {
      name: 'Facebook',
      colorClass: 'bg-blue-100 text-blue-600',
      href: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
      path: 'M9.198 21.5h4v-8.01h3.604l.396-3.98h-4V7.22c0-1.158.33-1.95 1.978-1.95h2.112V1.683C16.955 1.629 15.6 1.5 14.02 1.5c-3.5 0-5.898 2.137-5.898 6.062v3.945H4.5v3.98h3.622v8.013z'
    },
    {
      name: 'LinkedIn',
      colorClass: 'bg-sky-100 text-sky-700',
      href: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`,
      path: 'M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.447-2.136 2.941v5.665H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.067-.926-2.067-2.067 0-1.14.923-2.065 2.067-2.065 1.14 0 2.067.925 2.067 2.065 0 1.141-.926 2.067-2.067 2.067zM6.995 20.452H3.678V9h3.317v11.452z'
    }
  ]
})

const openSocial = (href) => {
  window.open(href, '_blank', 'noopener,noreferrer,width=600,height=600')
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
          <h3 class="text-xl font-bold text-gray-900">{{ t('profile.shareTitle') }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ t('profile.shareSubtitle') }}</p>
        </div>
        <button @click="emit('close')" class="p-2 bg-gray-100 rounded-full hover:bg-gray-200">
          <X class="w-5 h-5 text-gray-600" />
        </button>
      </div>

      <!-- Copy link -->
      <div class="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-2xl p-3 mb-5">
        <Link2 class="w-4 h-4 text-gray-400 flex-shrink-0" />
        <span class="flex-1 text-sm text-gray-600 truncate">{{ shareUrl }}</span>
        <button
          @click="copyLink"
          class="flex items-center gap-1 px-3 py-1.5 rounded-xl text-xs font-semibold transition-colors flex-shrink-0"
          :class="copied ? 'bg-green-100 text-green-700' : 'bg-blue-600 text-white hover:bg-blue-700'"
        >
          <Check v-if="copied" class="w-3.5 h-3.5" />
          {{ copied ? t('profile.copied') : t('profile.copyLink') }}
        </button>
      </div>

      <!-- Native share sheet (mobile browsers that support it) -->
      <button
        v-if="canNativeShare"
        @click="nativeShare"
        class="w-full mb-5 py-3 rounded-2xl bg-blue-50 text-blue-700 font-semibold text-sm hover:bg-blue-100 transition-colors"
      >
        {{ t('profile.shareVia') }}
      </button>

      <!-- Social buttons -->
      <div class="grid grid-cols-4 gap-3">
        <button
          v-for="social in socialLinks"
          :key="social.name"
          @click="openSocial(social.href)"
          class="flex flex-col items-center gap-1.5"
        >
          <span :class="['w-12 h-12 rounded-full flex items-center justify-center', social.colorClass]">
            <svg viewBox="0 0 24 24" class="w-5 h-5" fill="currentColor">
              <path :d="social.path" />
            </svg>
          </span>
          <span class="text-[11px] text-gray-500 font-medium">{{ social.name }}</span>
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
