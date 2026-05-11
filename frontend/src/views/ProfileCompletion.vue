<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { completeProfile } from '@/services/api';
import { checkAuth, authState } from '@/auth';
import { User, Calendar, Phone, BookOpen, Tag } from 'lucide-vue-next';

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
    // Call the backend update API
    console.log(authState.email)
    await completeProfile({
      user_gender: formData.value.gender,
      user_bio: formData.value.bio,
      user_category: formData.value.category,
      user_dob: formData.value.dob,
      user_mobile_no: formData.value.mobileNumber,
      user_email: authState.email
    });

    // Refresh the local authState cache to pull down the newly saved data
    await checkAuth();

    // The router guard will automatically allow us into the home page now
    router.push({ name: 'home' });
    
  } catch (error) {
    console.error("Profile update failed:", error);
    errorMessage.value = "Failed to update profile. Please try again or check your backend API configuration.";
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex justify-center font-sans">
    <div class="bg-white w-full max-w-md min-h-screen px-6 py-10 flex flex-col">
      
      <div class="mb-2">
        <h2 class="text-3xl font-extrabold text-gray-900 tracking-tight mb-2">Complete Profile</h2>
        <p class="text-gray-500 text-sm leading-relaxed">
          Almost there! We just need a few more details to set up your account.
        </p>
      </div>

      <div v-if="errorMessage" class="mb-6 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="submitForm" class="flex-1 flex flex-col space-y-5">
        
        <!-- Gender -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">Gender</label>
          <div class="relative flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><User :size="14" /></span>
            <select v-model="formData.gender" required class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent appearance-none">
              <option value="" disabled>Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        <!-- Category -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">Category</label>
          <div class="relative flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><Tag :size="14" /></span>
            <select v-model="formData.category" required class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent appearance-none">
              <option value="" disabled>Select Category</option>
              <option value="Volunteer">Volunteer</option>
              <option value="Citizen">Citizen</option>
            </select>
          </div>
        </div>

        <!-- Date of Birth -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">Date of Birth</label>
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

        <!-- Mobile Number -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">Mobile Number</label>
          <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 text-gray-400"><Phone :size="14" /></span>
            <input 
              v-model="formData.mobileNumber"
              type="tel" 
              required
              placeholder="e.g. 9876543210"
              class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent"
            />
          </div>
        </div>

        <!-- Bio -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-gray-700 uppercase tracking-wide">Bio</label>
          <div class="flex border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 bg-gray-50/50 transition-all">
            <span class="pl-4 pt-3.5 text-gray-400"><BookOpen :size="14" /></span>
            <textarea 
              v-model="formData.bio"
              required
              placeholder="Tell us a bit about yourself and why you joined."
              rows="3"
              class="w-full px-1 py-1.5 outline-none text-gray-700 bg-transparent resize-none"
            ></textarea>
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
          {{ isSubmitting ? 'Saving Profile...' : 'Complete Registration' }}
        </button>

      </form>
    </div>
  </div>
</template>

<style scoped>
/* Remove standard select arrow to rely on clean styling if desired */
/* select { -webkit-appearance: none; -moz-appearance: none; appearance: none; } */
</style>
