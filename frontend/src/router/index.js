import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landingpage',
      meta: { hideNavbar: true },
      component: () => import('../views/landingpage.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      meta: { hideNavbar: true },
      component: () => import('../views/SignupView.vue')
    },

    {
      path: '/login',
      name: 'login',
      meta: { hideNavbar: true },
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
      path: '/log-action',
      name: 'log-action',
      component: () => import('../views/LogActionView.vue')
    }
  ]
})

export default router
