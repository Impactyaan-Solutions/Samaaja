<script setup>
import { ref, onMounted } from 'vue';
import { useRouter , useRoute  } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {
  ArrowLeft
} from 'lucide-vue-next';
import { getLoginOptions, loginUsingOtp , loginUsingEmailOtp  } from '@/services/api';

const { t } = useI18n();
const logoSrc = `${import.meta.env.BASE_URL}${t('landing.logo.src')}?v=2`;
const mobileNumber = ref('')
const email = ref('');
const phoneOtp = ref('');
const emailOtp = ref('');
const router = useRouter();
const route = useRoute();

// UI state
const showPhoneOtpField = ref(false);
const showEmailOtpField = ref(false);

// Navigation Helper
const goBack = () => {
  window.history.length > 1 ? window.history.back() : console.log('No history to go back');
};

// Default true so the form doesn't flash/hide while options load.
const phoneLoginEnabled = ref(true);
const emailLoginEnabled = ref(false);
const otpEnabled = ref(false);
const providers = ref([]);
const errorMessage = ref('');
const isSubmitting = ref(false);

onMounted(async () => {
  try {
    const options = await getLoginOptions();
    phoneLoginEnabled.value = !!options.otp_enabled;
    emailLoginEnabled.value = options.email_login_enabled !== false;
    otpEnabled.value = !!options.otp_enabled;
    providers.value = options.providers || [];
     if (phoneLoginEnabled.value && otpEnabled.value) {
      loginMethod.value = 'phone';
    } else if (emailLoginEnabled.value) {
      loginMethod.value = 'email';
    }

  } catch (error) {
    console.error("Failed to load login options:", error);
    errorMessage.value = t('login.loadOptionsFailed');
  }
});

// Phone OTP Handlers
const handleSendPhoneOTP = () => {
  errorMessage.value = '';
  if (mobileNumber.value.length != 10) {
    errorMessage.value = t('login.invalidMobile');
    return;
  }
  alert(t('login.otpSent'));
  showPhoneOtpField.value = true;
}

const handlePhoneOtpLogin = async () => {
  errorMessage.value = '';
  try {
    if (phoneOtp.value.length != 4) {
      errorMessage.value = t('login.invalidOtp');
      return;
    }
    const data = {
      mobile_no: mobileNumber.value,
      otp: phoneOtp.value
    }
    const result = await loginUsingOtp(data);
    if (result) {
      redirectAfterLogin();
    }
  } catch (error) {
    console.error("Login Error:", error);
    errorMessage.value = t('login.connectionFailed', { error: error.message });
  }
}

// Email OTP Handlers
const handleSendEmailOTP = () => {
  errorMessage.value = '';
  if (!email.value || !email.value.includes('@')) {
    errorMessage.value = t('login.invalidEmail');
    return;
  }
  alert(t('login.emailOtpSent'));
  showEmailOtpField.value = true;
}
const loginMethod = ref('phone');
const handleEmailOtpLogin = async () => {
  errorMessage.value = '';
  try {
    if (emailOtp.value.length != 4) {
      errorMessage.value = t('login.invalidOtp');
      return;
    }
    const data = {
      email: email.value,
      otp: emailOtp.value
    }
    const result = await loginUsingEmailOtp(data);
    if (result) {
      redirectAfterLogin();
    }
  } catch (error) {
    console.error("Login Error:", error);
    errorMessage.value = t('login.connectionFailed', { error: error.message });
  }
}

const loginWithProvider = (authUrl) => {
  window.location.href = authUrl;
};

const redirectAfterLogin = () => {
  const redirect = route.query.redirect;

  if (
    typeof redirect === 'string' &&
    redirect.startsWith('/') &&
    !redirect.startsWith('//')
  ) {
    router.replace(redirect);
  } else {
    router.replace({ name: 'home' });
  }
};
const switchLoginMethod = (method) => {
  loginMethod.value = method;
  errorMessage.value = '';

  // Reset OTP fields when switching methods
  showPhoneOtpField.value = false;
  showEmailOtpField.value = false;

  phoneOtp.value = '';
  emailOtp.value = '';
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
        <img :src="logoSrc" :alt="t('landing.logo.alt')" class="h-9 w-auto" />
        <div class="w-5"></div>
      </div>

      <div class="mb-2">
        <h2 class="text-2xl font-extrabold text-gray-900 mb-1">{{ t('login.title') }}</h2>
        <p class="text-gray-500 text-xs leading-relaxed" v-if="phoneLoginEnabled || emailLoginEnabled">
          {{ t('login.subtitle') }}
        </p>
      </div>

      <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>

     <!-- Login Method Toggle -->
<div
  v-if="phoneLoginEnabled && otpEnabled && emailLoginEnabled"
  class="flex bg-gray-100 rounded-xl p-1 mb-6"
>
  <button
    @click="switchLoginMethod('phone')"
    :class="loginMethod === 'phone'
      ? 'bg-blue-600 text-white shadow-sm'
      : 'text-gray-600 hover:bg-gray-200'"
    class="flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all"
  >
    Phone
  </button>

  <button
    @click="switchLoginMethod('email')"
    :class="loginMethod === 'email'
      ? 'bg-blue-600 text-white shadow-sm'
      : 'text-gray-600 hover:bg-gray-200'"
    class="flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all"
  >
    Email
  </button>
</div>

<!-- Phone Login -->
<div
  v-if="loginMethod === 'phone' && phoneLoginEnabled && otpEnabled"
  class="space-y-4 mb-6"
>
  <h3 class="text-sm font-semibold text-gray-700">
    {{ t('login.phoneLoginTitle') }}
  </h3>

  <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden">
    <span class="px-4 py-3 text-gray-900 font-semibold border-r border-gray-100 bg-gray-50">
      +91
    </span>

    <input
      v-model="mobileNumber"
      type="tel"
      :placeholder="t('login.mobileNumberPlaceholder')"
      @input="mobileNumber = $event.target.value.replace(/[^0-9]/g, '')"
      maxlength="10"
      class="w-full px-4 py-3 outline-none text-gray-700 bg-transparent"
    />
  </div>

  <div v-if="showPhoneOtpField" class="space-y-1">
    <label class="block text-sm font-semibold text-gray-700">
      {{ t('login.otpLabel') }}
    </label>

    <input
      v-model="phoneOtp"
      type="text"
      maxlength="4"
      placeholder="1111"
      class="w-full px-4 py-2 rounded-xl border border-gray-200 outline-none"
    />
  </div>

  <button
    v-if="!showPhoneOtpField"
    @click="handleSendPhoneOTP"
    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-xl"
  >
    {{ t('login.sendOtp') }}
  </button>

  <button
    v-else
    @click="handlePhoneOtpLogin"
    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-xl"
  >
    {{ t('login.loginButton') }}
  </button>
</div>

<!-- Email Login -->
<div
  v-if="loginMethod === 'email' && emailLoginEnabled"
  class="space-y-4 mb-6"
>
  <h3 class="text-sm font-semibold text-gray-700">
    {{ t('login.emailLoginTitle') }}
  </h3>

  <input
    v-model="email"
    type="email"
    :placeholder="t('login.emailPlaceholder')"
    class="w-full px-4 py-3 rounded-xl border border-gray-200 outline-none"
  />

  <div v-if="showEmailOtpField" class="space-y-1">
    <label class="block text-sm font-semibold text-gray-700">
      {{ t('login.emailOtpLabel') }}
    </label>

    <input
      v-model="emailOtp"
      type="text"
      maxlength="4"
      placeholder="1111"
      class="w-full px-4 py-2 rounded-xl border border-gray-200 outline-none"
    />
  </div>

  <button
    v-if="!showEmailOtpField"
    @click="handleSendEmailOTP"
    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-xl"
  >
    {{ t('login.sendEmailOtp') }}
  </button>

  <button
    v-else
    @click="handleEmailOtpLogin"
    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-xl"
  >
    {{ t('login.loginButton') }}
  </button>
</div>
      <div class="relative my-10 text-center" v-if="providers.length">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <span class="relative px-4 bg-white text-[10px] font-bold text-gray-400 uppercase tracking-widest">
          {{ (phoneLoginEnabled || emailLoginEnabled) ? t('login.orContinueWith') : t('login.ContinueWith') }}
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
      <router-link
        :to="{ name: 'signup', query: route.query.redirect ? { redirect: route.query.redirect } : {} }"
        class="mb-4 text-center text-sm text-gray-600"
      >
        Don't have an account?
        <span class="font-semibold text-blue-600 hover:underline">
          Sign up
        </span>
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
