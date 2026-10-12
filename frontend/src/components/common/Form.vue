<script setup>
import { onUnmounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { SPEECH_RECOGNITION_LOCALES } from '@/i18n'

const { locale } = useI18n()

const isListening = ref(false)
const isStopping = ref(false)
const recognition = ref(null)
const voiceInputRefs = {}
let manualStop = false

const startVoiceInput = (field) => {
  if (isListening.value) {
    manualStop = true
    isStopping.value = true
    recognition.value?.stop()
    return
  }

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition

  if (!SpeechRecognition) {
    field.voiceInputError = field.voiceInput.notSupportedMessage
    return
  }

  const textarea = voiceInputRefs[field.key]
  const baseText = textarea ? textarea.value : ''
  let sessionFinalText = ''
  manualStop = false

  recognition.value = new SpeechRecognition()
  recognition.value.lang = SPEECH_RECOGNITION_LOCALES[locale.value] || 'en-IN'
  recognition.value.interimResults = true
  // One short session at a time, auto-restarted in onend below, instead of
  // relying on continuous:true — Chrome's continuous mode silently restarts
  // recognition internally after each pause, which can briefly revert the
  // transcript before it catches back up. Chaining clean single-utterance
  // sessions avoids that flicker.
  recognition.value.continuous = false

  recognition.value.onstart = () => {
    isListening.value = true
  }

  recognition.value.onresult = (event) => {
    let interimTranscript = ''

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript

      if (event.results[i].isFinal) {
        sessionFinalText += transcript + ' '
      } else {
        interimTranscript += transcript
      }
    }

    const textareaEl = voiceInputRefs[field.key]

    if (textareaEl) {
      const separator = baseText && !/\s$/.test(baseText) ? ' ' : ''
      textareaEl.value =
        (baseText + separator + sessionFinalText + interimTranscript).trim()
    }
  }

  recognition.value.onerror = (event) => {
    // A pause with nothing said yet just triggers 'no-speech' — quietly
    // let onend restart instead of surfacing it as a real error.
    if (event.error === 'no-speech') return

    field.voiceInputError = event.error === 'not-allowed'
      ? field.voiceInput.permissionDeniedMessage || field.voiceInput.errorMessage
      : field.voiceInput.errorMessage
    manualStop = true
  }

  recognition.value.onend = () => {
    if (manualStop) {
      isListening.value = false
      isStopping.value = false
      return
    }

    // A small delay avoids an InvalidStateError some browsers throw when
    // start() is called again before the previous session has fully torn down.
    setTimeout(() => {
      if (!manualStop) recognition.value?.start()
    }, 0)
  }

  recognition.value.start()
}

// Stop listening (and the auto-restart loop in onend) if the form is
// navigated away from mid-recording, so the mic doesn't stay on in the background.
onUnmounted(() => {
  manualStop = true
  recognition.value?.stop()
})

const setVoiceInputRef = (key) => (element) => {
  if (element) {
    voiceInputRefs[key] = element
  }
}
const props = defineProps({
  fields: {
    type: Array,
    required: true
  },
  submitLabel: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['submit'])

const submitForm = (event) => {
  const formData = new FormData(event.target)
  const data = Object.fromEntries(formData.entries())

  const consentField = props.fields.find(
    field => field.type === 'consent'
  )

  if (consentField) {
    data[consentField.key] = formData.has(consentField.key)
  }

  emit('submit', data)
}
</script>

<template>
  <form
    class="space-y-4"
    @submit.prevent="submitForm"
  >

    <div
      v-for="field in fields"
      :key="field.key"
    >
      <!-- Text / Email / Tel / Number -->
      <div v-if="['text', 'email', 'tel', 'number'].includes(field.type)">
        <label class="mb-1 block text-sm font-medium text-gray-700">
          {{ field.label }}

          <span
            v-if="field.required"
            class="text-red-500"
          >
            *
          </span>
        </label>

        <input
          :name="field.key"
          :type="field.type"
          :min="field.min"
          :placeholder="field.placeholder"
          :value="field.value ?? ''"
          :readonly="field.editable === false"
          :required="field.required"
          :class="[
            'w-full rounded-md border border-gray-300 px-3 py-2 text-sm',
            field.editable === false
              ? 'bg-gray-100 text-gray-500'
              : 'text-gray-700'
          ]"
        />
      </div>

      <!-- Radio -->
      <div v-else-if="field.type === 'radio'">
        <label class="mb-2 block text-sm font-medium text-gray-700">
          {{ field.label }}

          <span
            v-if="field.required"
            class="text-red-500"
          >
            *
          </span>
        </label>

        <div class="space-y-2">
          <label
            v-for="option in field.options"
            :key="option.value"
            class="flex items-center gap-2 text-sm text-gray-700"
          >
            <input
              :name="field.key"
              type="radio"
              :value="option.value"
              :required="field.required"
            />

            {{ option.label }}
          </label>
        </div>
      </div>

      <!-- Dropdown -->
      <div v-else-if="field.type === 'dropdown'">
        <label class="mb-1 block text-sm font-medium text-gray-700">
          {{ field.label }}

          <span
            v-if="field.required"
            class="text-red-500"
          >
            *
          </span>
        </label>

        <select
          :name="field.key"
          :disabled="field.editable === false"
          class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-700"
        >
          <option
            value=""
            disabled
          >
            {{ field.placeholder }}
          </option>

          <option
            v-for="option in field.options"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Textarea -->
      <div v-else-if="field.type === 'textarea'">
        <label class="mb-2 block text-sm font-medium text-gray-700">
          {{ field.label }}

          <span
            v-if="field.required"
            class="text-red-500"
          >
            *
          </span>
        </label>

        <textarea
          :ref="field.voiceInput?.enabled
            ? setVoiceInputRef(field.key)
            : undefined"
          :name="field.key"
          rows="4"
          :placeholder="field.placeholder"
          :readonly="field.editable === false"
          :required="field.required"
          class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-700"
        ></textarea>
        <button
          v-if="field.voiceInput?.enabled"
          type="button"
          @click="startVoiceInput(field)"
          :disabled="isStopping"
          class="mt-2 w-full rounded-md border border-primary-600 bg-primary-50 px-3 py-2 text-sm font-medium text-primary-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ isStopping
            ? (field.voiceInput.stoppingLabel || field.voiceInput.listeningLabel)
            : isListening
              ? field.voiceInput.listeningLabel
              : field.voiceInput.label
          }}
        </button>

        <p
          v-if="field.voiceInputError"
          class="mt-2 text-sm text-red-600"
        >
          {{ field.voiceInputError }}
        </p>
      </div>

      <!-- Consent -->
      <div v-else-if="field.type === 'consent'">
        <label class="flex items-start gap-2 text-sm text-gray-700">
          <input
            :name="field.key"
            type="checkbox"
            :required="field.required"
            class="mt-1"
          />

          <span>
            {{ field.label }}
          </span>
        </label>
      </div>
    </div>

    <button
      type="submit"
      :disabled="loading"
      class="w-full rounded-lg bg-primary-600 px-6 py-3 text-base font-semibold text-white transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {{ submitLabel }}
    </button>
    <p
      v-if="error"
      class="text-sm text-red-600"
    >
      {{ error }}
    </p>

  </form>
</template>