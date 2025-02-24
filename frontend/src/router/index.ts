import Home from '@/components/Home.vue'
import Resource from '@/components/buyer/Resource.vue'
import Details from '@/components/Details.vue'
import NewListing from '@/components/seller/NewListing.vue'
import Listing from '@/components/seller/Listing.vue'
import Listings from '@/components/seller/Listings.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Cart from '@/components/Cart.vue'
import Wishlist from '@/components/Wishlist.vue'
import Checkout from '@/components/authenticated user/checkout/Checkout.vue'
import OrderConfirmation from '@/components/authenticated user/checkout/OrderConfirmation.vue'
import Orders from '@/components/authenticated user/orders/Orders.vue'
import Order from '@/components/authenticated user/orders/Order.vue'
import SellerProfile from '@/components/seller/SellerProfile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/details', name: 'details', component: Details },
    { path: '/new-listing/:catchAll(.*)', name: 'new listing', component: Listing },
    { path: '/resource/:id', name: 'resource', component: Listing },
    { path: '/listings', name: 'listings', component: Listings },
    { path: '/view/:id', name: 'buyer resource', component: Resource },
    { path: '/cart', name: 'cart', component: Cart },
    { path: '/wishlist', name: 'wishlist', component: Wishlist },
    { path: '/checkout', name: 'checkout', component: Checkout },
    { path: '/order-confirmation', name: 'order confirmation', component: OrderConfirmation },
    { path: '/orders', name: 'orders', component: Orders },
    { path: '/order/:id', name: 'order', component: Order },
    { path: '/seller/:name', name: 'seller profile', component: SellerProfile },
  ],
})

export default router
