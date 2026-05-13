<script setup>
import { ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { completeProfile } from '@/services/api';
import { checkAuth, authState } from '@/auth';
import { User, Calendar, Phone, BookOpen, Tag } from 'lucide-vue-next';

const { t } = useI18n();
const router = useRouter();

const formData = ref({
  gender: '',
  bio: '',
  category: '',
  dob: '',
  mobileNumber: ''
});

const isSubmitting = ref(false);
const errorMessage = ref('');

const isFormValid = computed(() => {
  return formData.value.gender && 
         formData.value.bio && 
         formData.value.category && 
         formData.value.dob && 
         formData.value.mobileNumber;
});

const submitForm = async () => {
  if (!isFormValid.value) return;
  
  isSubmitting.value = true;
  errorMessage.value = '';

  try {
    await completeProfile({
      user_gender: formData.value.gender,
      user_bio: formData.value.bio,
      user_category: formData.value.category,
      user_dob: formData.value.dob,
      user_mobile_no: formData.value.mobileNumber,
      user_email: authState.email
    });

    await checkAuth();
    router.push({ name: 'home' });
    
  } catch (error) {
    console.error("Profile update failed:", error);
    errorMessage.value = t('complete_profile.error_msg');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex justify-center font-sans">
    <div class="bg-white w-full max-w-md min-h-screen px-6 py-10 flex flex-col">
      
      <div class="mb-2">
        <h2 class="text-3xl font-extrabold text-gray-900 tracking-tight mb-2">{{ t('complete_profile.title') }}</h2>
        <p class="text-gray-500 text-sm leading-relaxed">
          {{ t('complete_profile.subtitle') }}
        </p>
      </div>

      <div v-if="errorMessage" class="mb-6 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="submitForm" class="flex-1 flex flex-col space-y-5">
        
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('complete_profile.gender') }}</label>
          <div class="relative flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><User :size="14" /></span>
            <select v-model="formData.gender" required class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent appearance-none">
              <option value="" disabled>{{ t('complete_profile.gender_placeholder') }}</option>
              <option value="Male">{{ t('complete_profile.male') }}</option>
              <option value="Female">{{ t('complete_profile.female') }}</option>
              <option value="Other">{{ t('complete_profile.other') }}</option>
            </select>
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('complete_profile.category') }}</label>
          <div class="relative flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><Tag :size="14" /></span>
            <select v-model="formData.category" required class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent appearance-none">
              <option value="" disabled>{{ t('complete_profile.cat_placeholder') }}</option>
              <option value="Volunteer">{{ t('complete_profile.volunteer') }}</option>
              <option value="Citizen">{{ t('complete_profile.citizen') }}</option>
            </select>
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('complete_profile.dob') }}</label>
          <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><Calendar :size="14" /></span>
            <input 
              v-model="formData.dob"
              type="date" 
              required
              class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent"
            />
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('complete_profile.mobile') }}</label>
          <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><Phone :size="14" /></span>
            <input 
              v-model="formData.mobileNumber"
              type="tel" 
              required
              :placeholder="t('complete_profile.mobile_placeholder')"
              class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent"
            />
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('complete_profile.bio') }}</label>
          <div class="flex border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 pt-3.5 text-gray-400"><BookOpen :size="14" /></span>
            <textarea 
              v-model="formData.bio"
              required
              :placeholder="t('complete_profile.bio_placeholder')"
              rows="3"
              class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent resize-none"
            ></textarea>
          </div>
        </div>

        <button
          type="submit"
          :disabled="!isFormValid || isSubmitting"
          class="w-full py-2 mt-2 rounded-xl font-bold transition-all shadow-md flex justify-center items-center"
          :class="isFormValid && !isSubmitting ? 'bg-blue-600 hover:bg-blue-700 text-white active:scale-[0.98]' : 'bg-gray-200 text-gray-400 cursor-not-allowed'"
        >
          <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isSubmitting ? t('complete_profile.save_btn') : t('complete_profile.submit_btn') }}
        </button>

      </form>
    </div>
  </div>
</template>