import AuthBuyerHome from '@/components/AuthBuyerHome.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: AuthBuyerHome,
    },
  ],
})

export default router
