<script setup>
import { ref } from 'vue';
import { 
  ArrowLeft, 
  Facebook 
} from 'lucide-vue-next';

// 

// Navigation Helper
const goBack = () => {
  // Check if router exists, otherwise fallback to browser history
  window.history.length > 1 ? window.history.back() : console.log('No history to go back');
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4 font-sans">
    <div class="bg-white w-full max-w-md rounded-2xl shadow-sm p-8 flex flex-col">
      
      <button 
        @click="goBack" 
        class="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 hover:bg-blue-100 transition-colors mb-6 -ml-2"
      >
        <ArrowLeft :size="20" />
      </button>

      <h2 class="text-blue-600 text-2xl font-bold mb-8 tracking-tight">Samaaja</h2>

      <h1 class="text-3xl font-extrabold text-gray-900 mb-2">Log In</h1>
      <p class="text-gray-500 text-sm leading-relaxed mb-8">
        Enter your mobile number to get a verification code and securely log in.
      </p>

      <div class="space-y-4">
        <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
          <span class="px-4 py-3 text-gray-900 font-semibold border-r border-gray-100 bg-gray-50/50">
            +91
          </span>
          <input 
            v-model="mobileNumber"
            type="tel" 
            placeholder="Mobile Number" 
            class="w-full px-4 py-3 outline-none text-gray-700 placeholder-gray-400 bg-transparent"
          />
        </div>
      <router-link to="/homepage">
        <button
          @click="handleSendOTP"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-xl transition-all active:scale-[0.98] shadow-md"
        >
      
          Send OTP
    </button>

    </router-link>
      </div>

      <div class="relative my-10 text-center">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <span class="relative px-4 bg-white text-[10px] font-bold text-gray-400 uppercase tracking-widest">
          OR CONTINUE WITH
        </span>
      </div>

      <div class="space-y-3">
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

        <button 
          @click="loginWithFacebook"
          class="w-full flex items-center justify-center gap-3 border border-gray-200 py-3 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-gray-700"
        >
          <Facebook :size="18" fill="currentColor" class="text-gray-700" />
          Facebook
        </button>
      </div>

      <p class="mt-auto pt-10 text-center text-[10px] text-gray-400 leading-relaxed px-4">
        By logging in, you agree to our 
        <a href="#" class="text-blue-600 font-semibold hover:underline">Terms of Service</a> and 
        <a href="#" class="text-blue-600 font-semibold hover:underline">Privacy Policy</a>.
      </p>

    </div>
  </div>
</template>

<style scoped>
/* Chrome, Safari, Edge, Opera - Remove arrows from number input */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox - Remove arrows from number input */
input[type=number] {
  -moz-appearance: textfield;
}
</style>