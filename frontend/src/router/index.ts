import Home from '@/components/Home.vue'
import BuyerResource from '@/components/buyer/Resource.vue'
import Details from '@/components/Details.vue'
import NewListing from '@/components/seller/NewListing.vue'
import Resource from '@/components/seller/Resource.vue'
import Listings from '@/components/seller/Listings.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Cart from '@/components/Cart.vue'
import Wishlist from '@/components/Wishlist.vue'
import Checkout from '@/components/authenticated user/checkout/Checkout.vue'
import OrderConfirmation from '@/components/authenticated user/checkout/OrderConfirmation.vue'
import Orders from '@/components/authenticated user/orders/Orders.vue'
import Order from '@/components/authenticated user/orders/Order.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/details', name: 'details', component: Details },
    { path: '/new-listing', name: 'new listing', component: NewListing },
    { path: '/listings', name: 'listings', component: Listings },
    { path: '/new-listing/textbook', name: 'new listing textbook', component: NewListing },
    { path: '/new-listing/notes', name: 'new listing notes', component: NewListing },
    { path: '/new-listing/stationery', name: 'new listing stationery', component: NewListing },
    { path: '/resource/:id', name: 'resource', component: Resource },
    { path: '/view/:name', name: 'buyer resource', component: BuyerResource },
    { path: '/cart', name: 'cart', component: Cart },
    { path: '/wishlist', name: 'wishlist', component: Wishlist },
    { path: '/checkout', name: 'checkout', component: Checkout },
    { path: '/order-confirmation', name: 'order confirmation', component: OrderConfirmation },
    { path: '/orders', name: 'orders', component: Orders },
    { path: '/order/:id', name: 'order', component: Order },
  ],
})

export default router
