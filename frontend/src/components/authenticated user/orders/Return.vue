<template>
    <div id="order" v-if="Object.keys(order).length > 0 && Object.keys(all_resources).length > 0">
        <div id="order-title">
            <div id="main">Order {{ order.id }}: Return</div>
            <div id="back" @click="back">
                <i class="bi bi-arrow-left-circle-fill"></i> 
                <p>Order</p>
            </div>
        </div>
        <div id="content">
            <div id="col1">
                <div id="border">
                    <div id="items">
                        <div id="header">
                            <div id="one">Returnable Items</div>
                            <div id="two">Refund: {{ currency }}{{ total.toFixed(2) }} </div>
                        </div>
                        <div id="body">
                            <div id="select_item_error" v-if="select_item_error !== ''">{{ select_item_error }}</div>
                            <div class="resource" v-for="resource in order.resources.filter(resource => getResource(resource.resource).allow_return)">
                                <div id="image">
                                    <img :src="`${url}/${getResource(resource.resource).image1}`">
                                    <div v-if="order.status === 'Complete'" id="resnum">{{ resource.number }}</div>
                                    <div v-else>{{ resource.number_for_return }}</div>
                                </div>
                                <div class="name">
                                    <div>{{ getResource(resource.resource).name }}</div>
                                    <div v-if="order.status !== 'Return Started'">{{ currency }}{{ order.is_exchange ? parseFloat((0).toString()).toFixed(2) : (parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                                    <div v-else>{{ currency }}{{ order.is_exchange ? parseFloat((0).toString()).toFixed(2) : (resource.number_for_return*parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                                    <div id="toggle" v-if="order.status !== 'Return Started'">
                                        <div id="resnum1">{{ resource.number_for_return }}</div>
                                        <div id=controls>
                                            <div id="plus" v-if="resource.number_for_return < resource.number" @click="return_item(resource.number_for_return+1, resource.id)">+</div>
                                            <hr v-if="resource.number_for_return > 0 && resource.number_for_return < resource.number">
                                            <div id="minus" v-if="resource.number_for_return > 0" :class="resource.number < getResource(resource.resource).stock ? '' : 'round-border'" @click="return_item(resource.number_for_return-1, resource.id)">-</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="payment">
                    <div class="title">Payment Method</div>
                    <div id="card_ending">
                        Card ending in 1234
                    </div>
                </div>
                <div id="number">
                    <div>Seller Phone Number</div>
                    <div id="user_number">
                        <div id="number_container">
                            <div><input id="number_input" type="text" v-model="phone_number" disabled="true"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="col2">
                <div id="number">
                    <div class="title">Status</div>
                    <div id="user_number">
                        <select @input="update_status" v-model="status" v-if="(mode==='seller') && (order.status === 'Return Started')" id='order-status'>
                            <option style="display: none;" value="Return Started">Return Started</option>
                            <option value="Return Received">Return Received</option>
                        </select>
                        <p v-else>{{ order.status }}</p>
                    </div>
                </div>
                <div id="address">
                    <div>Seller Address</div>
                    <div id="address_lines">
                        <div v-if="!changing_address">{{ mode === 'buyer' ? seller.address_line_one : user.address_line_one }}</div>
                        <div v-if="seller.address_second_line && !changing_address">{{ mode === 'buyer' ? seller.address_second_line : user.address_second_line }}</div>
                        <div v-if="!changing_address">{{ mode === 'buyer' ? seller.city : user.city }}</div>
                        <div v-if="!changing_address">{{ mode === 'buyer' ? seller.postcode : user.postcode }}</div>
                        <div v-if="changing_address" class="input">
                            <label>First Line</label>
                            <input id="address1" type="text" :value="user.address_line_one">
                        </div>
                        <div v-if="changing_address" class="input">
                            <label class="header">Second Line</label>
                            <input id="address2" type="text" :value="user.address_second_line">
                        </div>
                        <div v-if="changing_address" class="input">
                            <label class="header">City</label>
                            <input id="city" type="text" :value="user.city">
                        </div>
                        <div v-if="changing_address" class="input">
                            <label class="header">Postcode</label>
                            <input id="postcode" type="text" :value="user.postcode">
                        </div>
                    </div>
                </div>
                <div id="number">
                    <div class="title">Return Method</div>
                    <div id="user_number">
                        <select v-if="order.status === 'Complete'" v-model="return_method">
                            <option value="Delivery">Delivery</option>
                            <option value="Collection">Collection</option>
                        </select>
                        <div v-else>{{ order.return_method }}</div>
                    </div>
                </div>
                <div id="return_reason"  v-if="order.status !== 'Return Started' || (order.status === 'Return Started' && order.return_reason !== '')">
                    <div class="title">Return Reason (optional)</div>
                    <div id="user_number">
                        <textarea :disabled="order.status === 'Return Started'" v-model="return_reason" placeholder="Enter reason for return"></textarea>
                    </div>
                </div>
                <div id="buttons">
                    <button :disabled="making_change" v-if="(mode == 'buyer') && order.status === 'Complete'" @click="submit_return(order, false)">Submit</button>
                    <button :disabled="making_change" id="cancel" v-if="(mode == 'buyer') && order.status === 'Return Started'" @click="submit_return(order, true)">Cancel</button>
                    <button :disabled="making_change" id="message_seller" v-if="(order.seller !== order.buyer) && order.status === 'Return Started'" @click="message_seller(mode === 'buyer' ? order.seller : order.buyer)">Message {{ mode === 'buyer' ? 'Seller' : 'Buyer' }}</button>
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
    import { defineComponent, nextTick } from 'vue';
    import type { Order, OrderResource, Resource, User } from '@/types';
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
            return_reason: string,
            making_change: boolean,
            placed_order: boolean,
            status: 'Placed' | 'Processing' | 'Return Received' | 'Cancelled' | 'Dispatched' | 'Complete' | 'Return Started' | 'Refunded',
            error: string,
            phone_number: string,
            changing_number: boolean,
            changing_address: boolean,
            return_method: 'Delivery' | 'Collection',
            select_item_error: string,
        } { return {
            mode: 'buyer',
            return_method: 'Delivery',
            placed_order: false,
            status: 'Return Started',
            select_item_error: '',
            phone_number: '',
            return_reason: '',
            total: 0,
            making_change: false,
            error: '',
            changing_number: false,
            changing_address: false,
        }},
        methods: {
            async update_status(): Promise<void> {
                // Updating order status
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
                if (!userResponse.ok) {
                    this.making_change = false
                    this.error = 'Error updating status. Please try again'
                    return
                } else {
                    this.making_change = false
                    let user: User = await userResponse.json()
                    useUserStore().saveUser(user)
                    useUsersStore().updateUser(user)
                }
            },
            message_seller(seller_id: number): void {
                // Take user to page to message other user
                window.location.href = `/message/${this.user.id}/${seller_id}`
            },
            async return_item(return_number: number, resource_id: number): Promise<void> {
                this.making_change = true
                let returnItemResponse = await fetch(`${useURLStore().url}/api/user/${this.user.id}/return/${this.order.id}/${resource_id}/`, {
                    // Updating number of items for return
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(return_number)
                })
                if (!returnItemResponse.ok) {
                    this.making_change = false
                    this.error = 'Error updating number of items. Please try again.'
                    return
                }
                if (return_number > 0) {
                    this.select_item_error = ''
                }
                this.making_change = false
                let data: {user: User, resource: Resource} = await returnItemResponse.json()
                useUserStore().saveUser(data.user)
                useUsersStore().updateUser(data.user)
                useResourcesStore().updateResource(data.resource)
            },
            async submit_return(order: Order, cancel: boolean): Promise<void> {
                // Submitting or cancelling return
                let selected_item = false
                for (const order_resource of order.resources) {
                    if (order_resource.number_for_return > 0) {
                        selected_item = true
                        break
                    }
                }
                if (!selected_item) {
                    this.select_item_error = 'Select at least one item to be returned.'
                    return
                }
                this.making_change = true
                let returnResponse = await fetch(`${useURLStore().url}/api/user/${this.user.id}/return/${this.order.id}/`, {
                        method: 'PUT',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                            'Content-Type' : 'application/json',
                        },
                        body: JSON.stringify({cancel: cancel ? 'true' : 'false', return_reason: this.return_reason, return_method: this.return_method})
                    })
                if (!returnResponse.ok) {
                    this.making_change = false
                    this.error = 'Error updating return status. Please try again.'
                    return
                }
                this.making_change = false
                let data: {user: User, resources: Resource[]} = await returnResponse.json()
                useUserStore().saveUser(data.user)
                useUsersStore().updateUser(data.user)
                useResourcesStore().saveResources(data.resources)
                const window_location: string[] = window.location.href.split('/')
                if (window_location.length <= 5) {
                    window.location.href = `/${this.mode === 'buyer' ? 'order' : 'sold-order'}/${window_location[4]}`
                    return
                }
                window.location.href = `/${this.mode === 'buyer' ? 'order' : 'sold-order'}/${window_location[4]}/${this.order.status}/${window_location[6]}/${window_location[7]}`
            },
            back(): void {
                // Return to order page
                const window_location: string[] = window.location.href.split('/')
                if (window_location.length <= 5) {
                    window.location.href = `/${this.mode === 'buyer' ? 'order' : 'sold-order'}/${window_location[4]}`
                    return
                }
                window.location.href = `/${this.mode === 'buyer' ? 'order' : 'sold-order'}/${window_location[4]}/${this.order.status}/${window_location[6]}/${window_location[7]}`
            },
            getResource(resource_id: number): Resource {
                // Return resource for given id
                const resource: Resource | undefined = useResourcesStore().resources.find(resource => resource.id === resource_id)
                if (resource) return resource
                return {} as Resource
            },
            async listedprice(resource: Resource): Promise<number> {
                // Performing currency conversion
                if (resource === undefined) return 0
                this.making_change = true
                let convertedPrice: Response = await fetch(`${useURLStore().url}/api/currency-conversion/${resource.id}/${this.user.currency}/${resource.price_currency}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    }
                })
                if (!convertedPrice.ok) {
                    this.making_change = false
                    return resource.price
                } else {
                    this.making_change = false
                    let returnedPrice: {new_price: number} = await convertedPrice.json()
                    return returnedPrice.new_price
                }
            },
            get_total(): void {
                // Retrieving return total
                this.total = 0
                if (!this.order || !this.order.resources || this.order.resources.length === 0 || this.order.is_exchange) return
                for (let item of this.order.resources) {
                    let resource = this.all_resources.find(resource => resource.id === item.resource && resource.allow_return)
                    if (resource) {
                        const order_resource: OrderResource | undefined = this.order.resources.find(order_resource => order_resource.resource === resource.id)
                        if (!order_resource) return
                        const price = parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))
                        this.total += order_resource.number_for_return * price
                    }
                }
            },
            returnable(resourceID: number): boolean {
                // Determine if item can be returned
                return this.all_resources.find(resource => resource.id === resourceID)?.allow_return || false
            },
        },
        computed: {
            url(): string {
                return useURLStore().url
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
            seller(): User {
                return useUsersStore().users.find(user => user.id === this.order.seller) || {} as User
            },
            all_resources(): Resource[] {
                return useResourcesStore().resources
            },
            order(): Order {
                // Orders to look thorugh varies based on whether buyer or seller is viewing
                const window_location: string[] = window.location.href.split('/')
                const id: number = parseInt(window_location[4])
                if (!this.user || ((this.mode === 'buyer') && ((!this.user.placed_orders) || (!this.user.placed_orders.find(order => order.id === id)))) || ((this.mode === 'seller') && ((!this.user.sold_orders) || (!this.user.sold_orders.find(order => order.id === id))))) return {} as Order
                let order: Order
                if (this.mode === 'buyer') {
                    order = this.user.placed_orders.find(order => order.id === id) || {} as Order
                    this.status = order.status
                } else {
                    order = this.user.sold_orders.find(order => order.id === id) || {} as Order
                    this.status = order.status
                }
                return order
            }
        },
        async mounted(): Promise<void> {
            if (Object.keys(this.user).length === 0) {
                // Return unauthorised user home
                window.location.href = '/'
                return
            }
            const window_location: string[] = window.location.href.split('/')
            if (window_location.includes('sold-return')) {
                this.mode = 'seller'
            }
            for (const resource of useResourcesStore().resources) {
                // Perform currency conversion
                resource.price = await this.listedprice(resource)
            }
            this.placed_order = false
            this.get_total()
            // Initialising variables
            this.phone_number = this.seller.phone_number
            this.return_method = this.order.return_method
            this.return_reason = this.order.return_reason
            document.addEventListener('keydown', (event) => {
                if (this.error != '') {
                    event.preventDefault()
                    return
                }
            })
        },
        watch: {
            select_item_error(): void {
                if (this.select_item_error !== '') {
                    nextTick(() => {
                        // Scroll to top of div when error occurs (where error message is)
                        const content = document.getElementById('content')
                        if (content) {
                            content.scrollTo({top: 0})
                        }
                    })
                }
            },
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
            seller(): void {
                this.phone_number = this.seller.phone_number
            }
        },
    })
</script>

<style scoped>
    #order {
        margin-left: 2rem;
        margin-right: 2rem;
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
        width: 12rem;
        background-color: white;
        border-radius: 0.5rem;
        font-size: 1.1rem;
    }

    #dark #user_number input, #dark select, #dark textarea {
        background-color: transparent !important;
        color: white !important;
    }

    #dark textarea::placeholder {
        color: lightgray !important;
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
        align-items: center;
        gap: 2rem;
        text-align: center;
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

    #toggle:hover {
        background-color: #D9D9D9;
    }

    #controls {
        display: flex;
        background-color: white;
        margin-left: auto;
        border-radius: 0.2rem;
    }

    #dark #toggle {
        color: black !important;
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

    #minus {
        border-top-right-radius: 0.2rem;
        border-bottom-right-radius: 0.2rem;
    }

    .round-border {
        border-top-left-radius: 0.2rem;
        border-bottom-left-radius: 0.2rem;
    }

    #minus i {
        color: red !important;
        font-size: 0.8rem;
    }

    #resnum1 {
        margin: auto;
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

    .name {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #image {
        position: relative;
    }

    .name {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #content { 
        display: flex;
        gap: 8rem;
    }

    #col1, #col2 {
        display: flex;
        flex-direction: column;
        gap: 3rem;
    }

    #card_ending, #address_lines, #user_number {
        border: 0.1rem solid #0DCAF0;
        padding: 1rem;
        border-radius: 0.8rem;
    }

    #payment div, #number div, #return_reason div, #address div {
        gap: 0.8rem;
        font-size: 1.1rem;
    }

    #header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    #header div, .title, button {
        font-size: 1.1rem;
    }

    #number, #payment, #address, #return_reason {
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

    #address_lines, #user_number {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
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

    #dark option {
        color: black;
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
        background-color: white;
    }

    #dark #buttons button:hover {
        background-color: darkgray;
    }

    #cancel {
        background-color: red !important;
        color: white;
    }

    #cancel:hover {
        cursor: pointer;
        background-color: darkred !important;
    }

    #number_container button, #address_lines button {
        border: none;
        color: white;
        border-radius: 0.5rem;
        width: 2rem;
        height: 2rem;
    }

    #user_number p {
        font-size: 1.1rem;
    }

    #number_container button i, #address_lines button i {
        font-size: 1.2rem;
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

    #dark #resnum {
        color: black;
    }

    #back p:hover {
        text-decoration: underline;
    }

    #back i, #back p {
        font-size: 1.2rem;
    }

    .input {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }

    .input input {
        padding: 0.6rem !important;
    }

    .header {
        margin-top: 0.5rem;
    }

    .clockwise {
        background-color: red;
    }

    .clockwise:hover {
        background-color: darkred;
        cursor: pointer;
    }

    .save {
        background-color: green;
    }

    .save:hover {
        background-color: darkgreen;
        cursor: pointer;
    }

    #address_lines input {
        border-radius: 0.5rem;
    }

    #dark #checkout, #dark #number_input {
        color: white;
    }

    #dark #resnum, #dark #plus, #dark #minus {
        color: black;
    }

    #dark #number_input {
        background-color: transparent;
    }

    #for_return, #not_for_return {
        border: none;
        padding: 0.4rem;
        padding-left: 0.6rem;
        padding-right: 0.6rem;
        border-radius: 0.5rem;
    }

    #not_for_return {
        background-color: lightgray;
    }

    #for_return {
        background-color: green;
        color: white;
    }

    #for_return:hover, #not_for_return:hover {
        cursor: pointer;
    }

    #not_for_return:hover {
        background-color: darkgray;
    }

    #for_return:hover {
        background-color: rgb(106, 184, 106);
    }

    .input input {
        width: 92% !important;
    }

    button:hover {
        cursor: pointer;
    }

    #select_item_error {
        color: red;
        text-align: center;
    }

    input:disabled, textarea:disabled, select:disabled {
        color: black !important;
        background-color: white !important;
    }

    select:disabled {
        appearance: none; /* remove arrow */
    }

    select, #return_reason textarea {
        border: none;
        font-size: 1.1rem;
    }

    #return_reason textarea {
        padding: 0.5rem;
    }

    textarea {
        resize: none;
    }

    button:disabled, button:disabled:hover {
        background-color: darkgray !important;
        cursor: not-allowed !important;
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

    @media (max-width: 859px) {
    }

    @media (max-width: 782px) {
        #content { 
            flex-direction: column;
            gap: 4rem;
            overflow-y: auto;
            margin-top: 0rem;
        }

        #checkout {
            gap: 1rem;
        }

        #back {
            left: 1rem;
            margin-top: 0.2rem;
        }
    }

    @media (max-width: 611px) {
        #search {
            margin-top: 5rem;
            position: absolute;
        }

        #header1 {
            margin-bottom: 6rem;
        }

        #resources {
            height: 71vh;
        }
    }

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