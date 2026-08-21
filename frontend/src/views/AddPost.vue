<script setup>
import { ref } from 'vue'
import { ArrowLeft, Image as ImageIcon, X, Video } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { addPost } from '../services/api'
import { checkAuth } from '../auth'
const router = useRouter()
const { t } = useI18n()

const fileInput = ref(null)
const uploadedFiles = ref([])


const title = ref('')
const category = ref('')
const description = ref('')

const submitPost = async (e) => {
  try {
    if(!title.value || !category.value || !description.value){
      alert(t('addPost.fillAllFields'))
      return;
    }
    e.preventDefault()
    const response = await addPost({
      title: title.value,
      category: category.value,
      description: description.value,
      attachments: uploadedFiles.value
    })
    alert(t('addPost.postSubmitted'))
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
    <!-- Header -->
    <header
      class="flex items-center px-5 py-5 sticky top-0 bg-white z-20 border-b border-gray-50"
    >
      <button
        @click="router.back()"
        class="p-2 -ml-2 rounded-full hover:bg-gray-100 transition-colors"
      >
        <ArrowLeft class="w-6 h-6 text-gray-800" />
      </button>

      <h2 class="font-bold text-lg text-gray-900 mx-auto -ml-2">
        {{ t('addPost.headerTitle') }}
      </h2>

      <div class="w-6"></div>
    </header>

    <div class="px-5 pt-2 pb-12">
      <form class="space-y-6">

        <!-- Description -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            {{ t('addPost.titleLabel') }}
            <span class="text-red-500">*</span>
          </label>

          <input
            v-model="title"
            :placeholder="t('addPost.titlePlaceholder')"
            class="w-full bg-white border border-gray-200 rounded-2xl p-4 text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm resize-none"
          ></input>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            {{ t('addPost.description') }}
            <span class="text-red-500">*</span>
          </label>

          <textarea
            rows="3"
            v-model="description"
            :placeholder="t('addPost.descriptionPlaceholder')"
            class="w-full bg-white border border-gray-200 rounded-2xl p-4 text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm resize-none"
          ></textarea>
        </div>

        <!-- Action Category -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            {{ t('addPost.category') }}
            <span class="text-red-500">*</span>
          </label>

          <select
            v-model="category"
            class="w-full bg-white border border-gray-200 rounded-2xl px-4 py-2 text-gray-600 appearance-none focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm font-medium"
          >
            <option value="" disabled selected>
              {{ t('addPost.selectCategory') }}
            </option>

            <option value="Agriculture & Livelihood">{{ t('categories.agricultureLivelihood') }}</option>
            <option value="Health & Nutrition">{{ t('categories.healthNutrition') }}</option>
            <option value="Education">{{ t('categories.education') }}</option>
            <option value="Civic Action & Governance">{{ t('categories.civicGovernance') }}</option>
            <option value="Sports & Fitness">{{ t('categories.sportsFitness') }}</option>
          </select>
        </div>

        <!-- Media -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-1">
            {{ t('addPost.media') }}
          </label>

          <p class="text-xs text-gray-500 mb-3">
            {{ t('addPost.mediaHint') }}
          </p>

          <!-- Hidden File Input -->
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleFileChange"
          />

          <!-- Upload Box -->
          <div
            v-if="uploadedFiles.length === 0"
            class="border-2 border-dashed rounded-2xl p-1 flex flex-col items-center justify-center transition-colors cursor-pointer group"
            :class="'border-gray-300 bg-gray-50 hover:bg-gray-100'"
            @click="handleMediaClick"
          >
            <div
              class="w-14 h-14 bg-blue-50 rounded-full flex items-center justify-center mb-4 group-hover:scale-105 transition-transform"
            >
              <ImageIcon class="w-6 h-6 text-primary-500" />
            </div>

            <span class="font-bold text-gray-900 text-sm">
              {{ t('addPost.addPhotoVideo') }}
            </span>

            <span class="text-sm text-gray-500 mt-1">
              {{ t('addPost.tapToBrowse') }}
            </span>
          </div>

          <!-- Preview Grid -->
          <div
            v-if="uploadedFiles.length"
            class="grid grid-cols-3 gap-3 mt-4"
          >
            <div
              v-for="(item, index) in uploadedFiles"
              :key="index"
              class="relative rounded-2xl overflow-hidden border border-gray-200 bg-gray-100"
            >
              <!-- Image -->
              <img
                v-if="item.preview"
                :src="item.preview"
                class="w-full h-28 object-cover"
              />

              <!-- Video -->
              <div
                v-else
                class="h-28 flex flex-col items-center justify-center text-gray-600 text-xs p-2 text-center"
              >
                <Video class="w-6 h-6 mb-2" />
                <span class="line-clamp-2">
                  {{ item.file.name }}
                </span>
              </div>

              <!-- Remove -->
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

        <!-- Submit -->
        <button
          @click="submitPost"
          type="button"
          class="w-full bg-primary-600 hover:bg-primary-700 text-white font-bold rounded-2xl p-4 shadow-lg shadow-primary-500/30 transition-colors uppercase tracking-wider text-sm"
        >
          {{ t('addPost.submit') }}
        </button>
      </form>
    </div>
  </div>
</template>