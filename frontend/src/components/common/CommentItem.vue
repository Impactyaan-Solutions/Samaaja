
<script setup>
import { ref, computed } from 'vue'
import { getTimeSinceCreation } from '@/utils/utils'
import { authState } from '@/auth'
import { Pencil, Trash2 } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { updateComment } from '@/services/api'

const { t } = useI18n()

const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete', 'updated'])

const isEditing = ref(false)
const editedText = ref('')
const isSaving = ref(false)
const errorMessage = ref('')

const authCache = JSON.parse(
  localStorage.getItem('samaaja_auth_cache') || '{}'
)

const currentUser = computed(
  () => authState.email || authCache.email
)

const isOwner = computed(
  () => props.comment.user_id === currentUser.value
)

function startEditing() {
  editedText.value = props.comment.comment_text || ''
  errorMessage.value = ''
  isEditing.value = true
}

function cancelEditing() {
  isEditing.value = false
  editedText.value = ''
  errorMessage.value = ''
}

async function saveComment() {
  const text = editedText.value.trim()

  if (!text) {
    errorMessage.value = 'Comment cannot be empty.'
    return
  }

  if (text === props.comment.comment_text) {
    cancelEditing()
    return
  }

  isSaving.value = true
  errorMessage.value = ''

  try {
    await updateComment(props.comment.name, text)

    emit('updated', {
      ...props.comment,
      comment_text: text
    })

    isEditing.value = false
  } catch (error) {
    console.error('Failed to update comment:', error)
    errorMessage.value = 'Failed to update comment. Please try again.'
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div class="flex items-start space-x-3 text-sm">
    <div
      class="w-8 h-8 rounded-full shrink-0 overflow-hidden bg-gray-100
             text-gray-700 flex items-center justify-center font-bold text-xs"
    >
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
      <div class="flex items-start justify-between mb-1">
        <div>
          <span class="font-semibold text-gray-900 text-xs">
            {{ comment.full_name }}
          </span>

          <div class="text-[10px] text-gray-400 font-medium">
            {{ getTimeSinceCreation(comment.creation) }}
          </div>
        </div>

        <div v-if="isOwner && !isEditing" class="flex items-center gap-1.5">
          <button
            class="p-1 rounded-full text-gray-400 hover:text-blue-500"
            :title="t('comments.edit')"
            @click="startEditing"
          >
            <Pencil :size="13" />
          </button>

          <button
            class="p-1 rounded-full text-gray-400 hover:text-red-500"
            :title="t('comments.delete')"
            @click="emit('delete', comment)"
          >
            <Trash2 :size="13" />
          </button>
        </div>
      </div>

      <div v-if="isEditing">
        <textarea
          v-model="editedText"
          rows="3"
          class="w-full rounded-lg border border-gray-300 bg-white p-2 text-xs
                 focus:outline-none focus:ring-2 focus:ring-blue-300"
          placeholder="Edit your comment..."
          :disabled="isSaving"
        />

        <p v-if="errorMessage" class="mt-1 text-xs text-red-500">
          {{ errorMessage }}
        </p>

        <div class="mt-2 flex justify-end gap-2">
          <button
            class="rounded-lg border px-3 py-1 text-xs"
            :disabled="isSaving"
            @click="cancelEditing"
          >
            Cancel
          </button>

          <button
            class="rounded-lg bg-blue-600 px-3 py-1 text-xs text-white
                   disabled:opacity-50"
            :disabled="isSaving"
            @click="saveComment"
          >
            {{ isSaving ? 'Saving...' : 'Save' }}
          </button>
        </div>
      </div>

      <p v-else class="text-gray-700 leading-relaxed text-xs whitespace-pre-wrap">
        {{ comment.comment_text }}
      </p>
    </div>
  </div>
</template>
