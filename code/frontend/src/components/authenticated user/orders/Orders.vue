<template>
    <div id="orders-view" v-if="(user && (mode === 'buyer') &&  user.placed_orders) || (user && (mode === 'seller') &&  user.sold_orders)">
        <div id="header">
            <div id="header1">
                <p>{{ mode === 'buyer' ? user.mode === 'buyer' ? 'My' : 'Placed' : 'Sold' }} Orders</p>
            <div id="search">
                <input @input="clear_error" v-model="search" id="order-search" type="text" @click="remove_focus" placeholder="Enter resource name">
                <i id="x" @click="handle_x_click" :class="search.trim() !== '' ? 'bi bi-x' : ''"></i>
                <i id="look" @click="search_orders" class="bi bi-search"></i>
            </div>
            </div>
            <div id="order_orders">
                <div  v-if="filtered_orders.length > 0">
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
                        <option value="Dispatched">Dispatched</option>
                        <option value="Complete">Complete</option>
                        <option value="Return Started">Return Started</option>
                        <option value="Return Received">Return Received</option>
                        <option value="Refunded">Refunded</option>
                        <option value="Cancelled">Cancelled</option>
                    </select>
                </div>
            </div>
        </div>
        <div id="resources">
            <div v-if="!searching" class="orders-item" @click="view_item(order.id)" v-for="order in filtered_orders">
                <div class="item-one" v-if="order.resources[0]">
                    <div class="item-image">
                        <img v-if="order.resources[0]" :src="`${url}${(allResources.find(res => res.id === order.resources[0].resource) as Resource)?.image1}`">
                        <img v-else>
                        <p id="number_of_items">{{ order_total(order) }}</p>
                    </div>
                    <div class="details">
                        <p :id="order.id.toString()">Order Number {{ order.id }}</p>
                        <p id="status"> Total: {{ currency }}{{ order_total_number(order).toFixed(2) }}</p>
                        <p id="status"> Status: {{ order.status }}</p>
                        <p id="view-details">View Details</p>
                    </div>
                </div>
            </div>
            <div v-if="searching">
                <Loading />
            </div>
            <div id="no-orders" v-if="filtered_orders.length === 0">
                No orders found
            </div>
        </div>
        <div id="pagination" v-if="filtered_orders.length > 0">
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
                <button :disabled="current_page===1" @click="update_page(-1)"><i class="bi bi-arrow-left"></i></button>
                <button :disabled="current_page===total_pages" @click="update_page(1)"><i class="bi bi-arrow-right"></i></button>
            </div>
        </div>
    </div>
    <div v-else>
        <Loading />
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Order, Resource, User, } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import Loading from '@/components/user experience/loading/Loading.vue';
    import { useURLStore } from '@/stores/url';
    export default defineComponent({
        components: { Loading },
        data(): {
            mode: 'buyer' | 'seller',
            mounted: boolean,
            order: 'new' | 'old' | string
            status: 'all' | 'Placed' | 'Processing' | 'Return Received' | 'Cancelled' | 'Dispatched' | 'Complete' | 'Return Started' | 'Refunded',
            current_page: number,
            total_pages: number,
            search: string,
            searching: boolean,
            searched_items: Order[]
        } { return {
            mode: 'buyer',
            mounted: false,
            order: 'new',
            search: '',
            status: 'all',
            total_pages: 1,
            current_page: 1,
            searching: false,
            searched_items: []
        }},
        methods: {
            update_page(new_page: number): void {
                // Updating page
                this.current_page = this.current_page + new_page
            },
            handle_x_click(): void {
                // Clear search value
                const input: HTMLInputElement = document.getElementById('order-search') as HTMLInputElement
                if (!input) return
                this.search = ''
                input.focus()
                this.searching = false
            },
            clear_error(): void {
                // Clear error messages
                const input: HTMLInputElement = document.getElementById('order-search') as HTMLInputElement
                if (!input || this.searching) return
                input.setCustomValidity('')
                input.reportValidity()
            },
            async search_orders(): Promise<void> {
                // Perform semantic search on orders
                const input: HTMLInputElement = document.getElementById('order-search') as HTMLInputElement
                if (!input || this.searching) return
                if (this.search.trim() === '') {
                    input.setCustomValidity('Enter a value')
                    input.reportValidity()
                    return
                } else {
                    this.clear_error()
                }
                this.searching = true
                const searchResults: Response = await fetch(`${useURLStore().url}/api/semantic-search-orders/${this.user.id}/${this.search}/buyer/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type' : 'application/json',
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(this.filtered_orders)
                })
                if (!searchResults.ok) {
                    return
                } else {
                    const matches: number[] = await searchResults.json()
                    this.searched_items = this.mode === 'buyer' ? this.user.placed_orders.filter(order => matches.includes(order.id)) : this.user.sold_orders.filter(order => matches.includes(order.id))
                    this.searching = false
                    if (matches.length === 0) {
                        input.setCustomValidity('Resource not found')
                        input.reportValidity()
                    }
                }
            },
            remove_focus(): void {
                // Remove focus on input element
                const div: HTMLInputElement = document.getElementById('search') as HTMLInputElement
                if (!div) return
                div.blur()
            },
            view_item(id: number): void {
                // View order
                window.location.href = `/${this.mode === 'buyer' ? 'order' : 'sold-order'}/${id}/${this.status}/${this.order}/${this.current_page}`
            },
            order_total(order: Order): number {
                // Calculate total number of items
                let total = 0
                for (let resource of order.resources) {
                    total += resource.number
                }
                return total
            },
            order_total_number(order: Order): number {
                // Calculate order total
                if (order.is_exchange) return 0
                let total = 0
                for (let resource of order.resources) {
                    const res: Resource | undefined = this.allResources.find(res => res.id === resource.resource)
                    if (!res) return 0
                    total += (resource.number * res.price)
                }
                return total
            },
            async listedprice(resource: Resource): Promise<number> {
                // Performing currency conversion
                if (resource === undefined) return 0
                let convertedPrice: Response = await fetch(`${useURLStore().url}/api/currency-conversion/${resource.id}/${this.user.currency}/${resource.price_currency}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    }
                })
                if (!convertedPrice.ok) return resource.price
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return parseFloat(returnedPrice.new_price.toString().replace('£', '').replace('$','').replace('€',''))
            }
        },
        computed: {
            currency(): string {
                return this.user.currency === 'GBP' ? '£' : this.user.currency === 'USD' ? '$' : '€' 
            },
            url(): string {
                return useURLStore().url
            },
            filtered_orders(): Order[] {
                // Filter orders
                let temp_orders;
                if (this.mode === 'buyer') {
                    temp_orders = this.searched_items.length > 0 ? this.searched_items.filter(order => (this.status === 'all' && order.status !== 'Cancelled') || order.status === this.status) : this.user.placed_orders.filter(order => (this.status === 'all' && order.status !== 'Cancelled') || order.status === this.status)
                } else {
                    temp_orders = this.searched_items.length > 0 ? this.searched_items.filter(order => (this.status === 'all' && order.status !== 'Cancelled') || order.status === this.status) : this.user.sold_orders.filter(order => (this.status === 'all' && order.status !== 'Cancelled') || order.status === this.status)
                }
                this.total_pages = Math.ceil(temp_orders.length/10)
                return temp_orders.sort((a,b) => {return this.order === 'new' ? b.id-a.id : a.id-b.id})
                .filter((_, index) => ((index) < (this.current_page*10)) && ((index+1) > ((this.current_page-1)*10)))
            },
            user(): User {
                return useUserStore().user
            },
            allResources(): Resource[] {
                return useResourcesStore().resources
            },
        },
        watch: {
            '$route.path'(): void {
                if (window.location.href.split('/').includes('sold-orders')) {
                    this.mode = 'seller'
                } else {
                    this.mode = 'buyer'
                }
            },
            search(): void {
                if (this.search.trim() === '') return
                this.searching = false
            },
            order(): void {
                // Scroll to top of first page each time order is updated
                const div: HTMLDivElement = document.getElementById('resources') as HTMLDivElement
                if (!div) return
                div.scrollTo({top: 0})
                if ((window.location.href.split('/').length > 4) && !this.mounted) return
                this.current_page = 1
            },
            status(): void {
                // Scroll to top of first page each time order status is updated
                const div: HTMLDivElement = document.getElementById('resources') as HTMLDivElement
                if (!div) return
                div.scrollTo({top: 0})
                if ((window.location.href.split('/').length > 4) && !this.mounted) return
                this.current_page = 1
            }
        },
        async mounted(): Promise<void> {
            for (const resource of this.allResources) {
                resource.price = await this.listedprice(resource)
            }
            if (Object.keys(this.user).length === 0) {
                // Return unauthorised user home
                window.location.href = '/'
                return
            }
            this.total_pages = this.mode === 'buyer' ? Math.ceil(this.user.placed_orders.length/10) : Math.ceil(this.user.sold_orders.length/10)
            document.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' && (event.target as HTMLInputElement).id === 'order-search') {
                    // Keyboard shortut for searching
                    this.search_orders()
                }
            })
            const window_location: string[] = window.location.href.split('/')
            if (window_location.includes('sold-orders')) {
                this.mode = 'seller'
            } else {
                this.mode = 'buyer'
            }
            if (window_location.length > 4) {
                // Reset search conditions (e.g. search filter and page)
                this.status = window_location[5].replace('%20', ' ') as 'all' | 'Placed' | 'Processing' | 'Return Received' | 'Cancelled' | 'Dispatched' | 'Complete' | 'Return Started' | 'Refunded'
                this.order = window_location[6]
                this.current_page = parseInt(window_location[7])
                nextTick(() => {
                    const div: HTMLParagraphElement = document.getElementById(window_location[4]) as HTMLParagraphElement
                    if (div) {
                        div.scrollIntoView()
                        // this.mounted = true
                    }
                })
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

    #order-search {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    #header {
        display: flex;
        justify-content: space-between;
    }

    #header1 {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #look {
        background-color: #d9d9d9;
        color: black;
        border-top-right-radius: 0.5rem;
        border-bottom-right-radius: 0.5rem;
        padding: 0.5rem;
    }

    #look:hover {
        background-color: darkgray;
        cursor: pointer;
    }

    #search {
        display: flex;
        align-items: center;
    }

    input {
        width: 30rem !important;
        padding: 0.5rem !important;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
    }

    input:focus {
        background-color: #d9d9d9 !important;
        border: none !important;
        outline: none;
    }

    #x {
        color: red;
        background-color: #d9d9d9;
        font-size: 1.48rem;
        width: 1.3rem;
        height: 2.2rem;
        display: flex;
        padding-right: 0.2rem;
        align-items: center;
        justify-content: center;
    }

    #x:hover {
        cursor: pointer;
        color: lightcoral;
    }

    #header p {
        font-size: 1.5rem;
    }

    #resources {
        display: flex;
        flex-direction: column;
        gap: 3rem;
        overflow-y: auto;
        height: 76vh;
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
        height: 9rem;
        object-fit: contain;
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
        left: 9rem;
        top: 0.3rem;
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
        font-size: 1.1rem;
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
        padding: 0.45rem;
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
            height: 7rem;
        }

        #number_of_items {
            left: 7rem;
        }

        #resources {
            height: 76vh;
        }
    }

    @media (max-width: 859px) {
        input {
            width: 20rem !important;
        }
    }

    @media (max-width: 686px) {
        input {
            width: 15rem !important;
        }
    }

    @media (max-width: 611px) {
        #search {
            margin-top: 5rem;
            position: absolute;
        }

        input {
            width: 16rem !important;
        }

        #header1 {
            margin-bottom: 6rem;
        }

        #resources {
            height: 71vh;
        }
    }

    @media (max-height: 959px) {
        #resources {
            height: 70vh;
        }
    }

    @media (max-height: 887px) {
        #resources {
            height: 67vh;
        }
    }

    @media (max-height: 816px) {
        #resources {
            height: 65vh;
        }
    }

    @media (max-height: 753px) {
        #resources {
            height: 62vh;
        }
    }

    @media (max-height: 613px) {
        #resources {
            height: 60vh;
        }
    }
</style>