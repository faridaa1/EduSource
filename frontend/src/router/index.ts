import AuthBuyerHome from '@/components/AuthBuyerHome.vue'
import Details from '@/components/Details.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: AuthBuyerHome,
    },
    {
      path: '/details',
      name: 'details',
      component: Details,
    },
  ],
})

export default router
