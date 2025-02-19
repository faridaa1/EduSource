import { defineStore } from 'pinia';
import type { Cart, Resource, User, Wishlist, WishlistResource } from '../types';

export const useUserStore = defineStore('user', {
    state: (): { user: User, csrf: string} => ({
        user: {} as User,
        csrf: ''
    }),
    actions: {
        saveUser(user: User): void {
            this.user = user
        },
        saveCsrf(csrf: string): void {
            this.csrf = csrf
        },
        addListing(listing: Resource): void {
            this.user.listings.push(listing)
        },
        updateListing(new_listing: Resource): void {
            let resource = this.user.listings.find(listing => listing.id === new_listing.id) 
            if (resource) {
                Object.assign(resource, new_listing)
            }
        },
        removeResource(id: number): void {
            this.user.listings = this.user.listings.filter(resource => resource.id !== id)
        },
        updateCart(new_cart: Cart): void {
            this.user.cart = new_cart
        },
        updateWishlist(new_wishlist: Wishlist): void {
            this.user.wishlist = new_wishlist
        }
    }
})