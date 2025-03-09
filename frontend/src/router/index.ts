import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Resource from '@/components/view resource/Resource.vue'
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
import SearchResults from '@/components/search/SearchResults.vue'
import Settings from '@/components/authenticated user/settings/Settings.vue'
import Return from '@/components/authenticated user/orders/Return.vue'
import Exchange from '@/components/authenticated user/exchange/Exchange.vue'
import Exchanges from '@/components/authenticated user/exchange/Exchanges.vue'
import CompareResources from '@/components/search/CompareResources.vue'
import Help from '@/components/help/Help.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/settings', name: 'settings', component: Settings },
    { path: '/help', name: 'help', component: Help },
    { path: '/details', name: 'details', component: Details },
    { path: '/new-listing/:catchAll(.*)', name: 'new listing', component: Listing },
    { path: '/resource/:id', name: 'resource', component: Listing },
    { path: '/listings', name: 'listings', component: SellerProfile },
    { path: '/view/:resourceid/add-review', name: 'add review', component: Resource },
    { path: '/view/:resourceid/review/:reviewid', name: 'view review', component: Resource },
    { path: '/view/:id', name: 'buyer resource', component: Resource },
    { path: '/cart', name: 'cart', component: Cart },
    { path: '/wishlist', name: 'wishlist', component: Wishlist },
    { path: '/fast-checkout/:id', component: Checkout },
    { path: '/checkout/', component: Checkout },
    { path: '/order-confirmation', name: 'order confirmation', component: OrderConfirmation },
    { path: '/orders', name: 'orders', component: Orders },
    { path: '/orders/:catchAll(.*)', name: 'back orders', component: Orders },
    { path: '/order/:catchAll(.*)', name: 'order', component: Order },
    { path: '/return/:catchAll(.*)', name: 'return', component: Return },
    { path: '/seller/:name', name: 'seller profile', component: SellerProfile },
    { path: '/message/:user1/:user2', name: 'message', component: Message },
    { path: '/messages', name: 'messages', component: Messages },
    { path: '/search/:name', name: 'search', component: SearchResults },
    { path: '/exchanges', name: 'exchanges', component: Exchanges },
    { path: '/compare/:catchAll(.*)', name: 'compare', component: CompareResources },
    { path: '/exchange/:catchAll(.*)', name: 'exchange', component: Exchange }
  ],
})

export default router
