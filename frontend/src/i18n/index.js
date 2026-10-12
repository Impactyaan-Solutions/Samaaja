import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import hi from './locales/hi.json'

export const SUPPORTED_LOCALES = ['en', 'hi']
// Web Speech API needs a full BCP-47 tag (e.g. 'en-IN'), not the short
// app locale codes above. Add an entry here whenever SUPPORTED_LOCALES gains a language.
export const SPEECH_RECOGNITION_LOCALES = {
  en: 'en-IN',
  hi: 'hi-IN'
}
const STORAGE_KEY = 'app_locale'
const DEFAULT_LOCALE = 'en'

function resolveInitialLocale() {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored && SUPPORTED_LOCALES.includes(stored)) return stored

  const browserLocale = navigator.language?.split('-')[0]
  if (browserLocale && SUPPORTED_LOCALES.includes(browserLocale)) return browserLocale

  return DEFAULT_LOCALE
}

const i18n = createI18n({
  legacy: false,
  locale: resolveInitialLocale(),
  fallbackLocale: DEFAULT_LOCALE,
  messages: { en, hi }
})

export function setLocale(locale) {
  if (!SUPPORTED_LOCALES.includes(locale)) return
  i18n.global.locale.value = locale
  localStorage.setItem(STORAGE_KEY, locale)
  document.documentElement.setAttribute('lang', locale)
}

export default i18n
