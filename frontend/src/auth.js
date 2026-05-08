import { reactive } from 'vue'

export const authState = reactive({
  isLoggedIn: false,
  user: null,
  isInitialLoad: true
})

export async function checkAuth() {
  try {
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