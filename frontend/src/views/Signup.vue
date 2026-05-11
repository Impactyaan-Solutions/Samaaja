<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { 
  ArrowLeftIcon, 
  CalendarIcon, 
  SearchIcon, 
  UserIcon 
} from 'lucide-vue-next';

// Import the service that works in your Login component
import { getGoogleSignInURL } from '@/services/api';

const router = useRouter();

// Form State
const fullName = ref('');
const dob = ref('');
const gender = ref('Male');
const role = ref('Volunteer');
const mobileNumber = ref('');

// Logic for Manual Signup
const handleSubmit = () => {
  if (!mobileNumber.value || !fullName.value) {
    alert("Please fill in the required fields.");
    return;
  }
  
  console.log('Registering user:', {
    name: fullName.value,
    dob: dob.value,
    gender: gender.value,
    role: role.value,
    mobile: mobileNumber.value
  });

  // Redirect to homepage after "registration"
  router.push('/homepage');
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
      <div class="flex items-center justify-between mt-4 mb-6">
        <button @click="goBack" class="p-2 hover:bg-gray-100 rounded-full transition-colors -ml-2">
          <ArrowLeftIcon class="w-5 h-5 text-gray-600" />
        </button>
        <h1 class="text-blue-600 font-bold text-xl tracking-tight">Samaaja</h1>
        <div class="w-5"></div> 
      </div>

      <div class="mb-3">
        <h2 class="text-3xl font-extrabold text-gray-900 mb-2">Sign Up</h2>
        <p class="text-gray-500 text-sm leading-relaxed">
          Join the community to start making a real impact in your local area.
        </p>
      </div>

      <!-- Signup Form -->
      <form @submit.prevent="handleSubmit" class="space-y-5">
        
        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Full Name</label>
          <div class="relative">
            <input 
              v-model="fullName"
              type="text" 
              placeholder="e.g. Rahul Poddar"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
            />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Date of Birth</label>
          <div class="relative">
            <input 
              v-model="dob"
              type="text" 
              placeholder="DD/MM/YYYY"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
            />
            <CalendarIcon class="w-5 h-5 text-gray-400 absolute right-4 top-1/2 -translate-y-1/2" />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Gender</label>
          <div class="grid grid-cols-3 gap-3">
            <button 
              type="button" 
              v-for="option in ['Female', 'Male', 'Other']" 
              :key="option"
              @click="gender = option"
              :class="[
                'py-3 rounded-xl border text-sm font-medium transition-all',
                gender === option 
                  ? 'bg-blue-600 border-blue-600 text-white shadow-md shadow-blue-100' 
                  : 'bg-gray-50 border-gray-100 text-gray-500 hover:bg-gray-100'
              ]"
            >
              {{option}}
            </button>
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Role</label>
          <select 
            v-model="role"
            class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none appearance-none bg-white text-gray-700"
          >
            <option>Volunteer</option>
            <option>Organizer</option>
            <option>Partner</option>
          </select>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">Mobile Number</label>
          <div class="relative flex items-center">
            <span class="absolute left-4 text-gray-500 font-medium">+91</span>
            <input 
              v-model="mobileNumber"
              type="tel" 
              placeholder="Mobile Number"
              class="w-full pl-14 pr-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none placeholder:text-gray-300"
            />
          </div>
        </div>

        <button 
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl transition-all shadow-lg shadow-blue-200 mt-4 active:scale-[0.98]"
        >
          Create Account
        </button>
      </form>

      <!-- Divider -->
      <div class="relative my-6">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <div class="relative flex justify-center text-xs uppercase">
          <span class="bg-white px-3 text-gray-400 font-bold tracking-wider">Or sign up with</span>
        </div>
      </div>

      <!-- Social Signup -->
      <div class="pb-8">
        <button 
          @click="loginWithGoogle"
          class="w-full flex items-center justify-center gap-3 border border-gray-200 py-3 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-gray-700"
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