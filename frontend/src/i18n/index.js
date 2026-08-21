import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import hi from './locales/hi.json'

export const SUPPORTED_LOCALES = ['en', 'hi']
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
