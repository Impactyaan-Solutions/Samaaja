<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import {
  ClipboardCheck,
  Users,
  Medal,
  LifeBuoy,
  Globe
} from 'lucide-vue-next';

const { t, locale } = useI18n();

// Query param busts the browser/CDN cache whenever the logo image is
// replaced in place (same filename), so bump this after swapping the file.
const LOGO_VERSION = 2;

const logoSrc = computed(() => `${import.meta.env.BASE_URL}${t('landing.logo.src')}?v=${LOGO_VERSION}`);

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
    title: t('landing.features.getRecognised.title'),
    description: t('landing.features.getRecognised.description'),
    icon: Medal,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    title: t('landing.features.askForHelp.title'),
    description: t('landing.features.askForHelp.description'),
    icon: LifeBuoy,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  }
]);
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex justify-center px-">
    
    <div class="w-full max-w-md bg-white min-h-screen shadow-sm px-8 py-0 flex flex-col gap-0">
      
      <header class="relative flex items-center justify-center mt-6 mb-6">
        <img
          :src="logoSrc"
          :alt="t('landing.logo.alt')"
          class="h-16 w-auto"
        />
        <button class="absolute right-0 flex items-center gap-1 bg-slate-100 px-3 py-1.5 rounded-full text-xs font-bold text-slate-600 uppercase">
          <Globe :size="12" />
          {{ locale }}
        </button>
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
        <a href="/signup">
          <button class="w-full py-4 bg-blue-600 hover:bg-blue-700 transition-colors text-white font-bold rounded-xl shadow-md">
            {{ t('landing.signUp') }}
          </button>
        </a>
        <a href="/login">
          <button class="w-full py-4 bg-blue-50 hover:bg-blue-100 transition-colors text-blue-800 font-bold rounded-xl">
            {{ t('landing.login') }}
          </button>
        </a>
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