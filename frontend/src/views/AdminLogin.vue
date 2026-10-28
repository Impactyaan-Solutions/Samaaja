<script setup>
import { ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { ArrowLeft } from 'lucide-vue-next';
import { loginWithUsernamePassword } from '@/services/api';
import { brandingState } from '@/branding';

const { t } = useI18n();
const appName = computed(() => brandingState.appName || t('landing.appName'));
const username = ref('');
const password = ref('');
const isSubmitting = ref(false);
const errorMessage = ref('');

const goBack = () => {
  window.history.length > 1 ? window.history.back() : console.log('No history to go back');
};

const handleLogin = async () => {
  errorMessage.value = '';

  if (!username.value || !password.value) {
    errorMessage.value = t('adminLogin.missingFields');
    return;
  }

  isSubmitting.value = true;
  try {
    await loginWithUsernamePassword(username.value, password.value);
    // A plain navigation, not a router push - /desk is the platform's own
    // server-rendered admin app, outside the Vue SPA entirely.
    window.location.href = '/desk';
  } catch (error) {
    errorMessage.value = t('adminLogin.invalidCredentials');
  } finally {
    isSubmitting.value = false;
  }
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
        <h1 class="text-[var(--brand-primary)] font-bold text-xl tracking-tight">{{ appName }}</h1>
        <div class="w-5"></div>
      </div>

      <div class="mb-6">
        <h2 class="text-2xl font-extrabold text-gray-900 mb-1">{{ t('adminLogin.title') }}</h2>
        <p class="text-gray-500 text-xs leading-relaxed">{{ t('adminLogin.subtitle') }}</p>
      </div>

      <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <input
          v-model="username"
          type="text"
          autocomplete="username"
          :placeholder="t('adminLogin.usernamePlaceholder')"
          class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all placeholder-gray-400"
        />
        <input
          v-model="password"
          type="password"
          autocomplete="current-password"
          :placeholder="t('adminLogin.passwordPlaceholder')"
          class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all placeholder-gray-400"
        />

        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full bg-[var(--brand-primary)] hover:bg-[var(--brand-accent)] disabled:opacity-60 text-white font-semibold py-3.5 rounded-xl transition-all active:scale-[0.98] shadow-md"
        >
          {{ isSubmitting ? t('adminLogin.loggingIn') : t('adminLogin.loginButton') }}
        </button>
      </form>

      <router-link
        :to="{ name: 'login' }"
        class="mt-auto mb-6 text-center text-xs text-gray-400 hover:text-gray-600 hover:underline"
      >
        {{ t('adminLogin.backToLogin') }}
      </router-link>

    </div>
  </div>
</template>
