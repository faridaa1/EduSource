import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Resource from '@/components/authenticated user/view resource/Resource.vue'
import Details from '@/components/authenticated user/profile/Details.vue'
import Listing from '@/components/authenticated user/seller/Listing.vue'
import Cart from '@/components/authenticated user/cart/Cart.vue'
import Wishlist from '@/components/authenticated user/wishlist/Wishlist.vue'
import Checkout from '@/components/authenticated user/checkout/Checkout.vue'
import OrderConfirmation from '@/components/authenticated user/checkout/OrderConfirmation.vue'
import Orders from '@/components/authenticated user/orders/Orders.vue'
import Order from '@/components/authenticated user/orders/Order.vue'
import SellerProfile from '@/components/SellerProfile.vue'
import Message from '@/components/authenticated user/messaging/Message.vue'
import Messages from '@/components/authenticated user/messaging/Messages.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/details', name: 'details', component: Details },
    { path: '/new-listing/:catchAll(.*)', name: 'new listing', component: Listing },
    { path: '/resource/:id', name: 'resource', component: Listing },
    { path: '/listings', name: 'listings', component: SellerProfile },
    { path: '/view/:id', name: 'buyer resource', component: Resource },
    { path: '/cart', name: 'cart', component: Cart },
    { path: '/wishlist', name: 'wishlist', component: Wishlist },
    { path: '/checkout', name: 'checkout', component: Checkout },
    { path: '/order-confirmation', name: 'order confirmation', component: OrderConfirmation },
    { path: '/orders', name: 'orders', component: Orders },
    { path: '/order/:id', name: 'order', component: Order },
    { path: '/seller/:name', name: 'seller profile', component: SellerProfile },
    { path: '/message/:user1/:user2s', name: 'message', component: Message },
    { path: '/messages', name: 'messages', component: Messages },
  ],
})

export default router
