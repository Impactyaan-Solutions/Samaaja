<script setup>
import { ref, computed } from 'vue';
import { useRouter  } from 'vue-router';
import {
  ArrowLeftIcon,
  CalendarIcon,
  SearchIcon,
  UserIcon
} from 'lucide-vue-next';
import router from '../router';
import { createAccount } from '@/services/api';
// Import the service that works in your Login component
import { getGoogleSignInURL } from '@/services/api';

// const router = useRouter();

const formData = ref({
  'name': '',
  'gender': '',
  'bio': '',
  'category': '',
  'dob': '',
  'mobile_no': ''
});

const isSubmitting = ref(false);
const errorMessage = ref('');

const isFormValid = computed(() => {
  return formData.value.gender && 
         formData.value.bio && 
         formData.value.category && 
         formData.value.dob && 
         formData.value.mobile_no &&
         formData.value.name;
});

// Logic for Manual Signup
const handleSubmit = async () => {
  if (!isFormValid.value) {
    alert("Please fill in all the required fields.");
    return;
  }
  const data = {
    name: formData.value.name,  
    dob: formData.value.dob,
    gender: formData.value.gender,
    category: formData.value.category,
    mobile_no: formData.value.mobile_no,
    bio: formData.value.bio
  }
  isSubmitting.value = true;
  try{
    await createAccount(data)
    router.push('/login')
  } catch(err){
    errorMessage.value = err.message;
  } finally{
    isSubmitting.value = false;
  }
};

// Logic for Google Signup (Uses the same working logic as Login)
const loginWithGoogle = async () => {
  try {
    const url = await getGoogleSignInURL();
    window.location.href = url;
  } catch (error) {
    console.error("Google Auth Error:", error);
    alert(`Connection failed: ${error.message}`);
  }
};

const goBack = () => {
  router.back();
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex justify-center px-4 font-sans">
    
    <div class="bg-white w-full max-w-md min-h-screen shadow-sm px-8 py-0 flex flex-col">
      
      <!-- Header -->
      <div class="flex items-center justify-between mt-2 mb-2">
        <button @click="goBack" class="p-2 hover:bg-gray-100 rounded-full transition-colors -ml-2">
          <ArrowLeftIcon class="w-5 h-5 text-gray-600" />
        </button>
        <h1 class="text-blue-600 font-bold text-xl tracking-tight">Samaaja</h1>
        <div class="w-5"></div> 
      </div>

      <div class="mb-2">
        <h2 class="text-2xl font-extrabold text-gray-900 mb-1">Sign Up</h2>
        <p class="text-gray-500 text-xs leading-relaxed">
          Join the community to start making a real impact!
        </p>
      </div>
      <div v-if="errorMessage" class="mb-6 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>
      <!-- Signup Form -->
      <form @submit.prevent="handleSubmit" class="space-y-2">
        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Full Name <span class="text-red-500">*</span></label>
          <div class="relative">
            <input 
              v-model="formData.name"
              type="text" 
              maxlength="30"
              placeholder="e.g. Rahul Poddar"
              class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
            />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Date of Birth <span class="text-red-500">*</span></label>
          <div class="relative">
            <input 
              v-model="formData.dob"
              type="text" 
              placeholder="DD/MM/YYYY"
              onfocus="this.type='date'; this.showPicker()"
              onblur="if(!this.value) this.type='text'"
              @keydown.prevent
              class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300 cursor-pointer"
            />
            <CalendarIcon class="w-5 h-5 text-gray-400 absolute right-4 top-1/2 -translate-y-1/2" />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Gender <span class="text-red-500">*</span></label>
          <div class="grid grid-cols-3 gap-3">
            <button 
              type="button" 
              v-for="option in ['Female', 'Male', 'Other']" 
              :key="option"
              @click="formData.gender = option"
              :class="[
                'py-2 rounded-xl border text-sm font-medium transition-all',
                formData.gender === option 
                  ? 'bg-blue-600 border-blue-600 text-white shadow-md shadow-blue-100' 
                  : 'bg-gray-50 border-gray-100 text-gray-500 hover:bg-gray-100'
              ]"
            >
              {{option}}
            </button>
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Role <span class="text-red-500">*</span></label>
          <select 
            v-model="formData.category"
            class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none appearance-none bg-white text-gray-700"
          >
            <option>Citizen</option>
            <option>NGO Partner</option>
          </select>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Mobile Number <span class="text-red-500">*</span></label>
          <div class="relative flex items-center">
            <span class="absolute left-4 text-gray-500 font-medium">+91</span>
            <input 
              v-model="formData.mobile_no"
              type="tel" 
              maxlength="10"
              @input="formData.mobile_no = $event.target.value.replace(/[^0-9]/g, '')"
              placeholder="Mobile Number"
              class="w-full pl-14 pr-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none placeholder:text-gray-300"
            />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Bio <span class="text-red-500">*</span></label>
          <div class="relative">
            <textarea 
              v-model="formData.bio"
              rows="2"
              maxlength="100"
              placeholder="Short bio"
              class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300 resize-none"
            ></textarea>
          </div>
        </div>

        <button 
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-blue-200 mt-2 active:scale-[0.98]"
        >
          Create Account
        </button>
      </form>

      <!-- Divider -->
      <div class="relative my-4">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <div class="relative flex justify-center text-xs uppercase">
          <span class="bg-white px-3 text-gray-400 font-bold tracking-wider">Or sign up with</span>
        </div>
      </div>

      <!-- Social Signup -->
      <div class="pb-4">
        <button 
          @click="loginWithGoogle"
          class="w-full flex items-center justify-center gap-3 border border-gray-200 py-2 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-gray-700"
        >
          <svg width="18" height="18" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.66l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          Google
        </button>
      </div>

    </div>
  </div>
</template>

<style scoped>
select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236B7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.25em;
}
</style>