import { createRouter, createWebHistory } from 'vue-router'
import { authState, checkAuth, isProfileComplete } from '../auth' // Ensure this import exists!

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landingpage',
      meta: { hideNavbar: true, public: true },
      component: () => import('../views/landingpage.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      meta: { hideNavbar: true, public: true },
      component: () => import('../views/SignupView.vue')
    },
    {
      path: '/login',
      name: 'login',
      meta: { hideNavbar: true, public: true },
      component: () => import('../views/loginview.vue')
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: () => import('../views/LeaderboardView.vue')
    },
    {
      path: '/homepage',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/announcements',
      name: 'announcements',
      component: () => import('../views/AnnouncementsView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue')
    },
    {
      path: '/settings',
      name: 'settings',
      meta: { hideNavbar: true },
      component: () => import('../views/Settings.vue')
    },
    {
      path: '/complete-profile',
      name: 'complete-profile',
      meta: { hideNavbar: true },
      component: () => import('../views/ProfileCompletionView.vue')
    },
    {
      path: '/log-action',
      name: 'log-action',
      component: () => import('../views/LogActionView.vue')
    }
  ]
})

/**
 * Navigation Guard
 */
router.beforeEach(async (to, from, next) => {
  // 1. Ensure we check the server session on initial load/reload
  if (authState.isInitialLoad) {
    await checkAuth();
  }

  const isLoggedIn = authState.isLoggedIn;
  const isPublic = to.meta.public;
  const profileComplete = isProfileComplete();

  // 2. Redirect Logic - Logic is evaluated top-down

  // Force onboarding if profile is incomplete
  if (isLoggedIn && !profileComplete && to.name !== 'complete-profile') {
    return next({ name: 'complete-profile' });
  }

  // Prevent accessing onboarding if profile is already complete
  if (isLoggedIn && profileComplete && to.name === 'complete-profile') {
    return next({ name: 'home' });
  }

  if (isLoggedIn && (to.name === 'login' || to.name === 'signup' || to.name === 'landingpage')) {
    // Already logged in? Send them to the app.
    return next({ name: 'home' });
  }

  if (!isPublic && !isLoggedIn) {
    // Not logged in and trying to access a private page? Send to landing/login.
    return next({ name: 'landingpage' });
  }

  // If none of the above rules hit, proceed as normal
  next();
});

export default router