<script setup>
defineProps({
  show: Boolean,
  item: Object // Expecting { type: 'ACTION' | 'POST', title: '...', description: '...', meta: '...' }
})

const emit = defineEmits(["close"])
</script>

<template>
  <Transition name="fade">
    <div
      v-if="show"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      @click.self="emit('close')"
    >
      <div class="bg-white rounded-2xl w-full max-w-md shadow-xl border border-slate-100 overflow-hidden transform transition-all">
        
        <div class="p-6">
         
         

          <p v-if="item?.meta" class="text-xs text-slate-500 mt-1 mb-4 flex items-center gap-1.5">
            {{ item.meta }}
          </p>

          <hr class="border-slate-100 my-4" />

          <p class="text-sm text-slate-600 whitespace-pre-wrap leading-relaxed">
            {{ item?.description || 'No description provided.' }}
          </p>
        </div>

       

      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Smooth fade transition for the modal backdrop overlay */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>