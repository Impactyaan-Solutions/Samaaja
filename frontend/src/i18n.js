import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import hi from './locales/hi.json'

const i18n = createI18n({
  legacy: false,
  // Loads saved language from localStorage, defaults to 'en'
  locale: localStorage.getItem('lang') || 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    hi
  }
})

export default i18n