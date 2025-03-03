<template>
    <div id="orders-view" v-if="user && user.placed_orders">
        <div id="header">
            <p>My Orders</p>
            <div id="order_orders">
                <div>
                    <label>Order By</label>
                    <select v-model="order">
                        <option value="new">Newest</option>
                        <option value="old">Oldest</option>
                    </select>
                    </div>
                <div>
                    <label>Status</label>
                    <select v-model="status">
                        <option value="all">All</option>
                        <option value="Placed">Placed</option>
                        <option value="Processing">Processing</option>
                        <option value="Cancelled">Cancelled</option>
                        <option value="Refund Rejected">Refund Rejected</option>
                        <option value="Dispatched">Dispatched</option>
                        <option value="Complete">Complete</option>
                        <option value="Being Returned">Being Returned</option>
                        <option value="Refunded">Refunded</option>
                    </select>
                </div>
            </div>
        </div>
        <div id="resources">
            <div id="empty-message" v-if="user.placed_orders.length === 0">No orders yet</div>
            <div class="orders-item"  @click="view_item(order.id)" v-for="order in user.placed_orders.filter((order, index) => (((index) < (current_page*10)) && ((index+1) > ((current_page-1)*10))) && (status === 'all' || order.status === status)).sort((a,b) => {return order === 'new' ? b.id-a.id : a.id-b.id})">
                <div class="item-one">
                    <div class="item-image">
                        <img :src="`http://localhost:8000${(allResources.find(res => res.id === order.resources[0].resource) as Resource)?.image1}`" alt="">
                        <p id="number_of_items">{{ order_total(order) }}</p>
                    </div>
                    <div class="details">
                        <p>Order Number {{ order.id }}</p>
                        <p id="status"> Status: {{ order.status }}</p>
                        <p id="view-details">View Details</p>
                    </div>
                </div>
            </div>
            <div v-if="user.placed_orders.sort((a,b) => {return order === 'new' ? b.id-a.id : a.id-b.id}).filter(order => status === 'all' || order.status === status).length === 0">
                <p id="no-orders">No orders to show</p>
            </div>
        </div>
        <div id="pagination">
            <div>
                <p>Page</p>
            </div>
            <div id="of">
                <select v-model="current_page">
                    <option :value="page" v-for="page in total_pages">{{ page }}</option>
                </select>
                <p>of {{ total_pages }}</p>
            </div>
            <div id="pagination-buttons">
                <button :disabled="current_page===1" @click="current_page=current_page-1"><i class="bi bi-arrow-left"></i></button>
                <button :disabled="current_page===total_pages" @click="current_page=current_page+1"><i class="bi bi-arrow-right"></i></button>
            </div>
        </div>
    </div>
    <div v-else>
        <Loading />
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Order, Resource, User, } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import Loading from '@/components/user experience/loading/Loading.vue';
    export default defineComponent({
        components: { Loading },
        data(): {
            order: 'new' | 'old'
            status: 'all' | 'Placed' | 'Processing' | 'Refund Rejected' | 'Dispatched' 
                    | 'Cancelled' | 'Complete' | 'Being Returned' | 'Refunded'
            current_page: number,
            total_pages: number,
        } { return {
            order: 'new',
            status: 'all',
            total_pages: 1,
            current_page: 1,
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
        },
        watch: {
            order(): void {
                const div: HTMLDivElement = document.getElementById('resources') as HTMLDivElement
                if (!div) return
                div.scrollTo({top: 0})
            },
            status(): void {
                const div: HTMLDivElement = document.getElementById('resources') as HTMLDivElement
                if (!div) return
                div.scrollTo({top: 0})
            }
        },
        mounted(): void {
            this.total_pages = Math.ceil(this.user.placed_orders.length/10)
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
        height: 50rem;
    }

    .orders-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.4rem;
        position: relative;
    }

    .orders-item:hover {
        cursor: pointer;
        background-color: lightgray;
        border-radius: 0.5rem;
    }

    #dark .orders-item:hover {
        background-color: #696969;
    }

    img {
        width: 9rem;
    }

    img:hover {
        cursor: pointer;
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

    #order_orders select {
        width: 10rem;
        text-align: center;
        padding: 0.2rem;
    }

    select {
        padding: 0.2rem;
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
        top: 4rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #order_orders {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #order_orders div {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    #order_orders label {
        width: 4.2rem;
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

    #no-orders {
        text-align: center;
    }

    #pagination {
        display: flex;
        align-items: center;
        gap: 1rem;
        justify-content: center;
    }

    #pagination p {
        font-size: 1.3rem;
    }

    #pagination select, #pagination i {
        font-size: 1rem;
    }

    #pagination #pagination-buttons {
        display: flex;
        gap: 1.5rem;
        margin-left: 1rem;
    }

    #pagination #pagination-buttons button {
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem;
        background-color: #0DCAF0;
        color: white;
    }

    #dark #pagination #pagination-buttons button {
        background-color: white;
        color: black;
    }

    #dark #pagination #pagination-buttons button:hover {
        background-color: darkgray;
    }

    #pagination #pagination-buttons button:hover {
        cursor: pointer;
        background-color: #15acca;
    }

    #pagination #pagination-buttons button:disabled, #dark #pagination #pagination-buttons button:disabled {
        background-color: lightgrey;
    }

    #pagination #pagination-buttons button:disabled:hover {
        cursor: not-allowed;
    }

    #of {
        display: flex;
        align-items: center;
        gap: 1rem;
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