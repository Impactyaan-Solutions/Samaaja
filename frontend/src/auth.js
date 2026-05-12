import { reactive } from 'vue'
import { getLoggedUser, getProfile, fetchImageAsBase64 } from '@/services/api'

const API_KEY = import.meta.env.VITE_API_KEY
const API_SECRET = import.meta.env.VITE_API_SECRET
const AUTH_CACHE_KEY = 'samaaja_auth_cache'

export const authState = reactive({
  isLoggedIn: false,
  email: null,
  isInitialLoad: true,
  profile: {
    fullName: null,
    image: null,
    imageBase64: null,
    category: null,
    organization: null,
    interests: [],
    gender: null,
    dob: null,
    mobileNumber: null,
    bio: null, // Separating bio from interests for clarity if needed, or keeping it as interests
    stats: {
      actions: 0,
      posts: 0,
      hours: 0
    }
  }
})

export const isProfileComplete = () => {
  const p = authState.profile;
  // All these are mandatory: Gender, Bio (interests/bio), Category, Date of birth, Mobile Number
  // Using interests or bio based on what gets saved. Let's rely on 'bio'.
  return !!(p.gender && p.bio && p.category && p.dob && p.mobileNumber);
}

const loadCachedAuth = () => {
  const cached = localStorage.getItem(AUTH_CACHE_KEY)
  if (cached) {
    try {
      const parsed = JSON.parse(cached)
      Object.assign(authState, parsed, { isInitialLoad: true }) // Keep isInitialLoad true so checkAuth still runs
    } catch (e) {
      console.error("Failed to parse cached auth", e)
    }
  }
}

const saveCachedAuth = () => {
  const stateToCache = { ...authState }
  delete stateToCache.isInitialLoad // Don't cache the loading state itself
  localStorage.setItem(AUTH_CACHE_KEY, JSON.stringify(stateToCache))
}

const clearCachedAuth = () => {
  localStorage.removeItem(AUTH_CACHE_KEY)
}

// Load from cache immediately on app start
loadCachedAuth()

export async function checkAuth() {
  try {
    if (import.meta.env.DEV === true) {
      authState.isLoggedIn = true;
      authState.email = 'Administrator';
      authState.profile.fullName = 'Ankit Saxena';
      authState.profile.image = 'https://dev.samaaja.impactyaan.com/files/recall.png';
      authState.profile.category = 'Volunteer';
      authState.profile.organization = 'Samaaja';
      authState.profile.interests = 'Community, Volunteering, Social Work';
      authState.profile.bio = 'Passionate about helping the community.';
      authState.profile.gender = 'Male';
      authState.profile.dob = '1990-01-01';
      authState.profile.mobileNumber = '9876543210';
      authState.profile.stats.actions = 10;
      authState.profile.stats.issuesReported = 5;
      // Cache the fresh data!
      saveCachedAuth()
      // Fetch the image in the background and cache the base64!
      await fetchImageAsBase64(authState.profile.image).then(base64 => {
        //console.log("Image Base64: ", base64)
        if (base64) {
          authState.profile.imageBase64 = base64;
          saveCachedAuth();
        }
      });
      return;
    }

    const data = await getLoggedUser();
    authState.email = data;
    authState.isLoggedIn = true;
    authState.isInitialLoad = false;
    const user_profile = await getProfile(data)
    if (user_profile) {
      authState.profile.fullName = user_profile.full_name
      authState.profile.image = user_profile.user_image
      authState.profile.category = user_profile.user_category
      authState.profile.organization = user_profile.user_organization
      authState.profile.gender = user_profile.gender
      authState.profile.dob = user_profile.birth_date // Assuming Frappe standard field
      authState.profile.mobileNumber = user_profile.mobile_no // Assuming Frappe standard field
      authState.profile.bio = user_profile.bio
      authState.profile.interests = user_profile.interests
      authState.profile.badges = user_profile.badges
      authState.profile.stats.actions = user_profile.action_count || 0
      authState.profile.stats.posts = user_profile.posts || 0
      authState.profile.stats.hours = user_profile.hours_invested || 0

      // Cache the fresh data!
      saveCachedAuth()

      // Fetch the image in the background and cache the base64!
      if (user_profile.user_image) {
        fetchImageAsBase64(user_profile.user_image).then(base64 => {
          if (base64) {
            authState.profile.imageBase64 = base64;
            saveCachedAuth();
          }
        });
      }
    }
  } catch (error) {
    console.log("Error: ", error)
    authState.isLoggedIn = false;
    clearCachedAuth() // Clear cache if the session is dead
  }
}

export const getRequestOptions = () => {
  return {
    credentials: 'include'
  }
}

export const getAPIToken = () => {
  return `token ${API_KEY}:${API_SECRET}`
}