<template>
    <div id="cart-view" v-if="user && user.cart">
        <div id="header">
            <p>My Cart</p>
            <p id="total">Total: {{ user.cart.total }}</p>
        </div>
        <div id="resources">
            <div class="cart-item" v-for="resource in user.cart.resources">
                {{ resource }}
                <div class="item-one">
                    <div class="item-image">
                        <img :src="`http://localhost:8000${(allResources.find(res => res.id === resource.resource) as Resource).image1}`" alt="">
                    </div>
                    <div class="details">
                        <p>{{ (allResources.find(res => res.id === resource.resource) as Resource).name }}</p>
                        <p>{{ (allResources.find(res => res.id === resource.resource) as Resource).price }}</p>
                        <p id="view-details">View Details</p>
                    </div>
                </div>
                <div class="item-two">

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

</style>