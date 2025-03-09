<template>
    <div id="cart-view" v-if="user && user.cart">
        <div id="header">
            <p>My Cart</p>
            <p id="total">Total: {{ currency }}{{ parseFloat(total.toString()).toFixed(2) }}</p>
        </div>
        <div id="resources">
            <div id="empty-message" v-if="!user.cart.resources || (user.cart.resources.length === 0)">No items in cart</div>
            <div class="cart-item" v-for="resource in user.cart.resources">
                <div class="item-one">
                    <div class="item-image">
                        <img :src="`http://localhost:8000${(allResources.find(res => res.id === resource.resource) as Resource)?.image1}`"  @click="view_item((allResources.find(res => res.id === resource.resource) as Resource)?.id)">
                    </div>
                    <div class="details">
                        <p>{{ (allResources.find(res => res.id === resource.resource) as Resource)?.name }}</p>
                        <p>{{ (allResources.find(res => res.id === resource.resource) as Resource)?.price }}</p>
                        <p id="view-details" @click="view_item((allResources.find(res => res.id === resource.resource) as Resource)?.id)">View Details</p>
                    </div>
                </div>
                <div class="item-two">
                    <div class="item">
                        <div class="number_toggle">
                            <div id="number">{{ resource.number }}</div>
                            <div class="number_controls">
                                <p v-if="resource.number < (allResources.find(res => res.id === resource.resource) as Resource)?.stock" id="plus" @click="toggle_cart(resource, 1)">+</p>
                                <hr v-if="resource.number < (allResources.find(res => res.id === resource.resource) as Resource)?.stock">
                                <p id="minus" :class="resource.number < (allResources.find(res => res.id === resource.resource) as Resource)?.stock ? '' : 'round-border'" @click="toggle_cart(resource, -1)"><i :class="resource.number === 1 ? 'bi bi-trash3-fill' : ''"></i>{{ resource.number === 1 ? '' : '-' }}</p>
                            </div>
                        </div>
                        <div>
                            <div class="cart_total"> Total: {{ currency }}{{ (resource.number * cart_price(resource)).toFixed(2) }} </div>
                        </div>
                    </div>
                    <div class="move_to_wishlist">
                        <button @click="move_to_wishlist(resource)">Move to Wishlist</button>
                    </div>
                </div>
            </div>
            <div v-if="error !== ''">
                <Error :message="error" @close-error="error = ''" />
            </div>
            <div v-if="confirm !== ''">
                <Confirm :message="confirm" @confirm-no="confirm_no" @confirm-yes="confirm_yes" />
            </div>
        </div>
        <div id="buttons" v-if="user.cart.resources && user.cart.resources.length > 0">
            <button id="checkout" @click="checkout">Checkout</button>
            <button id="checkout" @click="move_all_wishlist">Move all to Wishlist</button>
            <button id="clear" @click="clear_cart">Clear</button>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Cart, CartResource, Resource, User, Wishlist } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    import Error from '@/components/user experience/error/Error.vue';
    import Confirm from '@/components/user experience/confirm/Confirm.vue';
    export default defineComponent({
        components: { Error, Confirm },
        data(): {
            remembered_resource: CartResource,
            error: string,
            confirm: string,
            confirm_caller: 'delete_cart_item' | 'clear_cart' | '',
            total: number,
        } { return {
            remembered_resource: {} as CartResource,
            total: 0,
            error: '',
            confirm: '',
            confirm_caller: ''
        }},
        methods: {
            confirm_yes(): void {
                if (this.confirm_caller === 'clear_cart') {
                    this.clear_cart()
                } else {
                    this.toggle_cart(this.remembered_resource, -1)
                }
                this.confirm = ''
                this.confirm_caller = ''
            },
            confirm_no(): void {
                this.confirm = ''
                this.confirm_caller = ''
            },
            async checkout(): Promise<void> {
                const validate_cart: Response = await fetch(`http://localhost:8000/api/update-cart/user/${this.user.id}/cart/-1/resource/-1/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                    },
                })
                if (!validate_cart.ok) {
                    this.error = 'Error taking you to checkout. Please try again.'
                    return
                }
                const data: Cart = await validate_cart.json()
                useUserStore().updateCart(data)
                useUsersStore().updateUser(this.user)
                window.location.href = '/checkout'
            },
            move_all_wishlist(): void {
                for (let cart_item of this.user.cart.resources) {
                    this.move_to_wishlist(cart_item)
                }
            },
            async move_to_wishlist(resource: CartResource): Promise<void> {
                const moveToWishlist: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/cart-to-wishlist/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(resource.id)
                })
                if (!moveToWishlist.ok) {
                    this.error = 'Error moving to wishlist. Please try again.'
                    return
                }
                const data: {wishlist: Wishlist, cart: Cart} = await moveToWishlist.json()
                useUserStore().updateCart(data.cart)
                useUserStore().updateWishlist(data.wishlist)
                useUsersStore().updateUser(this.user)
            },
            async clear_cart(): Promise<void> {
                if (this.confirm === '') {
                    this.confirm = 'Are you sure you want to clear your cart'
                    this.confirm_caller = 'clear_cart'
                    return
                }
                for (const cart_item of this.user.cart.resources) {
                    this.delete_cart_item(cart_item)
                }
            },
            async delete_cart_item(resource: CartResource): Promise<void> {
                const deleteCartItem: Response = await fetch(`http://localhost:8000/api/update-cart/user/${this.user.id}/cart/${resource.id}/resource/${resource.resource}/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                })
                if (!deleteCartItem.ok) {
                    this.error = 'Error deleting from cart. Please try again.'
                    return
                }
                const data: {resource: CartResource, cart: Cart} = await deleteCartItem.json()
                useUserStore().updateCart(data.cart)
                useUsersStore().updateUser(this.user)
            },
            async edit_cart_item(resource: CartResource, value: number): Promise<void> {
                const putCartItem: Response = await fetch(`http://localhost:8000/api/update-cart/user/${this.user.id}/cart/${resource.id}/resource/${resource.resource}/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(value)
                })
                if (!putCartItem.ok) {
                    this.error = 'Error editing cart. Please try again.'
                    return
                }
                const data: {resource: CartResource, cart: Cart} = await putCartItem.json()
                useUserStore().updateCart(data.cart)
                useUsersStore().updateUser(this.user)
            },
            toggle_cart(resource: CartResource, value: number): void {
                if (resource.number === 1 && value === -1) {
                    if (this.confirm === '') {
                        this.remembered_resource = resource
                        this.confirm = 'Are you sure you want to delete this item from your cart?'
                        this.confirm_caller = 'delete_cart_item'
                        return
                    }
                    this.delete_cart_item(resource)
                } else {
                    this.edit_cart_item(resource, resource.number + value)
                }
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
            async update_total(): Promise<void> {
                if ((Object.keys(this.allResources).length === 0)|| (!this.user.cart.resources)) {
                    this.total = 0 
                    return
                }
                const cart_res = this.user.cart.resources.map(item => item.resource)
                this.total = 0
                for (const resource of this.allResources.filter(res => cart_res.includes(res.id))) {
                    resource.price = await this.listedprice(resource)
                    const cart_item = this.user.cart.resources.find(item => item.resource === resource.id)
                    if (cart_item) {
                        const price = parseFloat(resource.price.toString().replace('€','').replace('£','').replace('$',''))
                        this.total += (price * cart_item.number)
                    }
                }
            }
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
                this.update_total()
            },
            async resource(resource: Resource): Promise<void> {
                resource.price = await this.listedprice(resource)
            },
            "user.cart"(): void {
                this.update_total()
            },
            allResources(): void {
                this.update_total()
            }
        },
        mounted(): void {
            this.update_total()
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
        overflow-y: auto;
        height: 45rem;
    }

    .cart-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    img {
        height: 9rem;
        width: 9rem;
        object-fit: contain;
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
        color: rgb(206, 206, 206);
    }

    #view-details:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    .item {
        display: flex;
        flex-direction: column;
        margin-right: 1rem;
        align-items: center;
    }

    .item-two {
        display: flex;
        margin-right: 1rem;
    }

    .move_to_wishlist button {
        background-color: #0DCAF0;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .move_to_wishlist button:hover {
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

    .round-border {
        border-top-left-radius: 0.3rem;
        border-bottom-left-radius: 0.3rem;
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

    #dark #checkout, #dark .move_to_wishlist button {
        background-color: white;
    }

    #dark #checkout:hover, #dark .move_to_wishlist button:hover {
        background-color: rgb(156, 154, 154);
    }

    #checkout:hover {
        cursor: pointer;
        background-color: #177183;
    }

    #clear {
        background-color: red;
        color: white;
    }

    #clear:hover {
        cursor: pointer;
        background-color: darkred;
    }

    #empty-message {
        text-align: center;
        font-size: 1.1rem;
    }

    #minus i {
        color: red !important;
        font-size: 0.8rem;
    }

    #dark #cart-view {
        color: white;
    }

    #dark #minus, #dark #plus, #dark #number {
        color: black;
    }

    #dark #view-details {
        color: rgb(206, 206, 206);
    }

    /* Responsive Design */
    @media (max-width: 637px) {
        .item-two {
            flex-direction: column;
            gap: 1rem;
        }
    }

    @media (max-width: 522px) {
        .cart-item {
            flex-direction: column;
            align-items: flex-start;
        }

        .item-two {
            flex-direction: row;
        }
    }
</style>