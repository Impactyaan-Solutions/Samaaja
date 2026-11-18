<script setup>
import { computed , ref} from 'vue';
import { useI18n } from 'vue-i18n';
import {
  ClipboardCheck,
  Users,
  Medal,
  LifeBuoy,
  Globe
} from 'lucide-vue-next';
import {getLoginOptions } from '@/services/api'
const { t, locale } = useI18n();

// Query param busts the browser/CDN cache whenever the logo image is
// replaced in place (same filename), so bump this after swapping the file.
const LOGO_VERSION = 2;

const logoSrc = computed(() => `${import.meta.env.BASE_URL}${t('landing.logo.src')}?v=${LOGO_VERSION}`);
const errorMessage = ref('');
const checkingLoginOptions = ref(false);
const showErrorPopup = ref(false);
const errorTitle = ref('');
const checkLoginAccess = async (route) => {
  errorMessage.value = '';
  showErrorPopup.value = false;
  checkingLoginOptions.value = true;

  try {
    const options = await getLoginOptions();

    const phoneLoginEnabled = !!options.otp_enabled;
    const emailLoginEnabled = options.email_login_enabled !== false;
    const providers = options.providers || [];

    const loginAvailable =
      phoneLoginEnabled ||
      emailLoginEnabled ||
      providers.length > 0;

    if (!loginAvailable) {
      errorTitle.value = t('landing.loginUnavailable.title');
      errorMessage.value = t('landing.loginUnavailable.message');
      showErrorPopup.value = true;
      return;
    }

    window.location.href = route;

  } catch (error) {
    console.error('Failed to check login options:', error);

    errorTitle.value = t('landing.loginCheckFailed.title');
    errorMessage.value = t('landing.loginCheckFailed.message');
    showErrorPopup.value = true;

  } finally {
    checkingLoginOptions.value = false;
  }
};
const features = computed(() => [
  {
    title: t('landing.features.reportAct.title'),
    description: t('landing.features.reportAct.description'),
    icon: ClipboardCheck,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    title: t('landing.features.connect.title'),
    description: t('landing.features.connect.description'),
    icon: Users,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    title: t('landing.features.askForHelp.title'),
    description: t('landing.features.askForHelp.description'),
    icon: Medal,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    title: t('landing.features.getRecognised.title'),
    description: t('landing.features.getRecognised.description'),
    icon: LifeBuoy,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  }
]);
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex justify-center px-">
    
    <div class="w-full max-w-md bg-white min-h-screen shadow-sm px-8 py-0 flex flex-col gap-0">
      
      <header class="flex items-center justify-between mt-6 mb-6">
        <img
          :src="logoSrc"
          :alt="t('landing.logo.alt')"
          class="h-16 w-auto"
        />
       
      </header>

      <section class="space-y-1.5 mt-4 mb-8">
        <h4 class="text-3xl font-extrabold text-slate-900 leading-snug">
          {{ t('landing.tagline1') }}
        </h4>
        <h4 class="text-3xl font-extrabold text-slate-900 leading-snug">
          {{ t('landing.tagline2') }}
        </h4>
        <h4 class="text-3xl font-extrabold text-slate-900 leading-snug">
          {{ t('landing.tagline3') }}
        </h4>
      </section>

     
<section class="flex flex-col gap-3 mb-6">

  <button
    type="button"
    @click="checkLoginAccess('/signup')"
    :disabled="checkingLoginOptions"
    class="w-full py-4 bg-blue-600 hover:bg-blue-700 transition-colors text-white font-bold rounded-xl shadow-md"
  >
    {{ t('landing.signUp') }}
  </button>

  <button
    type="button"
    @click="checkLoginAccess('/login')"
    :disabled="checkingLoginOptions"
    class="w-full py-4 bg-blue-50 hover:bg-blue-100 transition-colors text-blue-800 font-bold rounded-xl"
  >
    {{ t('landing.login') }}
  </button>

 <!-- Login Error Popup -->
<div
  v-if="showErrorPopup"
  class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-6"
  @click.self="showErrorPopup = false"
>
  <div class="w-full max-w-sm bg-white rounded-2xl p-6 shadow-xl text-center">

    <div class="mx-auto mb-4 w-14 h-14 rounded-full bg-red-100 flex items-center justify-center">
      <span class="text-red-600 text-2xl font-bold">!</span>
    </div>

    <h3 class="text-xl font-bold text-slate-900 mb-2">
      {{ errorTitle }}
    </h3>

    <p class="text-sm text-slate-600 leading-relaxed mb-6">
      {{ errorMessage }}
    </p>
    <a
  :href="t('landing.loginUnavailable.linkUrl')"
  target="_blank"
  rel="noopener noreferrer"
  class="text-blue-600 hover:text-blue-800 underline text-sm font-semibold mb-6 inline-block"
>
  {{ t('landing.loginUnavailable.linkText') }}
</a>
    <button
      type="button"
      @click="showErrorPopup = false"
      class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-colors"
    >
      {{ t('landing.loginUnavailable.button') }}
    </button>

  </div>
</div>

</section>


      <section class="pb-8">
        <h3 class="text-xs font-black text-slate-400 tracking-widest uppercase mb-6">
          {{ t('landing.whatYouCanDo') }}
        </h3>

        <div class="space-y-5">
          <div v-for="feature in features" :key="feature.title" class="flex gap-4">
            <div :class="[feature.iconBg, 'w-12 h-12 flex-shrink-0 rounded-full flex items-center justify-center']">
              <component :is="feature.icon" :class="feature.iconColor" :size="24" />
            </div>
            
            <div class="space-y-1">
              <h4 class="font-bold text-slate-900 text-lg leading-tight">{{ feature.title }}</h4>
              <p class="text-slate-500 leading-snug">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<style scoped>
div {
  font-family: 'Inter', sans-serif;
}
</style>