<script setup>
import { ref } from 'vue'
import { X, Send } from 'lucide-vue-next'
import { authState } from '@/auth'
import { createComment, getComments } from '@/services/api'
import CommentItem from './CommentItem.vue'
import { onMounted } from 'vue'
const props = defineProps({
  postId: {
    type: String,
    required: true
  },
  commentCount: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['close', 'comment-added'])

const comments = ref([])
const commentText = ref('')
const page = ref(1)
const pageSize = 10
const loading = ref(false)
const hasMore = ref(true)
const commentContainer = ref(null)

// const userEmail = ref("")
// userEmail.value = authCache?.email;
// const isOwner = props.comment.user_id === userEmail.value;
const fetchComments = async (reset = false) => {
  if (loading.value || (!hasMore.value && !reset)) return

  loading.value = true

  if (reset) {
    page.value = 1
    comments.value = []
    hasMore.value = true
  }

  try {
    const response = await getComments(
      props.postId,
      page.value,
      pageSize
    )

    const newComments = response.comments || []

    if (reset) {
      comments.value = newComments
    } else {
      comments.value = [
        ...newComments,
        ...comments.value
      ]
    }

    if (newComments.length < pageSize) {
      hasMore.value = false
    } else {
      page.value++
    }
  } finally {
    loading.value = false
  }
}
onMounted(() => {
  fetchComments()
})
const submitComment = async () => {
  if (!commentText.value.trim()) return

  try {
    const response = await createComment(props.postId, commentText.value.trim())
    comments.value.push(response)
    commentText.value = ''
    emit('comment-added')
    fetchComments()
  } catch (error) {
    console.error("Failed to submit comment:", error)
  }
}


const handleScroll = async (e) => {
  const el = e.target
  if (el.scrollTop <= 10) {
    await fetchComments()
  }
}
const handleEdit = (comment) => {
  // TODO: implement edit flow
  console.log('Edit comment:', comment)
}

const handleDelete = (comment) => {
  // TODO: implement delete flow + remove from comments.value
  console.log('Delete comment:', comment)
}

defineExpose({ fetchComments })
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div class="fixed inset-0 bg-black/40 z-40" @click="emit('close')" />
    </Transition>

    <Transition name="slide-up">
      <div class="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-sm z-50 bg-white rounded-t-2xl shadow-2xl max-h-[70vh] flex flex-col">
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
          <h3 class="font-semibold text-gray-900 text-sm">
            Comments <span class="text-gray-400 font-normal">({{ commentCount }})</span>
          </h3>
          <button @click="emit('close')" class="p-1 rounded-full hover:bg-gray-100 transition-colors">
            <X class="w-5 h-5 text-gray-500" />
          </button>
        </div>

       
<div
  ref="commentContainer"
  class="flex-1 overflow-y-auto px-4 py-3 space-y-4"
  @scroll="handleScroll"
>
  <p
    v-if="comments.length === 0"
    class="text-center text-sm text-gray-400 py-8"
  >
    No comments yet. Be the first!
  </p>

  <CommentItem
    v-else
    v-for="comment in comments"
    :key="comment.id"
    :comment="comment"
    @edit="handleEdit"
    @delete="handleDelete"
  />
</div>
       

        <div class="px-4 py-3 border-t border-gray-100 flex items-center space-x-3 bg-white">
        <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xs shrink-0 overflow-hidden">
  <img
    v-if="authState.profile?.image || authState.profile?.imageBase64"
    :src="authState.profile.image || authState.profile.imageBase64"
    alt="avatar"
    class="w-full h-full object-cover"
  />
  <span v-else>
    {{ authState.profile?.fullName?.charAt(0)?.toUpperCase()|| '?' }}
  </span>
</div>
          <input
            v-model="commentText"
            type="text"
            placeholder="Write a comment..."
            class="flex-1 bg-gray-50 rounded-full px-4 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-200 border border-gray-100"
            @keyup.enter="submitComment"
          />
          <button
            @click="submitComment"
            :disabled="!commentText.trim()"
            class="p-2 rounded-full bg-blue-500 text-white hover:bg-blue-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <Send class="w-4 h-4" />
          </button>
        </div>
           </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>