import { createRouter, createWebHistory } from 'vue-router'
import { authState, checkAuth, isProfileComplete } from '../auth' // Ensure this import exists!

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landingpage',
      meta: { hideNavbar: true, public: true },
      component: () => import('../views/Landing.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      meta: { hideNavbar: true, public: true },
      component: () => import('../views/Signup.vue')
    },
    {
      path: '/login',
      name: 'login',
      meta: { hideNavbar: true, public: true },
      component: () => import('../views/Login.vue')
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: () => import('../views/Leaderboard.vue')
    },
    {
      path: '/homepage',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/announcements',
      name: 'announcements',
      component: () => import('../views/Announcements.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue')
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
      component: () => import('../views/ProfileCompletion.vue')
    },
    {
      path: '/log-action',
      name: 'log-action',
      component: () => import('../views/LogAction.vue')
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