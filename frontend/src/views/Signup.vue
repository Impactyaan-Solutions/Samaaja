<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter  } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {
  ArrowLeftIcon,
  CalendarIcon,
  SearchIcon,
  UserIcon
} from 'lucide-vue-next';
import router from '../router';
import { createAccount, getLoginOptions } from '@/services/api';

// const router = useRouter();
const { t } = useI18n();

const genderOptions = computed(() => [
  { value: 'Female', label: t('signup.genderFemale') },
  { value: 'Male', label: t('signup.genderMale') },
  { value: 'Other', label: t('signup.genderOther') }
]);

const USE_MOBILE_NUMBER_AUTH = import.meta.env.VITE_USE_MOBILE_NUMBER_AUTH === 'true';

const formData = ref({
  'name': '',
  'gender': '',
  'bio': '',
  'category': '',
  'dob': '',
  'mobile_no': '',
  'password': '',
  'confirmPassword': ''
});

const isSubmitting = ref(false);
const errorMessage = ref('');
const providers = ref([]);

onMounted(async () => {
  try {
    const options = await getLoginOptions();
    providers.value = options.providers || [];
  } catch (error) {
    console.error("Failed to load login options:", error);
  }
});

const isFormValid = computed(() => {
  return formData.value.gender &&
         formData.value.bio &&
         formData.value.category &&
         formData.value.dob &&
         formData.value.mobile_no &&
         formData.value.name &&
         formData.value.password &&
         formData.value.password === formData.value.confirmPassword;
});

// Logic for Manual Signup
const handleSubmit = async () => {
  if (!formData.value.password) {
    errorMessage.value = t('signup.passwordRequired');
    return;
  }
  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = t('signup.passwordMismatch');
    return;
  }
  if (!isFormValid.value) {
    alert(t('signup.fillRequiredFields'));
    return;
  }
  errorMessage.value = '';
  const data = {
    name: formData.value.name,
    dob: formData.value.dob,
    gender: formData.value.gender,
    category: formData.value.category,
    mobile_no: formData.value.mobile_no,
    bio: formData.value.bio,
    password: formData.value.password
  }
  isSubmitting.value = true;
  try{
    await createAccount(data)
    router.push('/login')
  } catch(err){
    errorMessage.value = err.message;
  } finally{
    isSubmitting.value = false;
  }
};

// One button per configured Social Login Key, same as Login.vue
const signupWithProvider = (authUrl) => {
  window.location.href = authUrl;
};

const goBack = () => {
  router.back();
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex justify-center px-4 font-sans">
    
    <div class="bg-white w-full max-w-md min-h-screen shadow-sm px-8 py-0 flex flex-col">
      
      <!-- Header -->
      <div class="flex items-center justify-between mt-2 mb-2">
        <button @click="goBack" class="p-2 hover:bg-gray-100 rounded-full transition-colors -ml-2">
          <ArrowLeftIcon class="w-5 h-5 text-gray-600" />
        </button>
        <h1 class="text-blue-600 font-bold text-xl tracking-tight">{{ t('landing.appName') }}</h1>
        <div class="w-5"></div> 
      </div>

      <div class="mb-2">
        <h2 class="text-2xl font-extrabold text-gray-900 mb-1">{{ t('signup.title') }}</h2>
        <p class="text-gray-500 text-xs leading-relaxed">
          {{ t('signup.subtitle') }}
        </p>
      </div>
      <div v-if="errorMessage" class="mb-6 p-3 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
        {{ errorMessage }}
      </div>
      <!-- Signup Form -->
      <form @submit.prevent="handleSubmit" class="space-y-2" v-if="USE_MOBILE_NUMBER_AUTH">
        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.fullName') }} <span class="text-red-500">*</span></label>
          <div class="relative">
            <input
              v-model="formData.name"
              type="text"
              maxlength="30"
              :placeholder="t('signup.fullNamePlaceholder')"
              class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
            />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.dob') }} <span class="text-red-500">*</span></label>
          <div class="relative">
            <input
              v-model="formData.dob"
              type="text"
              :placeholder="t('signup.dobPlaceholder')"
              onfocus="this.type='date'; this.showPicker()"
              onblur="if(!this.value) this.type='text'"
              @keydown.prevent
              class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300 cursor-pointer"
            />
            <CalendarIcon class="w-5 h-5 text-gray-400 absolute right-4 top-1/2 -translate-y-1/2" />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.gender') }} <span class="text-red-500">*</span></label>
          <div class="grid grid-cols-3 gap-3">
            <button
              type="button"
              v-for="option in genderOptions"
              :key="option.value"
              @click="formData.gender = option.value"
              :class="[
                'py-2 rounded-xl border text-sm font-medium transition-all',
                formData.gender === option.value
                  ? 'bg-blue-600 border-blue-600 text-white shadow-md shadow-blue-100'
                  : 'bg-gray-50 border-gray-100 text-gray-500 hover:bg-gray-100'
              ]"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.role') }} <span class="text-red-500">*</span></label>
          <select
            v-model="formData.category"
            class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none appearance-none bg-white text-gray-700"
          >
            <option value="Citizen">{{ t('signup.roleCitizen') }}</option>
            <option value="NGO Partner">{{ t('signup.roleNgoPartner') }}</option>
          </select>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.mobileNumber') }} <span class="text-red-500">*</span></label>
          <div class="relative flex items-center">
            <span class="absolute left-4 text-gray-500 font-medium">+91</span>
            <input
              v-model="formData.mobile_no"
              type="tel"
              maxlength="10"
              @input="formData.mobile_no = $event.target.value.replace(/[^0-9]/g, '')"
              :placeholder="t('signup.mobileNumber')"
              class="w-full pl-14 pr-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none placeholder:text-gray-300"
            />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.bio') }} <span class="text-red-500">*</span></label>
          <div class="relative">
            <textarea
              v-model="formData.bio"
              rows="2"
              maxlength="100"
              :placeholder="t('signup.bioPlaceholder')"
              class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300 resize-none"
            ></textarea>
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.password') }} <span class="text-red-500">*</span></label>
          <input
            v-model="formData.password"
            type="password"
            :placeholder="t('signup.passwordPlaceholder')"
            class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
          />
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-gray-700">{{ t('signup.confirmPassword') }} <span class="text-red-500">*</span></label>
          <input
            v-model="formData.confirmPassword"
            type="password"
            :placeholder="t('signup.confirmPasswordPlaceholder')"
            class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-300"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-blue-200 mt-2 active:scale-[0.98]"
        >
          {{ t('signup.createAccount') }}
        </button>
      </form>

      <!-- Divider -->
      <div class="relative my-4" v-if="USE_MOBILE_NUMBER_AUTH && providers.length">
        <div class="absolute inset-0 flex items-center" >
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <div class="relative flex justify-center text-xs uppercase">
          <span class="bg-white px-3 text-gray-400 font-bold tracking-wider">{{ t('signup.orSignUpWith') }}</span>
        </div>
      </div>
      <div class="relative my-4" v-if="!USE_MOBILE_NUMBER_AUTH && providers.length">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-100"></div>
        </div>
        <div class="relative flex justify-center text-xs uppercase">
          <span class="bg-white px-3 text-gray-400 font-bold tracking-wider">{{ t('signup.SignUpWith') }}</span>
        </div>
      </div>
      <!-- One button per configured Social Login Key - nothing renders if none are set up -->
      <div class="pb-4 space-y-4" v-if="providers.length">
        <button
          v-for="provider in providers"
          :key="provider.name"
          @click="signupWithProvider(provider.auth_url)"
          class="w-full flex items-center justify-center gap-3 border border-gray-200 py-2 rounded-xl hover:bg-gray-50 transition-colors font-semibold text-gray-700"
        >
          <img v-if="provider.icon" :src="provider.icon" class="w-[18px] h-[18px]" :alt="provider.provider_name" />
          {{ provider.provider_name }}
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