<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ArrowLeft, Image as ImageIcon, X, Video } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { logAction } from '../services/api'
import { checkAuth } from '../auth'

const { t } = useI18n()
const router = useRouter()

const fileInput = ref(null)
const uploadedFiles = ref([])


const type = ref('')
const category = ref('')
const description = ref('')
const hours_invested = ref('')

const submitAction = async (e) => {
  try {
    e.preventDefault()
    const response = await logAction({
      type: type.value,
      category: category.value,
      description: description.value,
      hours_invested: hours_invested.value,
      attachments: uploadedFiles.value
    })
    alert(t('log_action.success'))
    await checkAuth()
    router.push({ name: 'home' });
  } catch (error) {
    console.error('Error logging action:', error)
  }
}

const handleMediaClick = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const files = Array.from(event.target.files || [])
  processFiles(files)
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const processFiles = (files) => {
  if (files.length === 0) return;
  const file = files[0];
  const mappedFile = {
    file,
    type: file.type,
    preview: file.type.startsWith('image/')
      ? URL.createObjectURL(file)
      : null,
  };

  uploadedFiles.value = [mappedFile];
}

const removeFile = (index) => {
  const item = uploadedFiles.value[index]
  if (item.preview) {
    URL.revokeObjectURL(item.preview)
  }
  uploadedFiles.value.splice(index, 1)
}
</script>

<template>
  <div class="min-h-full bg-white">
    <header class="flex items-center px-5 py-5 sticky top-0 bg-white z-20 border-b border-gray-50">
      <button
        @click="router.back()"
        class="p-2 -ml-2 rounded-full hover:bg-gray-100 transition-colors"
      >
        <ArrowLeft class="w-6 h-6 text-gray-800" />
      </button>

      <h2 class="font-bold text-lg text-gray-900 mx-auto -ml-2">
        {{ t('log_action.title') }}
      </h2>

      <div class="w-6"></div>
    </header>

    <div class="px-5 pt-2 pb-12">
      <form class="space-y-6">
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            {{ t('log_action.type_label') }}
            <span class="text-red-500">*</span>
          </label>
          <select
            v-model="type"
            class="w-full bg-white border border-gray-200 rounded-2xl px-4 py-2 text-gray-600 appearance-none focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm font-medium"
          >
            <option value="" disabled selected>{{ t('log_action.type_placeholder') }}</option>
            <option value="On-Ground Action">{{ t('log_action.type_on_ground') }}</option>
            <option value="Data & Reporting">{{ t('log_action.type_data') }}</option>
            <option value="Training & Mentoring">{{ t('log_action.type_training') }}</option>
            <option value="Events & Activities">{{ t('log_action.type_events') }}</option>
            <option value="Outreach & Awareness">{{ t('log_action.type_outreach') }}</option>
            <option value="Community Engagement">{{ t('log_action.type_community') }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            {{ t('log_action.category_label') }}
            <span class="text-red-500">*</span>
          </label>

          <select
            v-model="category"
            class="w-full bg-white border border-gray-200 rounded-2xl px-4 py-2 text-gray-600 appearance-none focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm font-medium"
          >
            <option value="" disabled selected>{{ t('log_action.category_placeholder') }}</option>
            <option value="Water">{{ t('log_action.cat_water') }}</option>
            <option value="Climate">{{ t('log_action.cat_climate') }}</option>
            <option value="Civic">{{ t('log_action.cat_civic') }}</option>
            <option value="Education">{{ t('log_action.cat_education') }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            {{ t('log_action.desc_label') }}
            <span class="text-red-500">*</span>
          </label>

          <textarea
            rows="3"
            v-model="description"
            :placeholder="t('log_action.desc_placeholder')"
            class="w-full bg-white border border-gray-200 rounded-2xl p-4 text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm resize-none"
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            {{ t('log_action.hours_label') }}
            <span class="text-red-500">*</span>
          </label>

          <input
            type="number"
            min="0"
            v-model="hours_invested"
            max="24"
            step="0.5"
            placeholder="0"
            class="w-full bg-white border border-gray-200 rounded-xl p-2 text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm resize-none"
          />
        </div>

        <div>
          <label class="block text-sm font-bold text-gray-900 mb-1">
            {{ t('log_action.media_label') }}
          </label>

          <p class="text-xs text-gray-500 mb-3">{{ t('log_action.media_hint') }}</p>

          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleFileChange"
          />

          <div
            v-if="uploadedFiles.length === 0"
            class="border-2 border-dashed rounded-2xl p-1 flex flex-col items-center justify-center transition-colors cursor-pointer group"
            :class="'border-gray-300 bg-gray-50 hover:bg-gray-100'"
            @click="handleMediaClick"
          >
            <div class="w-14 h-14 bg-blue-50 rounded-full flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
              <ImageIcon class="w-6 h-6 text-primary-500" />
            </div>

            <span class="font-bold text-gray-900 text-sm">{{ t('log_action.add_media_text') }}</span>
            <span class="text-sm text-gray-500 mt-1">{{ t('log_action.tap_hint') }}</span>
          </div>

          <div v-if="uploadedFiles.length" class="grid grid-cols-3 gap-3 mt-4">
            <div
              v-for="(item, index) in uploadedFiles"
              :key="index"
              class="relative rounded-2xl overflow-hidden border border-gray-200 bg-gray-100"
            >
              <img v-if="item.preview" :src="item.preview" class="w-full h-28 object-cover" />
              <div v-else class="h-28 flex flex-col items-center justify-center text-gray-600 text-xs p-2 text-center">
                <Video class="w-6 h-6 mb-2" />
                <span class="line-clamp-2">{{ item.file.name }}</span>
              </div>
              <button
                type="button"
                class="absolute top-2 right-2 bg-black/60 text-white rounded-full p-1"
                @click.stop="removeFile(index)"
              >
                <X class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <button
          @click="submitAction"
          type="button"
          class="w-full bg-primary-600 hover:bg-primary-700 text-white font-bold rounded-2xl p-4 shadow-lg shadow-primary-500/30 transition-colors uppercase tracking-wider text-sm"
        >
          {{ t('log_action.submit') }}
        </button>
      </form>
    </div>
  </div>
</template>