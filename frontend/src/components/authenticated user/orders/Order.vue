<template>
    <div id="order" v-if="Object.keys(order).length > 0">
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
                            <div class="resource" v-for="resource in order.resources">
                                <div id="image">
                                    <img :src="`http://localhost:8000/${getResource(resource.resource).image1}`" alt="">
                                    <div id="resnum">{{ resource.number }}</div>
                                </div>
                                <div class="name">
                                    <div>{{ getResource(resource.resource).name }}</div>
                                    <div>{{ currency }}{{ (resource.number*parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                                    <p id="add-review" @click="add_review">Add Review</p>
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
                        {{ order.status }}
                    </div>
                </div>
                <div id="buttons">
                    <button v-if="returnable && order.status === 'Complete'">Start Return</button>
                    <button id="cancel" v-if="order.status === 'Placed'" @click="cancel_order">Cancel</button>
                </div>
            </div>
        </div>
        <div v-if="error !== ''">
            <Error :message="error" @close-error="error=''" />
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Order, Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    import Error from '@/components/user experience/error/Error.vue';
    export default defineComponent({
        components: { Error },
        data(): {
            total: number,
            placed_order: boolean,
            error: string,
        } { return {
            placed_order: false,
            total: 0,
            error: ''
        }},
        methods: {
            
            add_review(): void {
                
            },
            async cancel_order(): Promise<void> {
                let userResponse = await fetch(`http://localhost:8000/api/user/${this.user.id}/order/`, {
                        method: 'DELETE',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf
                        },
                        body: JSON.stringify(this.order.id)
                    })
                if (!userResponse.ok) {
                    this.error = 'Error cancelling order. Please try again'
                    return
                }
                let user: User = await userResponse.json()
                useUserStore().saveUser(user)
                useUsersStore().updateUser(user)
            },
            back(): void {
                window.location.href = '/orders'
            },
            home(): void {
                window.location.href = '/cart'
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
                if (!convertedPrice.ok) return resource.price
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return returnedPrice.new_price
            },
            get_total(): void {
                this.total = 0
                if (!this.user.cart || !this.user.cart.resources) return
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
            returnable(): boolean {
                for(const resource of this.order.resources) {
                    const res = this.getResource(resource.resource)
                    // can return 30 days within purchase date
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
                if (!this.user || !this.user.placed_orders) return {} as Order
                const window_location: string[] = window.location.href.split('/')
                const id: number = parseInt(window_location[window_location.length-1])
                return this.user.placed_orders.find(order => order.id === id) || {} as Order
            }
        },
        async mounted(): Promise<void> {
            for (const resource of useResourcesStore().resources) {
                resource.price = await this.listedprice(resource)
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

    #border {
        border: 0.1rem solid #0DCAF0;
        border-radius: 0.8rem;
        padding: 1rem;
    }

    #body {
        height: 25rem;
        overflow-y: scroll;
        display: flex;
        padding-right: 2rem;
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
        top: 5rem;
        display: flex;
        justify-content: center;
        align-items: center;
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

    #payment {
        display: fl;
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

    #buttons button {
        border-radius: 0.4rem;
        border: none;
        padding: 0.5rem;
    }

    #cancel {
        background-color: red;
        color: white;
    }

    #cancel:hover {
        background-color: darkred;
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

    /* Responsive Design */
    @media (max-width: 1002px) {
        #content { 
            flex-direction: column;
            gap: 4rem;
            overflow-y: scroll;
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
</style>