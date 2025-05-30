<template>
    <div id="order" v-if="Object.keys(order).length > 0 && Object.keys(all_resources).length > 0">
        <div id="order-title">
            <div id="main">Order {{ order.id }}</div>
            <div id="back" @click="back">
                <i class="bi bi-arrow-left-circle-fill"></i> 
                <p>Orders</p>
            </div>
        </div>
        <div id="content">
        <div id="col1">
                <div id="border">
                    <div id="items">
                        <div id="header">
                            <div id="one">Items</div>
                            <div id="two">Total: {{ currency }}{{ total.toFixed(2) }} </div>
                        </div>
                        <div id="body">
                            <div class="resource" v-for="resource in order.resources" @click="(event) => view_resource(event, getResource(resource.resource).id)">
                                <div id="image">
                                    <img :src="`${url}/${getResource(resource.resource).image1}`">
                                    <div id="resnum">{{ resource.number }}</div>
                                </div>
                                <div class="name">
                                    <div>{{ getResource(resource.resource).name }}</div>
                                    <div>{{ currency }}{{ order.is_exchange ? parseFloat((0).toString()).toFixed(2) : (resource.number*parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                                    <p id="add-review" v-if="!(getResource(resource.resource).user === user.id) && can_review(getResource(resource.resource))">Add Review</p>
                                    <p id="add-review" v-if="!(getResource(resource.resource).user === user.id) && !can_review(getResource(resource.resource))">View Review</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="address">
                    <div class="title">Delivery Address</div>
                    <div id="address_lines">
                        <div>{{ user.address_line_one }}</div>
                        <div>{{ user.address_second_line }}</div>
                        <div>{{ user.city }}</div>
                        <div>{{ user.postcode }}</div>
                    </div>
                </div>
            </div>
            <div id="col2">
                <div id="payment">
                    <div class="title">Payment Method</div>
                    <div id="card_ending">
                        Card ending in 1234
                    </div>
                </div>
                <div id="number">
                    <div class="title">Phone Number</div>
                    <div id="user_number">
                        <div>{{ user.phone_number }}</div>
                    </div>
                </div>
                <div id="number">
                    <div class="title">Status</div>
                    <div id="user_number">
                        <select @input="update_status" v-if="(mode==='seller') && (order.status !== 'Cancelled') && (order.status !== 'Return Received') && (order.status !== 'Refunded') && (order.status !== 'Complete')" id='order-status' v-model="status">
                            <option style="display: none;" value="Placed" disabled>Placed</option>
                            <option v-if="(order.status === 'Placed') || (order.status === 'Processing')" value="Processing">Processing</option>
                            <option v-if="(order.status === 'Processing') || (order.status === 'Placed') || (order.status === 'Dispatched')" value="Dispatched">Dispatched</option>
                            <option v-if="(order.status === 'Processing') || (order.status === 'Placed') || (order.status === 'Dispatched')" value="Complete">Complete</option>
                            <option v-if="(order.status === 'Return Started')" value="Return Started" disabled>Return Started</option>
                            <option v-if="(order.status === 'Return Started')" value="Return Received">Return Received</option>
                        </select>
                        <p v-else>{{ order.status }}</p>
                    </div>
                </div>
                <div id="number" v-if="(order.status !== 'Cancelled')">
                    <div class="title">{{ !order_complete ? 'Estimated' : ''}} Delivery Date</div>
                    <div id="user_number">
                        <p>{{ new Date(order_complete ? order.delivery_date : order.estimated_delivery_date).getDate() }} {{ new Date(order_complete ? order.delivery_date : order.estimated_delivery_date).toLocaleString('en-UK', {'month' : 'long'}) }}</p>
                    </div>
                </div>
                <div id="buttons">
                    <button :disabled="making_change" v-if="(mode == 'buyer') && returnable && order.status === 'Complete'" @click="view_return(order)">Start Return</button>
                    <button :disabled="making_change" v-if="returnable && order.status === 'Return Started'" @click="view_return(order)">View Return</button>
                    <button :disabled="making_change" id="message_seller" v-if="(order.seller !== order.buyer) && returnable && order.status === 'Return Started'" @click="message_seller(mode === 'buyer' ? order.seller : order.buyer)">Message {{ mode === 'buyer' ? 'Seller' : 'Buyer' }}</button>
                    <button :disabled="making_change" id="cancel" v-if="returnable && order.status === 'Return Started' && mode === 'buyer'" @click="start_return(order)">Cancel Return</button>
                    <button :disabled="making_change" id="cancel" v-if="(mode == 'buyer') && order.status === 'Placed'" @click="cancel_order">Cancel</button>
                </div>
            </div>
        </div>
        <div v-if="error !== ''">
            <Error :message="error" @close-error="error=''" />
        </div>
        <div v-else>
            <Loading />
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Order, Resource, Review, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    import Error from '@/components/user experience/error/Error.vue';
    import Loading from '@/components/user experience/loading/Loading.vue';
    import { useURLStore } from '@/stores/url';
    export default defineComponent({
        components: { Error, Loading }, 
        data(): {
            mode: 'buyer' | 'seller',
            total: number,
            placed_order: boolean,
            making_change: boolean,
            error: string,
            status: 'Placed' | 'Processing' | 'Return Received' | 'Cancelled' | 'Dispatched' | 'Complete' | 'Return Started' | 'Refunded',
        } { return {
            status: 'Processing',
            mode: 'buyer',
            placed_order: false,
            making_change: false,
            total: 0,
            error: ''
        }},
        methods: {
            async update_status(): Promise<void> {
                // Update order status
                const status: HTMLSelectElement = document.getElementById('order-status') as HTMLSelectElement
                if (!status) {
                    this.error = 'Error updating status. Please try again'
                    return
                }
                if (this.order.status === status.value) return
                this.making_change = true
                let userResponse = await fetch(`${useURLStore().url}/api/user/${this.user.id}/order/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify({'id': this.order.id, status: status.value})
                })
                this.making_change = false
                if (!userResponse.ok) {
                    this.error = 'Error updating status. Please try again'
                    return
                }
                let user: User = await userResponse.json()
                useUserStore().saveUser(user)
                useUsersStore().updateUser(user)
            },
            message_seller(seller_id: number): void {
                // Allow user to message buyer/seller
                window.location.href = `/message/${this.user.id}/${seller_id}`
            },
            view_return(order: Order): void {
                const window_location: string[] = window.location.href.split('/')
                if (window_location.length === 5) {
                    window.location.href = `/${this.mode === 'buyer' ? 'return' : 'sold-return'}/${order.id}`
                } else {
                    window.location.href = `/${this.mode === 'buyer' ? 'return' : 'sold-return'}/${order.id}/${window_location[5]}/${window_location[6]}/${window_location[7]}`
                }
            },
            async start_return(order: Order): Promise<void> {
                // Cancelling return
                if (order.status === 'Return Started') {
                    this.making_change = true
                    let returnResponse = await fetch(`${useURLStore().url}/api/user/${this.user.id}/return/${this.order.id}/`, {
                        method: 'PUT',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                            'Content-Type' : 'application/json',
                        },
                        body: JSON.stringify({cancel: 'true', return_reason: this.order.return_reason, return_method: this.order.return_method})
                    })
                    this.making_change = false
                    if (!returnResponse.ok) {
                        this.error = 'Error cancelling return. Please try again.'
                        return
                    }
                    let data: {user: User, resources: Resource[]} = await returnResponse.json()
                    useUserStore().saveUser(data.user)
                    useUsersStore().updateUser(data.user)
                    useResourcesStore().saveResources(data.resources)
                    return
                }
            },
            view_resource(event: Event, id: number): void {
                // Allow user to view resource
                if (event.target && (event.target as HTMLDivElement).id === 'add-review') {
                    const resource: Resource = this.all_resources.find(resource => resource.id === id) as Resource
                    this.add_review(resource)
                    return
                }
                window.location.href = `/view/${id}`
            },
            add_review(resource: Resource): void {
                // Take user to add review page of resource
                if (this.can_review(resource)) {
                    window.location.href = `/view/${resource.id}/add-review`
                } else {
                    window.location.href = `/view/${resource.id}/review/${(resource.reviews.find(review => review.user === this.user.id && review.resource === resource.id) as Review).id}`
                }
            },
            can_review(resource: Resource): boolean {
                // Check if user has reviewed the resource before
                if (!resource.reviews || resource.reviews.length === 0) return true
                return resource.reviews.find(review => review.user === this.user.id && review.resource === resource.id) ? false : true
            },
            async cancel_order(): Promise<void> {
                // Allow user to cancel order
                this.making_change = true
                let userResponse = await fetch(`${useURLStore().url}/api/user/${this.user.id}/order/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(this.order.id)
                })
                this.making_change = false
                if (!userResponse.ok) {
                    this.error = 'Error cancelling order. Please try again'
                    return
                }
                let user: User = await userResponse.json()
                useUserStore().saveUser(user)
                useUsersStore().updateUser(user)
            },
            back(): void {
                // Allow user to go back to Orders page
                const window_location: string[] = window.location.href.split('/')
                if (window_location.length === 5) {
                    window.location.href = `/${this.mode === 'buyer' ? 'orders' : 'sold-orders'}`
                } else {
                    window.location.href = `/${this.mode === 'buyer' ? 'orders' : 'sold-orders'}/${this.order.id}/${window_location[5]}/${window_location[6]}/${window_location[7]}`
                }
            },
            getResource(resource_id: number): Resource {
                // Allow resource retrieval given an ID
                const resource: Resource | undefined = this.all_resources.find(resource => resource.id === resource_id)
                if (resource) return resource
                return {} as Resource
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
                return returnedPrice.new_price
            },
            get_total(): void {
                // Calculating return total
                this.total = 0
                if (!this.order || !this.order.resources || this.order.resources.length === 0 || this.order.is_exchange) return
                for (let item of this.order.resources) {
                    let resource = this.all_resources.find(resource => resource.id === item.resource)
                    if (resource) {
                        const price = parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))
                        this.total += item.number * price
                    }
                }
            }
        },
        computed: {
            order_complete(): boolean {
                if (this.order.status === 'Complete' || this.order.status === 'Refunded' || this.order.status === 'Return Received' || this.order.status === 'Return Started') {
                    return true
                }
                return false
            },
            url(): string {
                return useURLStore().url
            },
            returnable(): boolean {
                for(const resource of this.order.resources) {
                    const res = this.getResource(resource.resource)
                    // Can return 30 days within purchase date
                    const purchase_days: number = (new Date().getTime() - new Date(this.order.date).getTime())/1000/3600/24
                    if (res.allow_return && purchase_days <= 30) return true
                }
                return false
            },
            currency(): string {
                return this.user.currency === 'GBP' ? '£' : this.user.currency === 'USD' ? '$' : '€' 
            },
            users(): User[] {
                return useUsersStore().users
            },
            user(): User {
                return useUserStore().user
            },
            all_resources(): Resource[] {
                return useResourcesStore().resources
            },
            order(): Order {
                // Order to filter thtough depends on user mode
                if (!this.user || ((this.mode === 'buyer') && !this.user.placed_orders) || ((this.mode === 'seller') && !this.user.sold_orders)) return {} as Order
                const window_location: string[] = window.location.href.split('/')
                const id: number = parseInt(window_location[4])
                if (this.mode === 'buyer') {
                    const order: Order = this.user.placed_orders.find(order => order.id === id) || {} as Order
                    this.status = order.status
                    return order
                }
                const order: Order = this.user.sold_orders.find(order => order.id === id) || {} as Order
                this.status = order.status
                return order
            }
        },
        async mounted(): Promise<void> {
            if (Object.keys(this.user).length === 0) {
                // Return unauthorised user home
                window.location.href = '/'
                return
            }
            for (const resource of useResourcesStore().resources) {
                resource.price = await this.listedprice(resource)
            }
            const window_location: string[] = window.location.href.split('/')
            if (window_location.includes('sold-order')) {
                this.mode = 'seller'
            }
            this.placed_order = false
            this.get_total()
        },
        watch: {
            async all_resources(): Promise<void> {
                for (const resource of useResourcesStore().resources) {
                    resource.price = await this.listedprice(resource)
                }
                this.get_total()
            },
            async user(): Promise<void> {
                for (const resource of useResourcesStore().resources) {
                    resource.price = await this.listedprice(resource)
                }
                this.get_total()
            },
        },
    })
</script>

<style scoped>
    #order {
        margin-left: 2rem;
        margin-right: 2rem;
        margin-left: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 1rem;
    }

    #number_container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
    }

    #number_container input {
        width: 7rem;
        border-radius: 0.5rem;
    }

    .edit-buttons {
        display: flex;
        gap: 0.5rem;
    }

    #order-title {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        display: flex;
    }

    #order-title #main {
        font-weight: bold;
        font-size: 1.5rem;
    }

    div, button {
        font-size: 1.1rem;
    }

    #border {
        border: 0.1rem solid #0DCAF0;
        border-radius: 0.8rem;
        padding: 1rem;
    }

    #body {
        height: 25rem;
        overflow-y: auto;
        display: flex;
        padding-right: 2rem;
        flex-direction: column;
        gap: 1rem;
    }

    img {
        width: 8rem;
        height: 8rem;
        object-fit: contain;
    }

    .resource {
        display: flex;
        padding: 0.4rem;
        align-items: center;
        gap: 2rem;
    }

    .resource:hover {
        background-color: lightgray;
        cursor: pointer;
        border-radius: 0.5rem;
    }

    #dark .resource:hover {
        background-color: #595959;
        cursor: pointer;
        border-radius: 0.5rem;
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

    button:hover {
        cursor: pointer;
        background-color: darkgray;
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
        position: absolute;
        border-radius: 0.5rem;
        padding: 0.5rem;
        min-width: 1rem;
        border: 0.1rem solid black;
        background-color: white;
        left: 5.8rem;
        top: 0rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #dark #resnum {
        color: black;
    }

    .name {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #image {
        position: relative;
    }

    #content { 
        display: flex;
        gap: 8rem;
    }

    #add-review {
        color: #789ECA;
    }

    #add-review:hover {
        text-decoration: underline;
        cursor: pointer;
    }

    #dark #add-review {
        color: rgb(206, 206, 206);
    }

    #col1, #col2 {
        display: flex;
        flex-direction: column;
        gap: 3rem;
    }

    #dark select {
        background-color: transparent !important;
        color: white;
    }

    #dark option {
        color: black;
    }

    #payment {
        display: fl;
    }

    #user_number select {
        border: none;
        font-size: 1.1rem;
        width: 100%;
    }

    #user_number p {
        font-size: 1.1rem;
    }

    #card_ending, #address_lines, #user_number {
        border: 0.1rem solid #0DCAF0;
        padding: 1rem;
        border-radius: 0.8rem;
    }

    #header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    #header div, .title {
        font-size: 1.3rem;
    }

    #number, #payment, #address {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .change_text { 
        color: rgb(144, 171, 253);
    }

    #dark .change_text {
        color: rgb(255, 255, 255);
    }

    .change_text:hover { 
        text-decoration: underline;
        cursor: pointer;
    }

    #address_lines {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
    }

    #dark #border, #dark #user_number, #dark #address_lines, #dark #card_ending {
        border: 0.1rem solid white;
    }

    #border, #user_number, #address_lines, #card_ending {
        width: 22rem;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    #buttons {
        display: flex;
        gap: 1rem;
    }

    #buttons button {
        border-radius: 0.4rem;
        border: none;
        padding: 0.5rem;
        background-color: #0DCAF0;
    }

    #buttons button:hover {
        background-color: #1e7587;
    }

    #dark #buttons button {
        color: black;
        background-color: white ;
    }

    #dark #buttons button:hover {
        background-color: darkgray;
    }

    #back {
        display: flex;
        align-items: center;
        gap: 1rem;
        position: absolute;
        left: 2rem;
    }

    #back:hover {
        cursor: pointer;
    }

    #back i:hover {
        color: rgb(80, 80, 80);
    }

    #dark #back i:hover {
        color: rgb(206, 206, 206);
    }

    #dark #order {
        color: white;
    }

    #back p:hover {
        text-decoration: underline;
    }

    #back i, #back p {
        font-size: 1.2rem;
    }

    #number_container button {
        border: none;
        color: white;
        border-radius: 0.2rem;
        width: 1.5rem;
        height: 1.5rem;
    }

    #address_lines button {
        border: none;
        color: white;
        border-radius: 0.2rem;
        width: 1.5rem;
        height: 1.5rem;
    }

    .header {
        margin-top: 0.5rem;
    }

    #address_lines input {
        border-radius: 0.5rem;
    }

    #cancel {
        background-color: red !important;
        color: white;
    }

    #dark #cancel {
        color: white !important;
    }

    #cancel:hover {
        background-color: darkred !important;
    }

    button:disabled, button:disabled:hover, #cancel:disabled, #cancel:disabled:hover {
        background-color: darkgray !important;
        cursor: not-allowed !important;
        color: white !important;
    }

    /* Responsive Design */
    @media (max-width: 1002px) {
        #content { 
            flex-direction: column;
            gap: 4rem;
            overflow-y: auto;
            padding-right: 1rem;
            max-height: 86vh;
            margin-top: 0rem;
        }

        #checkout {
            gap: 1rem;
        }

        #buttons {
            margin: auto;
        }
    }

    @media (max-height: 986px) {
        #content {
            height: 85vh;
        }
    }

    @media (max-height: 958px) {
        #content {
            height: 83vh;
        }
    }

    @media (max-height: 772px) {
        #content {
            height: 80vh;
        }
    }
</style>