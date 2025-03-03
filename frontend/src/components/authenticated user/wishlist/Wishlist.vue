<template>
    <div id="cart-view" v-if="user && user.wishlist">
        <div id="header">
            <p>My Wishlist</p>
        </div>
        <div id="resources">
            <div id="empty-message" v-if="user.wishlist.resources.length === 0">No items in wishlist</div>
            <div class="cart-item" v-for="resource in user.wishlist.resources">
                <div class="item-one">
                    <div class="item-image">
                        <img @click="view_item((allResources.find(res => res.id === resource.resource) as Resource)?.id)" :src="`http://localhost:8000${(allResources.find(res => res.id === resource.resource) as Resource)?.image1}`" alt="">
                    </div>
                    <div class="details">
                        <p>{{ (allResources.find(res => res.id === resource.resource) as Resource)?.name }}</p>
                        <p> {{ currency }}{{ parseFloat((allResources.find(res => res.id === resource.resource) as Resource)?.price.toString().replace('€','').replace('£','').replace('$','')) }}</p>
                        <p id="view-details" @click="view_item((allResources.find(res => res.id === resource.resource) as Resource)?.id)">View Details</p>
                    </div>
                </div>
                <div class="item-two">
                    <button id="move_to_cart" @click="move_to_cart(resource)">Move to Cart</button>
                    <button id="remove_from_wishlist" @click="remove_item(resource)">Remove</button>
                </div>
            </div>
        </div>
        <div id="buttons" v-if="user.wishlist.resources.length > 0">
            <button id="checkout" @click="add_wishlist">Move all to Cart</button>
            <button id="clear" @click="clear_wishlist">Clear</button>
        </div>
        <div v-if="error !== ''">
                <Error :message="error" @close-error="error = ''" />
        </div>
        <div v-if="confirm !== ''">
            <Confirm :message="confirm" @confirm-no="confirm=''" @confirm-yes="clear_wishlist" />
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Cart, CartResource, Resource, User, Wishlist, WishlistResource } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    import Error from '@/components/user experience/error/Error.vue';
    import Confirm from '@/components/user experience/confirm/Confirm.vue';
    export default defineComponent({
        components: { Error, Confirm },
        data(): {
            total: number,
            error: string,
            confirm: string,
        } { return {
            total: 0,
            error: '',
            confirm: ''
        }},
        methods: {
            async clear_wishlist(): Promise<void> {
                if (this.confirm === '') {
                    this.confirm = 'Are you sure you want to clear your wishlist?'
                    return
                }
                this.confirm = ''
                for (const wishlist_item of this.user.wishlist.resources) {
                    this.delete_wishlist_item(wishlist_item)
                }
            },
            async add_wishlist(): Promise<void> {
                for (const wishlist_item of this.user.wishlist.resources) {
                    this.move_to_cart(wishlist_item)
                }
            },
            async move_to_cart(resource: WishlistResource): Promise<void> {
                const moveToCartResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/wishlist/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(resource.id)
                })
                if (!moveToCartResponse.ok) {
                    this.error = 'Error moving to cart. Please try again.'
                    return
                }
                const data: {wishlist: Wishlist, cart: Cart} = await moveToCartResponse.json()
                useUserStore().updateWishlist(data.wishlist)
                useUserStore().updateCart(data.cart)
                useUsersStore().updateUser(this.user)
            },
            async delete_wishlist_item(resource: WishlistResource): Promise<void> {
                const deleteWishlistItemResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/wishlist/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(resource.resource)
                })
                if (!deleteWishlistItemResponse.ok) {
                    this.error = 'Error deleting from wishlist. Please try again'
                    return
                }
                this.error = ''
                const data: {wishlist: Wishlist} = await deleteWishlistItemResponse.json()
                useUserStore().updateWishlist(data.wishlist)
                useUsersStore().updateUser(this.user)
            },
            remove_item(resource: WishlistResource): void {
                this.delete_wishlist_item(resource)
            },
            view_item(id: number): void {
                window.location.href = `/view/${id}`
            },
            cart_price(resource: CartResource): number {
                const res = this.allResources.find(res => res.id === resource.resource)
                if (res) return parseFloat(res.price.toString().replace('€','').replace('£','').replace('$',''))
                return 0
            },
            async listedprice(resource: Resource): Promise<number> {
                if (resource === undefined) return 0
                let convertedPrice: Response = await fetch(`http://localhost:8000/api/currency-conversion/${resource.id}/${this.user.currency}/${resource.price_currency}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    }
                })
                if (!convertedPrice.ok) return resource.price
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return returnedPrice.new_price
            },
        },
        computed: {
            currency(): string {
                return this.user.currency === 'GBP' ? '£' : this.user.currency === 'USD' ? '$' : '€' 
            },
            user(): User {
                return useUserStore().user
            },
            allResources(): Resource[] {
                return useResourcesStore().resources
            },
            resource(): Resource | {} {
                const window_location: string[] = window.location.href.split('/')
                const name: string = window_location[window_location.length-1]
                return this.allResources[0]
            },
        },
        watch: {
            user(new_user: User): void {
            },
            async resource(resource: Resource): Promise<void> {
                resource.price = await this.listedprice(resource)
            },
        },
        mounted(): void {
            
        },
    })
</script>

<style scoped>
    .cart_total {
        margin-top: 0.5rem;
    }

    #cart-view {
        display: flex;
        flex-direction: column;
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        gap: 1rem;
    }

    #header {
        display: flex;
        justify-content: space-between;
    }

    #header p {
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }

    #header #total {
        font-weight: bold;
    }

    #resources {
        display: flex;
        flex-direction: column;
        gap: 3rem;
        overflow-y: scroll;
        height: 45rem;
    }

    .cart-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    img {
        max-height: 9rem;
        width: 9rem;
    }

    img:hover {
        cursor: pointer;
    }

    .item-one {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .details {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #view-details {
        color: rgb(121, 189, 218);
    }

    #dark #view-details {
        color: rgb(255, 255, 255);
    }

    #view-details:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    .item-two {
        display: flex;
        gap: 0.8rem;
        margin-right: 1rem;
    }

    .item-two button {
        border: none;
        border-radius: 0.5rem;
        background-color: #0DCAF0;
        padding: 0.5rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .item-two button:hover{
        background-color: #177183;
        cursor: pointer;
    }

    .number_toggle {
        display: flex;
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        padding-left: 0.4rem;
        padding-right: 0.4rem;
        padding-top: 0.3rem;
        padding-bottom: 0.3rem;
        width: 6rem;
        justify-content: space-between;
    }

    .number_controls {
        display: flex;
        background-color: white;
        border-radius: 0.3rem;
    }

    .number_controls hr {
        border: none;
        background-color: black;
        width: 0.01rem;
    }

    .number_controls p {
        width: 1.3rem;
        text-align: center;
    }

    .number_controls p:hover {
        background-color: darkgray;
        cursor: pointer;
    }

    #minus {
        border-top-right-radius: 0.3rem;
        border-bottom-right-radius: 0.3rem;
    }

    #plus {
        border-top-left-radius: 0.3rem;
        border-bottom-left-radius: 0.3rem;
    }

    #number {
        margin: auto;
    }

    #buttons {
        display: flex;
        gap: 1rem;
        align-items: center;
        justify-content: center;
    }

    #buttons button {
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem;
        font-size: 1.2rem;
    }

    #checkout {
        background-color: #0DCAF0;
    }

    #dark #checkout, #dark #move_to_cart {
        background-color: white;
    }

    #dark #checkout:hover, #dark #move_to_cart:hover {
        background-color: rgb(156, 154, 154);
    }
    
    #checkout:hover {
        cursor: pointer;
        background-color: #177183;
    }

    #clear, #remove_from_wishlist {
        background-color: red;
        color: white;
    }

    #dark #view-details {
        color: rgb(206, 206, 206);
    }

    #dark #cart-view {
        color: white;
    }

    #clear:hover, #remove_from_wishlist:hover {
        cursor: pointer;
        background-color: darkred;
    }

    #empty-message {
        text-align: center;
        font-size: 1.1rem;
    }

    /* Responsive Design */
    @media (max-width:585px) {
        .item-two {
            flex-direction: column;
            gap: 1rem;
        }
    }

    @media (max-width:468px) {
        .cart-item {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.4rem;
        }

        .item-two {
            flex-direction: row;
        }
    }
</style>