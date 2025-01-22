import AuthBuyerHome from '@/components/AuthBuyerHome.vue'
import Details from '@/components/Details.vue'
import Listings from '@/components/seller/Listings.vue'
import NewListing from '@/components/seller/NewListing.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: AuthBuyerHome },
    { path: '/details', name: 'details', component: Details },
    { path: '/listings', name: 'listings', component: Listings },
    { path: '/new-listing', name: 'new listing', component: NewListing },
  ],
})

export default router
