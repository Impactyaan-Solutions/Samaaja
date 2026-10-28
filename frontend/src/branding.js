import { reactive } from 'vue'
import { getBranding } from '@/services/api'

const BRANDING_CACHE_KEY = 'samaaja_branding_cache'

// Null fields mean "not customized" - components fall back to the i18n
// defaults (landing.appName / landing.logo.src / landing.tagline) in that
// case, this store only ever overrides them when Samaaja Settings' own
// Branding tab actually has a value.
export const brandingState = reactive({
  appName: null,
  logo: null,
  tagline: null,
  primaryColor: null,
  accentColor: null,
})

const loadCachedBranding = () => {
  const cached = localStorage.getItem(BRANDING_CACHE_KEY)
  if (!cached) return
  try {
    Object.assign(brandingState, JSON.parse(cached))
  } catch (e) {
    console.error('Failed to parse cached branding', e)
  }
}

const saveCachedBranding = () => {
  localStorage.setItem(BRANDING_CACHE_KEY, JSON.stringify(brandingState))
}

const applyBrandColors = () => {
  const root = document.documentElement
  if (brandingState.primaryColor) {
    root.style.setProperty('--brand-primary', brandingState.primaryColor)
  }
  if (brandingState.accentColor) {
    root.style.setProperty('--brand-accent', brandingState.accentColor)
  }
}

// Load from cache immediately on app start, so a repeat visit paints the
// right colors/name before the network round trip below even starts.
loadCachedBranding()
applyBrandColors()

export async function loadBranding() {
  try {
    const data = await getBranding()
    brandingState.appName = data.app_name || null
    brandingState.logo = data.logo || null
    brandingState.tagline = data.tagline || null
    brandingState.primaryColor = data.primary_color || null
    brandingState.accentColor = data.accent_color || null
    saveCachedBranding()
    applyBrandColors()
  } catch (error) {
    console.error('Failed to load branding:', error)
  }
}
