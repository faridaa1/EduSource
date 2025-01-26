import BuyerHome from '@/components/buyer/BuyerHome.vue'
import Details from '@/components/Details.vue'
import NewListing from '@/components/seller/NewListing.vue'
import Resource from '@/components/seller/Resource.vue'
import SellerHome from '@/components/seller/SellerHome.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: BuyerHome },
    { path: '/details', name: 'details', component: Details },
    { path: '/new-listing', name: 'new listing', component: NewListing },
    { path: '/seller-home', name: 'seller home', component: SellerHome },
    { path: '/buyer-home', name: 'buyer home', component: BuyerHome },
    { path: '/new-listing/textbook', name: 'new listing textbook', component: NewListing },
    { path: '/new-listing/notes', name: 'new listing notes', component: NewListing },
    { path: '/new-listing/stationery', name: 'new listing stationery', component: NewListing },
    { path: '/resource/:id', name: 'resource', component: Resource },
  ],
})

export default router
