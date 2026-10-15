<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {
  ArrowLeft
} from 'lucide-vue-next';
import { getLoginOptions, loginUsingOtp, loginUsingPassword } from '@/services/api';

const { t } = useI18n();
const mobileNumber = ref('');
const password = ref('');
const otp = ref('');
const router = useRouter();
// Navigation Helper
const goBack = () => {
  window.history.length > 1 ? window.history.back() : console.log('No history to go back');
};
const USE_MOBILE_NUMBER_AUTH = import.meta.env.VITE_USE_MOBILE_NUMBER_AUTH === 'true';

// Phone + password is the default; OTP only shows if enabled in Samaaja
// Settings (set via the setup wizard), and replaces password entirely when
// it is - never both at once. Social buttons are whatever Social Login Key
// records are actually configured, empty list means none render at all.
const otpEnabled = ref(false);
const providers = ref([]);
const errorMessage = ref('');
const isSubmitting = ref(false);

onMounted(async () => {
  try {
    const options = await getLoginOptions();
    otpEnabled.value = !!options.otp_enabled;
    providers.value = options.providers || [];
  } catch (error) {
    console.error("Failed to load login options:", error);
  }
});

const handleSendOTP = () => {
  if (mobileNumber.value.length != 10) {
    alert(t('login.invalidMobile'))
    return
  }
  alert(t('login.otpSent'))
  // Show OTP field
  const otpField = document.querySelector('.hidden');
  otpField.classList.remove('hidden');
  // Show login button
  const loginBtn = document.getElementById('login-btn');
  loginBtn.classList.remove('hidden');
  // Change send otp button to verify otp
  const sendOtpBtn = document.getElementById('send-otp-btn');
  sendOtpBtn.classList.add('hidden');
}

const handleOtpLogin = async () => {
  try {
    if (otp.value.length != 4) {
      alert(t('login.invalidOtp'))
      return
    }
    const data = {
      mobile_no: mobileNumber.value,
      otp: otp.value
    }
    const result = await loginUsingOtp(data)
    if (result) {
      router.push('/homepage')
    }
  } catch (error) {
    console.error("Login Error:", error);
    alert(t('login.connectionFailed', { error: error.message }));
  }
}

const handlePasswordLogin = async () => {
  errorMessage.value = '';

  if (mobileNumber.value.length != 10) {
    errorMessage.value = t('login.invalidMobile')
    return
  }
  if (!password.value) {
    errorMessage.value = t('login.passwordRequired')
    return
  }

  isSubmitting.value = true;
  try {
    const data = {
      mobile_no: mobileNumber.value,
      password: password.value
    }
    const result = await loginUsingPassword(data)
    if (result) {
      router.push('/homepage')
    } else {
      errorMessage.value = t('login.loginFailed')
    }
  } catch (error) {
    console.error("Login Error:", error);
    errorMessage.value = t('login.loginFailed')
  } finally {
    isSubmitting.value = false;
  }
}

const loginWithProvider = (authUrl) => {
  window.location.href = authUrl;
};

</script>

<template>
  <div class="min-h-screen bg-gray-100 flex justify-center px-4 font-sans">

    <div class="bg-white w-full max-w-md min-h-screen shadow-sm px-8 py-0 flex flex-col">

      <!-- Header -->
      <div class="flex items-center justify-between mt-2 mb-2">
        <button @click="goBack" class="p-2 hover:bg-gray-100 rounded-full transition-colors -ml-2">
          <ArrowLeft class="w-5 h-5 text-gray-600" />
        </button>
        <h1 class="text-blue-600 font-bold text-xl tracking-tight">{{ t('landing.appName') }}</h1>
        <div class="w-5"></div>
      </div>

      <div class="mb-2">
        <h2 class="text-2xl font-extrabold text-gray-900 mb-1">{{ t('login.title') }}</h2>
        <p class="text-gray-500 text-xs leading-relaxed" v-if="USE_MOBILE_NUMBER_AUTH">
          {{ otpEnabled ? t('login.subtitle') : t('login.passwordSubtitle') }}
        </p>
      </div>

      <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>

      <!-- Phone + Password (default login method) -->
      <form @submit.prevent="handlePasswordLogin" class="space-y-4" v-if="USE_MOBILE_NUMBER_AUTH && !otpEnabled">
        <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
          <span class="px-4 py-3 text-gray-900 font-semibold border-r border-gray-100 bg-gray-50/50">
            +91
          </span>
          <input
            v-model="mobileNumber"
            type="tel"
            :placeholder="t('login.mobileNumberPlaceholder')"
            @input="mobileNumber = $event.target.value.replace(/[^0-9]/g, '')"
            maxlength="10"
            class="w-full px-4 py-3 outline-none text-gray-700 placeholder-gray-400 bg-transparent"
          />
        </div>

        <input
          v-model="password"
          type="password"
          :placeholder="t('login.passwordPlaceholder')"
          class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all placeholder-gray-400"
        />

        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold py-3.5 rounded-xl transition-all active:scale-[0.98] shadow-md"
        >
          {{ t('login.loginButton') }}
        </button>
      </form>

      <!-- Phone + OTP (only shown when enabled during setup) -->
      <div class="space-y-4" v-if="USE_MOBILE_NUMBER_AUTH && otpEnabled">
        <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
          <span class="px-4 py-3 text-gray-900 font-semibold border-r border-gray-100 bg-gray-50/50">
            +91
          </span>
          <input
            v-model="mobileNumber"
            type="tel"
            :placeholder="t('login.mobileNumberPlaceholder')"
            @input="mobileNumber = $event.target.value.replace(/[^0-9]/g, '')"
            maxlength="10"
            class="w-full px-4 py-3 outline-none text-gray-700 placeholder-gray-400 bg-transparent"
          />
        </div>

        <div class="space-y-1 hidden">
          <label class="block text-sm font-semibold text-gray-700">{{ t('login.otpLabel') }} <span class="text-red-500">*</span></label>
          <div class="relative">
            <input
              v-model="otp"
              type="text"
              maxlength="4"
              placeholder="1111"
              class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
            />
          </div>
        </div>

        <button
          @click="handleSendOTP"
          id="send-otp-btn"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-xl transition-all active:scale-[0.98] shadow-md"
        >
          {{ t('login.sendOtp') }}
        </button>

        <button
          id="login-btn"
          @click="handleOtpLogin"
          class="hidden w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-xl transition-all active:scale-[0.98] shadow-md"
        >
          {{ t('login.loginButton') }}
        </button>
      </div>

      <div class="relative my-10 text-center" v-if="USE_MOBILE_NUMBER_AUTH && providers.length">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <span class="relative px-4 bg-white text-[10px] font-bold text-gray-400 uppercase tracking-widest">
          {{ t('login.orContinueWith') }}
        </span>
      </div>

      <div class="relative my-4 text-center" v-if="!USE_MOBILE_NUMBER_AUTH && providers.length">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <span class="relative px-4 bg-white text-[10px] font-bold text-gray-400 uppercase tracking-widest">
          {{ t('login.ContinueWith') }}
        </span>
      </div>

      <!-- One button per configured Social Login Key - nothing renders if none are set up -->
      <div class="space-y-4" v-if="providers.length">
        <button
          v-for="provider in providers"
          :key="provider.name"
          @click="loginWithProvider(provider.auth_url)"
          class="w-full flex items-center justify-center gap-3 border border-gray-200 py-3 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-gray-700"
        >
          <img v-if="provider.icon" :src="provider.icon" class="w-[18px] h-[18px]" :alt="provider.provider_name" />
          {{ provider.provider_name }}
        </button>
      </div>

      <router-link
        :to="{ name: 'admin-login' }"
        class="mt-auto mb-2 text-center text-xs text-gray-400 hover:text-gray-600 hover:underline"
      >
        {{ t('login.adminLoginLink') }}
      </router-link>

      <p class="mb-6 text-center text-[10px] text-gray-400 leading-relaxed px-4">
        {{ t('login.agreementPrefix') }}
        <a href="#" class="text-blue-600 font-semibold hover:underline">{{ t('login.termsOfService') }}</a> {{ t('login.and') }}
        <a href="#" class="text-blue-600 font-semibold hover:underline">{{ t('login.privacyPolicy') }}</a>.
      </p>

    </div>
  </div>
</template>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type=number] {
  -moz-appearance: textfield;
}
</style>
