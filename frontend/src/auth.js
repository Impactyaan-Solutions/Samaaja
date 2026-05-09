import { reactive } from 'vue'


const key = import.meta.env.VITE_API_KEY
const secret = import.meta.env.VITE_API_SECRET


export const authState = reactive({
  isLoggedIn: false,
  user: null,
  isInitialLoad: true
})

export async function checkAuth() {
  try {

    if (import.meta.env.DEV === true) {
      authState.isLoggedIn = true;
      authState.user = 'Administrator';
      return;
    }
    // We call Frappe's standard method to get the current user
    const response = await fetch('/api/method/frappe.auth.get_logged_user');
    const data = await response.json();

    if (data.message && data.message !== 'Guest') {
      authState.isLoggedIn = true;
      authState.user = data.message;
    } else {
      authState.isLoggedIn = false;
      authState.user = null;
    }
  } catch (error) {
    console.error("Auth check failed", error);
    authState.isLoggedIn = false;
  } finally {
    // Mark the check as complete so the router can proceed
    authState.isInitialLoad = false;
  }
}
export const getRequestOptions = () => {
  if (import.meta.env.DEV) {
    return {
      headers: {
        Authorization: `token ${key}:${secret}`
      }
    }
  }
  return {
    credentials: 'include'
  }
}