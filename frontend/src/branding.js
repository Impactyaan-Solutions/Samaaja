import { reactive } from 'vue'
import { getBranding } from '@/services/api'

// Branding set in Samaaja Settings > Branding. Each field is empty until
// it loads, or when it is left blank in Desk; screens then fall back to
// their translated defaults (landing.appName, landing.logo, landing.tagline*).
export const branding = reactive({
  appName: '',
  appLogo: '',
  tagLine: '',
})

export const loadBranding = async () => {
  try {
    const data = await getBranding()
    branding.appName = data.app_name || ''
    branding.appLogo = data.app_logo || ''
    branding.tagLine = data.tag_line || ''
  } catch (error) {
    // Not fatal: the defaults stay in place.
    console.error('Failed to load branding:', error)
  }
}
