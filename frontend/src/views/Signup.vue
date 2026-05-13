<script setup>
import { ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { createAccount } from '@/services/api';
import { getGoogleSignInURL } from '@/services/api';
import { ArrowLeftIcon, CalendarIcon, UserIcon } from 'lucide-vue-next';

const { t } = useI18n();
const router = useRouter();

const formData = ref({
  name: '', gender: '', bio: '', category: '', dob: '', mobile_no: ''
});

const isSubmitting = ref(false);
const errorMessage = ref('');

// Reactive options for dropdowns and buttons
const genderOptions = computed(() => [
  { label: t('signup.female'), value: 'Female' },
  { label: t('signup.male'), value: 'Male' },
  { label: t('signup.other'), value: 'Other' }
]);

const roleOptions = computed(() => [
  { label: t('signup.role_volunteer'), value: 'Volunteer' },
  { label: t('signup.role_organizer'), value: 'Organizer' },
  { label: t('signup.role_partner'), value: 'Partner' }
]);

const isFormValid = computed(() => {
  return formData.value.gender && formData.value.bio && formData.value.category && 
         formData.value.dob && formData.value.mobile_no && formData.value.name;
});

const handleSubmit = async () => {
  if (!isFormValid.value) return;
  
  isSubmitting.value = true;
  try {
    await createAccount(formData.value)
    router.push('/login')
  } catch(err){
    errorMessage.value = err.message;
  } finally {
    isSubmitting.value = false;
  }
};

const loginWithGoogle = async () => {
  try {
    const url = await getGoogleSignInURL();
    window.location.href = url;
  } catch (error) {
    alert(`Connection failed: ${error.message}`);
  }
};

const goBack = () => router.back();
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex justify-center px-4 font-sans">
    <div class="bg-white w-full max-w-md min-h-screen shadow-sm px-8 py-0 flex flex-col">
      
      <div class="flex items-center justify-between mt-2 mb-2">
        <button @click="goBack" class="p-2 hover:bg-gray-100 rounded-full transition-colors -ml-2">
          <ArrowLeftIcon class="w-5 h-5 text-gray-600" />
        </button>
        <h1 class="text-blue-600 font-bold text-xl tracking-tight">Samaaja</h1>
        <div class="w-5"></div> 
      </div>

      <div class="mb-2">
        <h2 class="text-2xl font-extrabold text-gray-900 mb-1">{{ t('signup.title') }}</h2>
        <p class="text-gray-500 text-xs leading-relaxed">{{ t('signup.subtitle') }}</p>
      </div>
      <div v-if="errorMessage" class="mb-6 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-2">
        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.full_name') }} <span class="text-red-500">*</span></label>
          <input v-model="formData.name" type="text" maxlength="30" :placeholder="t('signup.name_placeholder')" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300" />
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.dob') }} <span class="text-red-500">*</span></label>
          <div class="relative">
            <input v-model="formData.dob" type="text" :placeholder="t('signup.dob_placeholder')" onfocus="this.type='date'; this.showPicker()" onblur="if(!this.value) this.type='text'" @keydown.prevent class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300 cursor-pointer" />
            <CalendarIcon class="w-5 h-5 text-gray-400 absolute right-4 top-1/2 -translate-y-1/2" />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.gender') }} <span class="text-red-500">*</span></label>
          <div class="grid grid-cols-3 gap-3">
            <button 
              type="button" 
              v-for="option in genderOptions" :key="option.value"
              @click="formData.gender = option.value"
              :class="['py-2 rounded-xl border text-sm font-medium transition-all', formData.gender === option.value ? 'bg-blue-600 border-blue-600 text-white shadow-md' : 'bg-gray-50 border-gray-100 text-gray-500 hover:bg-gray-100']"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.role') }} <span class="text-red-500">*</span></label>
          <select v-model="formData.category" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none appearance-none bg-white text-gray-700">
            <option value="" disabled>{{ t('signup.role_select') }}</option>
            <option v-for="role in roleOptions" :key="role.value" :value="role.value">{{ role.label }}</option>
          </select>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.mobile') }} <span class="text-red-500">*</span></label>
          <div class="relative flex items-center">
            <span class="absolute left-4 text-gray-500 font-medium">+91</span>
            <input v-model="formData.mobile_no" type="tel" maxlength="10" @input="formData.mobile_no = $event.target.value.replace(/[^0-9]/g, '')" :placeholder="t('signup.mobile_placeholder')" class="w-full pl-14 pr-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none placeholder:text-gray-300" />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.bio') }} <span class="text-red-500">*</span></label>
          <textarea v-model="formData.bio" rows="2" maxlength="100" :placeholder="t('signup.bio_placeholder')" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300 resize-none"></textarea>
        </div>

        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-blue-200 mt-2 active:scale-[0.98]">
          {{ t('signup.create_account') }}
        </button>
      </form>

      <div class="relative my-4">
        <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-gray-100"></div></div>
        <div class="relative flex justify-center text-xs uppercase"><span class="bg-white px-3 text-gray-400 font-bold tracking-wider">{{ t('signup.or_signup') }}</span></div>
      </div>

      <div class="pb-4">
        <button @click="loginWithGoogle" class="w-full flex items-center justify-center gap-3 border border-gray-200 py-2 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-gray-700">
          Google
        </button>
      </div>
    </div>
  </div>
</template>