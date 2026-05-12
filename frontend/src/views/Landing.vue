<script setup>
import { 
  ClipboardCheck, 
  Users, 
  Medal, 
  LifeBuoy, 
  Globe 
} from 'lucide-vue-next';

const features = [
  {
    title: 'Report & Act',
    description: 'Raise local problems and track progress.',
    icon: ClipboardCheck,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    title: 'Connect',
    description: 'Post or join community discussions.',
    icon: Users,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    title: 'Get Recognised',
    description: 'See your impact and leaderboard rank.',
    icon: Medal,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    title: 'Ask for Help',
    description: 'Get support from experts and community.',
    icon: LifeBuoy,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  }
];
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex justify-center px-">
    
    <div class="w-full max-w-md bg-white min-h-screen shadow-sm px-8 py-0 flex flex-col gap-0">
      
      <header class="flex justify-between items-center mt-4 mb-2">
        <div class="flex items-center gap-2">
          <img src="/samaaja.png" alt="Samaaja" class="w-12 h-12" />
          <h1 class="text-2xl font-black text-blue-600">Samaaja</h1>
        </div>
        <button class="flex items-center gap-1 bg-slate-100 px-3 py-1.5 rounded-full text-xs font-bold text-slate-600 uppercase">
          <Globe :size="12" />
          EN
        </button>
      </header>

      <section class="space-y-2 mb-2">
        <h2 class="text-4xl font-extrabold text-slate-900 leading-tight">
          Build Your Community. Take Action.
        </h2>
        <p class="text-slate-500 text-lg leading-relaxed">
          Join people in your area solving real issues and improving their community together.
        </p>
      </section>

      <section class="flex flex-col gap-3 mb-6">
        <a href="/signup">
          <button class="w-full py-4 bg-blue-600 hover:bg-blue-700 transition-colors text-white font-bold rounded-xl shadow-md">
            Sign Up
          </button>
        </a>
        <a href="/login">
          <button class="w-full py-4 bg-blue-50 hover:bg-blue-100 transition-colors text-blue-800 font-bold rounded-xl">
            Login
          </button>
        </a>
      </section>

      <section class="pb-8">
        <h3 class="text-xs font-black text-slate-400 tracking-widest uppercase mb-6">
          What you can do
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