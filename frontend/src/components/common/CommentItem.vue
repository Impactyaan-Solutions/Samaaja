<script setup>
import { getTimeSinceCreation } from '@/utils/utils'
import { authState } from '@/auth'
import { Pencil, Trash2 } from 'lucide-vue-next'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete'])
const authCache = JSON.parse(localStorage.getItem("samaaja_auth_cache"));

let userEmail = authCache?.email;

const isOwner = computed(() => {
  return props.comment.user_id === authState.email
})
// console.log('isOwner:', isOwner, 'userEmail:', userEmail.value, 'comment.user_id:', props.comment.user_id);
</script>

<template>
  <div class="flex items-start space-x-3 text-sm">

    <!-- Avatar: profile pic or initial fallback -->
    <div class="w-8 h-8 rounded-full shrink-0 overflow-hidden bg-gray-100 text-gray-700 flex items-center justify-center font-bold text-xs">
      <img
        v-if="comment.user_image"
        :src="comment.user_image"
        :alt="comment.full_name"
        class="w-full h-full object-cover"
        @error="$event.target.style.display = 'none'"
      />
      <span v-else>
        {{ comment.full_name?.charAt(0)?.toUpperCase() || '?' }}
      </span>
    </div>

    <div class="flex-1 bg-gray-50 rounded-2xl px-3 py-2">
      <div class="flex items-start justify-between mb-0.5">
        <div>
          <span class="font-semibold text-gray-900 text-xs">
            {{ comment.full_name }}
          </span>
          <div class="text-[10px] text-gray-400 font-medium">
            {{ getTimeSinceCreation(comment.creation) }}
          </div>
        </div>

        <!-- Edit / Delete icons — only for owner 
        <div v-if="isOwner" class="flex items-center gap-1.5">
          <button
            class="p-1 rounded-full text-gray-400 hover:text-blue-500 hover:bg-blue-50 transition-colors"
            :title="t('comments.edit')"
            @click="emit('edit', comment)"
          >
            <Pencil :size="13" />
          </button>
          <button
            class="p-1 rounded-full text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors"
            :title="t('comments.delete')"
            @click="emit('delete', comment)"
          >
            <Trash2 :size="13" />
          </button>
        </div>-->
      </div>

      <p class="text-gray-700 leading-relaxed text-xs">{{ comment.comment_text }}</p>
    </div>

  </div>
</template>