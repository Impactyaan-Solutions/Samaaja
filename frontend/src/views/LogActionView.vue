<script setup>
import { ArrowLeft, Zap, Image as ImageIcon, MapPin } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="min-h-full bg-white">
    <!-- Header -->
    <header class="flex items-center px-5 py-5 sticky top-0 bg-white z-20 border-b border-gray-50">
      <button @click="router.back()" class="p-2 -ml-2 rounded-full hover:bg-gray-100 transition-colors">
        <ArrowLeft class="w-6 h-6 text-gray-800" />
      </button>
      <h2 class="font-bold text-lg text-gray-900 mx-auto -ml-2">Log Action</h2>
      <div class="w-6"></div> <!-- Spacer for centering -->
    </header>

    <div class="px-5 pt-6 pb-12">
      <form class="space-y-6">
        <!-- Action Type -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">Action Type</label>
          <div class="flex items-center bg-gray-50 border border-gray-100 rounded-2xl p-4 shadow-inner">
            <Zap class="w-5 h-5 text-gray-400 mr-3" />
            <input 
              type="text" 
              value="Log your Action" 
              class="bg-transparent w-full text-gray-800 font-medium focus:outline-none"
              readonly
            />
          </div>
        </div>

        <!-- Action Category -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            Action Category <span class="text-red-500">*</span>
          </label>
          <select class="w-full bg-white border border-gray-200 rounded-2xl p-4 text-gray-600 appearance-none focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm font-medium">
            <option value="" disabled selected>Select a category...</option>
            <option value="water">Water Conservation</option>
            <option value="cleanliness">Cleanliness</option>
            <option value="education">Education</option>
          </select>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">
            Description <span class="text-red-500">*</span>
          </label>
          <textarea 
            rows="5"
            placeholder="What impact did you make today?&#10;(Supports local language typing)"
            class="w-full bg-white border border-gray-200 rounded-2xl p-4 text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-sm resize-none"
          ></textarea>
        </div>

        <!-- Media -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-1">
            Media (Optional)
          </label>
          <p class="text-xs text-gray-500 mb-3">(Adding photos improves trust)</p>
          <div class="border-2 border-dashed border-gray-300 rounded-2xl p-10 flex flex-col items-center justify-center bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer group">
            <div class="w-14 h-14 bg-blue-50 rounded-full flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
              <ImageIcon class="w-6 h-6 text-primary-500" />
            </div>
            <span class="font-bold text-gray-900 text-sm">Add photos or videos</span>
            <span class="text-sm text-gray-500 mt-1">Tap to browse from your device</span>
          </div>
        </div>

        <!-- Location -->
        <div>
          <label class="block text-sm font-bold text-gray-900 mb-2">Location</label>
          <button type="button" class="w-full bg-white border border-gray-200 rounded-2xl p-4 text-gray-700 flex items-center justify-center space-x-2 hover:bg-gray-50 shadow-sm mb-6">
            <MapPin class="w-5 h-5 text-gray-400" />
            <span class="font-semibold">Add Location</span>
          </button>
        </div>
        
        <button type="submit" class="w-full bg-primary-600 hover:bg-primary-700 text-white font-bold rounded-2xl p-4 shadow-lg shadow-primary-500/30 transition-colors uppercase tracking-wider text-sm">
          Submit Action
        </button>
      </form>
    </div>
  </div>
</template>
