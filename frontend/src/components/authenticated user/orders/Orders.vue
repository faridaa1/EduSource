<template>
    <div id="orders-view" v-if="user && user.placed_orders">
        <div id="header">
            <p>My Orders</p>
            <div id="order_orders">
                <label>Order By</label>
                <select v-model="order">
                    <option value="new">Newest</option>
                    <option value="old">Oldest</option>
                </select>
            </div>
        </div>
        <div id="resources">
            <div id="empty-message" v-if="user.placed_orders.length === 0">No orders yet</div>
            <div class="orders-item" v-for="order in user.placed_orders.sort((a,b) => {return order === 'new' ? b.id-a.id : a.id-b.id})">
                <div class="item-one">
                    <div class="item-image">
                        <img @click="view_item(order.id)" :src="`http://localhost:8000${(allResources.find(res => res.id === order.resources[0].resource) as Resource)?.image1}`" alt="">
                        <p id="number_of_items">{{ order_total(order) }}</p>
                    </div>
                    <div class="details">
                        <p>Order Number {{ order.id }}</p>
                        <p id="status"> Status: {{ order.status }}</p>
                        <p id="view-details" @click="view_item(order.id)">View Details</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Order, Resource, User, } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    export default defineComponent({
        data(): {
            order: 'new' | 'old'
        } { return {
            order: 'new'
        }},
        methods: {
            view_item(id: number): void {
                window.location.href = `/order/${id}`
            },
            order_total(order: Order): number {
                let total = 0
                for (let resource of order.resources) {
                    total += resource.number
                }
                return total
            }
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
            order(): void {
                const div: HTMLDivElement = document.getElementById('resources') as HTMLDivElement
                div.scrollTo({top: 0})
            }
        }
    })
</script>

<style scoped>
    #orders-view {
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

    #resources {
        display: flex;
        flex-direction: column;
        gap: 3rem;
        overflow-y: scroll;
        height: 51.7rem;
    }

    .orders-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    img {
        width: 9rem;
    }

    img:hover {
        cursor: pointer;
    }

    .item-image {
        position: relative;
    }

    .item-one {
        display: flex;
        gap: 3rem;
        align-items: center;
    }

    .details {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #view-details {
        color: #789ECA;
    }

    #view-details:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    #empty-message {
        text-align: center;
        font-size: 1.1rem;
    }

    #status {
        color: darkgray;
    }

    #dark #status {
        color: rgb(49, 49, 49);
    }

    #number_of_items {
        position: absolute;
        border-radius: 0.5rem;
        padding: 0.5rem;
        min-width: 1rem;
        border: 0.1rem solid black;
        background-color: white;
        left: 6.5rem;
        top: 6rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #order_orders {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    select {
        border-radius: 0.5rem;
    }

    #dark #orders-view, #dark #view-details {
        color: white;
    }

    #dark #number_of_items {
        color: black;
    }

    #dark #status {
        color: rgb(206, 206, 206);
    }

    /* Responsive Design */
    @media (max-width: 500px) {
        img {
            width: 7rem;
        }

        #number_of_items {
            left: 5rem;
            top: 4rem;
        }

        #resources {
            height: 50rem;
        }
    }
</style>