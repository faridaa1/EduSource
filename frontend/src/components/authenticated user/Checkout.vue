<template>
    <div v-if="user.cart" id="checkout">
        <div id="header">Checkout</div>
        <div id="content">
            <div id="col1">
                <div id="items">
                    <div id="header">
                        <div id="one">Items</div>
                        <div id="two">Total: </div>
                    </div>
                    <div id="body">
                        <div class="resource" v-for="resource in user.cart.resources">
                            <div id="image"><img :src="`http://localhost:8000/${getResource(resource.resource).image1}`" alt=""></div>
                            <div class="name">
                                <div>{{ getResource(resource.resource).name }}</div>
                                <div id="toggle">
                                    <div id="resnum">{{ resource.number }}</div>
                                    <div id=controls>
                                        <div id="plus" v-if="resource.number < getResource(resource.resource).stock" @click="add_to_cart(resource)">+</div>
                                        <hr>
                                        <div id="minus" @click="remove_from_cart(resource)">-</div>
                                    </div>
                                </div>
                                <div>{{ user.currency === 'GBP' ? '£' : user.currency === 'USD' ? '$' : '€'  }}{{ (resource.number*parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="payment"></div>
            </div>
            <div id="col2">
                <div id="address"></div>
                <div id="number"></div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Cart, CartResource, Resource, Review, User, Wishlist } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
        } { return {
        }},
        methods: {
            async remove_from_cart(resource: CartResource): Promise<void> {
                if (resource.number === 1) {
                    if (!confirm('Are you sure you want to delete this item')) {
                        return
                    }
                }
                const putCartItem: Response = await fetch(`http://localhost:8000/api/update-cart/user/${this.user.id}/cart/${resource.id}/resource/${resource.resource}/`, {
                    method: resource.number === 1 ? 'DELETE' : 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(resource.number-1)
                })
                if (!putCartItem.ok) {
                    console.error('Error editing cart')
                    return
                }
                const data: {resource: CartResource, cart: Cart} = await putCartItem.json()
                useUserStore().updateCart(data.cart)
                useUsersStore().updateUser(this.user)
            },
            async add_to_cart(resource: CartResource): Promise<void> {
                const putCartItem: Response = await fetch(`http://localhost:8000/api/update-cart/user/${this.user.id}/cart/${resource.id}/resource/${resource.resource}/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(resource.number+1)
                })
                if (!putCartItem.ok) {
                    console.error('Error editing cart')
                    return
                }
                const data: {resource: CartResource, cart: Cart} = await putCartItem.json()
                useUserStore().updateCart(data.cart)
                useUsersStore().updateUser(this.user)
            },
            getResource(resource_id: number): Resource {
                const resource: Resource | undefined = useResourcesStore().resources.find(resource => resource.id === resource_id)
                if (resource) return resource
                return {} as Resource
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
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return returnedPrice.new_price
            },
        },
        computed: {
            users(): User[] {
                return useUsersStore().users
            },
            user(): User {
                return useUserStore().user
            },
            all_resources(): Resource[] {
                return useResourcesStore().resources
            }
        },
        async mounted(): Promise<void> {
            for (const resource of useResourcesStore().resources) {
                resource.price = await this.listedprice(resource)
            }
        },
        watch: {
            async all_resources(): Promise<void> {
                for (const resource of useResourcesStore().resources) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async user(): Promise<void> {
                for (const resource of useResourcesStore().resources) {
                    resource.price = await this.listedprice(resource)
                }
            }
        },
    })
</script>

<style scoped>

    #body {
        height: 25rem;
        overflow-y: scroll;
        border: 0.1rem solid #0DCAF0;
        padding: 1rem;
        border-radius: 0.8rem;
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    img {
        width: 8rem;
    }

    .resource {
        display: flex;
        align-items: center;
        gap: 2rem;
        text-align: center;
    }

    #toggle {
        background-color: #D9D9D9;
        display: flex;
        width: 6rem;
        padding-left: 0.4rem;
        padding-right: 0.4rem;
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        border-radius: 0.5rem;
        align-items: center;
    }

    #controls {
        display: flex;
        background-color: white;
        margin-left: auto;
        border-radius: 0.2rem;
    }

    #controls div {
        width: 1rem;
    }

    #controls div:hover {
        background-color: darkgray;
        cursor: pointer;
    }

    hr { 
        border: none;
        background-color: black;
        width: 0.01rem;
    }

    #plus:hover {
        border-top-left-radius: 0.2rem;
        border-bottom-left-radius: 0.2rem;
    }

    #minus:hover {
        border-top-right-radius: 0.2rem;
        border-bottom-right-radius: 0.2rem;
    }

    #resnum {
        margin: auto;
    }

    .name {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
</style>