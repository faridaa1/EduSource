<template>
    <div id="cart-view" v-if="user && user.cart">
        <div id="header">
            <p>My Cart</p>
            <p id="total">Total: {{ user.cart.total }}</p>
        </div>
        <div id="resources">
            <div class="cart-item" v-for="resource in user.cart.resources">
                <div class="item-one">
                    <div class="item-image">
                        <img :src="`http://localhost:8000${(allResources.find(res => res.id === resource.resource) as Resource)?.image1}`" alt="">
                    </div>
                    <div class="details">
                        <p>{{ (allResources.find(res => res.id === resource.resource) as Resource)?.name }}</p>
                        <p>{{ (allResources.find(res => res.id === resource.resource) as Resource)?.price }}</p>
                        <p id="view-details" @click="view_item((allResources.find(res => res.id === resource.resource) as Resource)?.name)">View Details</p>
                    </div>
                </div>
                <div class="item-two">
                    <div class="number_toggle">
                        <div id="number">{{ resource.number }}</div>
                        <div class="number_controls">
                            <p id="plus">+</p>
                            <hr>
                            <p id="minus">-</p>
                        </div>
                    </div>
                    <div>
                        <p>price is here</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Cart, CartResource, Resource, Review, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    export default defineComponent({
        data(): {
            cart_resource: CartResource,
        } { return {
            cart_resource: {
                id: -1,
                resource: -1,
                number: 0
            },
        }},
        methods: {
            view_item(name: string): void {
                window.location.href = `/view/${name}`
            },
            async listedprice(resource: Resource): Promise<number> {
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
            async user(new_user: User): Promise<void> {
                for (const resource of this.allResources) {
                    resource.price = await this.listedprice(resource)
                }
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
        height: 52rem;
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
        flex-direction: column;
        margin-right: 1rem;
        align-items: center;
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
</style>