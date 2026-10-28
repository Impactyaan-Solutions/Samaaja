<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { completeProfile, getMetadataOptions } from '@/services/api';
import { checkAuth, authState } from '@/auth';
import { User, Phone, Mail, Tag } from 'lucide-vue-next';

const router = useRouter();
const { t } = useI18n();
const formData = ref({
  name: '',
  mobileNumber: '',
  gender: ''
});

const isSubmitting = ref(false);
const errorMessage = ref('');
const genderOptions = ref([]);

onMounted(() => {
  formData.value.name = authState.profile.fullName || '';
  formData.value.mobileNumber = authState.profile.mobileNumber || '';
  formData.value.gender = authState.profile.gender || '';
});

const fetchMetadataOptions = async () => {
  try {
    genderOptions.value = await getMetadataOptions('Gender');
  } catch (error) {
    console.error('Failed to load metadata options:', error);
    errorMessage.value = 'Failed to load profile options. Please refresh the page.';
  }
};

onMounted(() => {
  fetchMetadataOptions();
});

const isFormValid = computed(() => {
  return formData.value.name && formData.value.mobileNumber && formData.value.gender;
});

const submitForm = async () => {
  if (!isFormValid.value) return;

  isSubmitting.value = true;
  errorMessage.value = '';

  try {
    await completeProfile({
      user_name: formData.value.name,
      user_mobile_no: formData.value.mobileNumber,
      user_gender: formData.value.gender
    });

    // Refresh the local authState cache to pull down the newly saved data
    await checkAuth();

    // The router guard will automatically allow us into the home page now
    router.push({ name: 'home' });

  } catch (error) {
    console.error(error);
    errorMessage.value = error.message;
  } finally {
    isSubmitting.value = false;
  }
};

</script>

<template>
  <div class="min-h-screen bg-gray-50 flex justify-center font-sans">
    <div class="bg-white w-full max-w-md min-h-screen px-6 py-10 flex flex-col">

      <div class="mb-2">
        <h2 class="text-3xl font-extrabold text-gray-900 tracking-tight mb-2">{{ t('profileCompletion.title') }}</h2>
        <p class="text-gray-500 text-sm leading-relaxed">
          {{ t('profileCompletion.subtitle') }}
        </p>
      </div>

      <div v-if="errorMessage" class="mb-6 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="submitForm" class="flex-1 flex flex-col space-y-5">

        <!-- Name -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('profileCompletion.name') }}</label>
          <div class="relative flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><User :size="14" /></span>
            <input
              v-model="formData.name"
              type="text"
              required
              :placeholder="t('profileCompletion.namePlaceholder')"
              class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent"
            />
          </div>
        </div>

        <!-- Mobile Number -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('profileCompletion.mobileNumber') }}</label>
          <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><Phone :size="14" /></span>
            <input
              v-model="formData.mobileNumber"
              type="tel"
              required
              :placeholder="t('profileCompletion.mobileNumberPlaceholder')"
              class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent"
            />
          </div>
        </div>

        <!-- Gender -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('profileCompletion.gender') }}</label>
          <div class="relative flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><Tag :size="14" /></span>
            <select v-model="formData.gender" required class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent appearance-none">
              <option value="" disabled>{{ t('profileCompletion.selectGender') }}</option>
              <option v-for="option in genderOptions" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>
        </div>

        <!-- Email (read-only: it's the account's sign-in identity) -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">{{ t('profileCompletion.email') }}</label>
          <div class="flex items-center border border-gray-100 rounded-xl overflow-hidden bg-gray-100">
            <span class="pl-4 text-gray-400"><Mail :size="14" /></span>
            <input
              :value="authState.email"
              type="email"
              disabled
              class="w-full px-1 py-1.5 outline-none text-gray-500 bg-transparent"
            />
          </div>
        </div>

        <!-- Submit Button -->
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
          {{ isSubmitting ? t('profileCompletion.savingProfile') : t('profileCompletion.completeRegistration') }}
        </button>

      </form>
    </div>
  </div>
</template>
