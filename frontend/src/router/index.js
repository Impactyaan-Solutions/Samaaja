import { createRouter, createWebHistory } from 'vue-router'
import { authState, checkAuth, isProfileComplete } from '../auth' // Ensure this import exists!

const router = createRouter({
  history: createWebHistory('/'),
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
      path: '/admin-login',
      name: 'admin-login',
      meta: { hideNavbar: true, public: true },
      component: () => import('../views/AdminLogin.vue')
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
     path: '/events/:id',
     name: 'event-detail',
     component: () => import('../views/EventDetail.vue')
    },
    {
      path: '/event-register/:id',
      name: 'event-register',
      component: () => import('../views/EventRegister.vue')
    },
    {
      path: '/event-registerd/:id',
      name: 'event-registerd',
      component: () => import('../views/EventRegistrationSuccess.vue')
    },
    {
      path: '/event-checkin/:id',
      name: 'event-checkin',
      component: () => import('../views/EventAttendence.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/volunteer-listings',
      name: 'volunteer-listings',
      component: () => import('../views/VolunteerListings.vue')
    },
    {
      path: '/volunteer-listings/:id',
      name: 'volunteer-opportunity-detail',
      component: () => import('../views/VolunteerOpportunityDetail.vue')
    },
    
    {
      path: '/volunteer-listings/:id/apply',
      name: 'volunteer-application',
      component: () => import('../views/VolunteerApplicationForm.vue')
    },
    {
      // Renamed from /profile: Frappe already uses that address for the
      // logged-in user's own account page. We leave it to Frappe rather
      // than fight over it.
      path: '/account',
      name: 'account',
      component: () => import('../views/Profile.vue')
    },
    {
      path: '/project/:id',
      name: 'project',
      component: () => import('../views/Project.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
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
    },
    {
      path: '/add-post',
      name: 'add-post',
      component: () => import('../views/AddPost.vue')
    }
  ]
})

/**
 * Navigation Guard
 */
router.beforeEach(async (to, from, next) => {
  console.log(`Navigating to ${to.name} from ${from.name}`);
  // if (import.meta.env.DEV === true) {
  //   console.log("Development mode: auto-logging in as Administrator");
  //   authState.isLoggedIn = true;
  //   authState.email = 'Administrator';
  //   authState.profile.fullName = 'Ankit Saxena';
  //   authState.profile.category = 'Admin';
  //   next();
  //   return;
  // }

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

  // if (!isPublic && !isLoggedIn) {
  //   // Not logged in and trying to access a private page? Send to landing/login.
  //   return next({ name: 'landingpage' });
  // }
  if (!isPublic && !isLoggedIn) {
  return next({
    name: 'login',
    query: {
      redirect: to.fullPath
    }
  });
}

  // If none of the above rules hit, proceed as normal
  next();
});

export default router