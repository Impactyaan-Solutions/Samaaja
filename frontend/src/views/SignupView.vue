<template>
  <div class="min-h-full flex items-center justify-center p-4 py-8">
    <div class="bg-white w-full rounded-3xl shadow-sm border border-gray-100 p-8">
      
      <div class="flex items-center justify-between mb-8">
        <button @click="$router.back()" class="p-2 hover:bg-gray-100 rounded-full transition-colors -ml-2">
          <ArrowLeftIcon class="w-5 h-5 text-gray-600" />
        </button>
        <h1 class="text-blue-600 font-bold text-xl tracking-tight">Samaaja</h1>
        <div class="w-5"></div> 
      </div>

      <div class="mb-6">
        <h2 class="text-3xl font-extrabold text-gray-900 mb-2">Sign Up</h2>
        <p class="text-gray-500 text-sm leading-relaxed">
          Join the community to start making a real impact in your local area.
        </p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-5">
        
        <div class="space-y-1.5">
          <label class="block text-sm font-semibold text-gray-700">Full Name</label>
          <input 
            type="text" 
            placeholder="e.g. Rahul Poddar"
            class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
          />
        </div>

        <div class="space-y-1.5">
          <label class="block text-sm font-semibold text-gray-700">Date of Birth</label>
          <div class="relative">
            <input 
              type="text" 
              placeholder="DD/MM/YYYY"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
            />
            <CalendarIcon class="w-5 h-5 text-gray-400 absolute right-4 top-1/2 -translate-y-1/2" />
          </div>
        </div>

        <div class="space-y-1.5">
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

        <div class="space-y-1.5">
          <label class="block text-sm font-semibold text-gray-700">Role</label>
          <select class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none appearance-none bg-white text-gray-700">
            <option>Volunteer</option>
            <option>Organizer</option>
            <option>Partner</option>
          </select>
        </div>

        <div class="space-y-1.5">
          <label class="block text-sm font-semibold text-gray-700">Location</label>
          <div class="relative flex items-center">
            <SearchIcon class="w-4 h-4 text-gray-400 absolute left-4" />
            <input 
              type="text" 
              placeholder="Search city or area..."
              class="w-full pl-10 pr-24 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none placeholder:text-gray-300"
            />
            <button type="button" class="absolute right-4 text-sm font-bold text-blue-600 hover:text-blue-700">
              Auto-fetch
            </button>
          </div>
        </div>

    <router-link to="/homepage">
      <button class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl transition-all shadow-lg shadow-blue-200 mt-4 active:scale-[0.98]">
        Create Account
      </button>
    </router-link>
      </form>

      <div class="relative my-8">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <div class="relative flex justify-center text-xs uppercase">
          <span class="bg-white px-3 text-gray-400">Or sign up with</span>
        </div>
      </div>

      <div class="space-y-3">
        <button class="w-full flex items-center justify-center gap-3 border border-gray-200 py-3.5 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-gray-700">
          <GlobeIcon class="w-5 h-5" />
          Continue with Google
        </button>
        <button class="w-full flex items-center justify-center gap-3 border border-gray-200 py-3.5 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-gray-700">
          <FacebookIcon class="w-5 h-5 text-blue-600" />
          Continue with Facebook
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { 
  ArrowLeftIcon, 
  CalendarIcon, 
  SearchIcon, 
  GlobeIcon, 
  FacebookIcon 
} from 'lucide-vue-next';

const gender = ref('Male');

const handleSubmit = () => {
  console.log('Form submitted');
};
</script>

<style scoped>

select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236B7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.25em;
}
div {
  font-family: 'Inter', sans-serif;
}
</style>