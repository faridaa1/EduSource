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
                                    <img :src="`http://localhost:8000/${getResource(resource.resource).image1}`" alt="">
                                    <div v-if="order.status === 'Requested Return'" id="resnum">{{ resource.number_for_return }}</div>
                                </div>
                                <div class="name">
                                    <div>{{ getResource(resource.resource).name }}</div>
                                    <div v-if="order.status !== 'Requested Return'">{{ currency }}{{ (parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                                    <div v-else>{{ currency }}{{ (resource.number_for_return*parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                                    <div id="toggle" v-if="order.status !== 'Requested Return'">
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
                            <div><input id="number_input" type="text" :value="seller.phone_number" disabled @input="clear_number_error"></div>
                            <div class="edit-buttons" v-if="changing_number">
                                <button class="save" @click="change_phone_number"><i class="bi bi-floppy-fill"></i></button>
                                <button class="clockwise" @click="cancel_edit(0)"><i class="bi bi-arrow-counterclockwise"></i></button>
                            </div>
                        </div>
                        <!-- <div v-if="!changing_number" class="change_text" @click="changing_number = true">Change Phone Number</div> -->
                    </div>
                </div>
            </div>
            <div id="col2">
                <div id="number">
                    <div class="title">Status</div>
                    <div id="user_number">
                        {{ order.status }}
                    </div>
                </div>
                <div id="address">
                    <div>Seller Address</div>
                    <div id="address_lines">
                        <div v-if="!changing_address">{{ seller.address_line_one }}</div>
                        <div v-if="seller.address_second_line && !changing_address">{{ seller.address_second_line }}</div>
                        <div v-if="!changing_address">{{ seller.city }}</div>
                        <div v-if="!changing_address">{{ seller.postcode }}</div>
                        <!-- <div v-if="!changing_address" class="change_text" @click="changing_address = true">Change Address</div> -->
                        <div v-if="changing_address" class="input">
                            <label for="">First Line</label>
                            <input id="address1" type="text" :value="user.address_line_one" @input="clear_address_error">
                        </div>
                        <div v-if="changing_address" class="input">
                            <label for="" class="header">Second Line</label>
                            <input id="address2" type="text" :value="user.address_second_line" @input="clear_address_error">
                        </div>
                        <div v-if="changing_address" class="input">
                            <label for="" class="header">City</label>
                            <input id="city" type="text" :value="user.city" @input="clear_address_error">
                        </div>
                        <div v-if="changing_address" class="input">
                            <label for="" class="header">Postcode</label>
                            <input id="postcode" type="text" :value="user.postcode" @input="clear_address_error">
                        </div>
                        <div v-if="changing_address" class="edit-buttons header">
                            <button class="save" @click="change_address"><i class="bi bi-floppy-fill"></i></button>
                            <button class="clockwise" @click="cancel_edit(1)"><i class="bi bi-arrow-counterclockwise"></i></button>
                        </div>
                    </div>
                </div>
                <div id="number">
                    <div class="title">Return Method</div>
                    <div id="user_number">
                        <select :disabled="order.status === 'Requested Return'" v-model="return_method">
                            <option value="Delivery">Delivery</option>
                            <option value="Collection">Collection</option>
                        </select>
                    </div>
                </div>
                <div id="return_reason"  v-if="order.status !== 'Requested Return' || (order.status === 'Requested Return' && order.return_reason !== '')">
                    <div class="title">Return Reason (optional)</div>
                    <div id="user_number">
                        <textarea :disabled="order.status === 'Requested Return'" v-model="return_reason" placeholder="Enter reason for return"></textarea>
                    </div>
                </div>
                <div id="buttons">
                    <button v-if="order.status === 'Complete'" @click="submit_return(order, false)">Submit</button>
                    <button id="cancel" v-if="order.status === 'Requested Return'" @click="submit_return(order, true)">Cancel</button>
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
    import type { Order, OrderResource, Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    import Error from '@/components/user experience/error/Error.vue';
    import Loading from '@/components/user experience/loading/Loading.vue';
    export default defineComponent({
        components: { Error, Loading },
        data(): {
            total: number,
            return_reason: string,
            placed_order: boolean,
            error: string,
            changing_number: boolean,
            changing_address: boolean,
            return_method: 'Delivery' | 'Collection',
            select_item_error: string,
        } { return {
            return_method: 'Delivery',
            placed_order: false,
            select_item_error: '',
            return_reason: '',
            total: 0,
            error: '',
            changing_number: false,
            changing_address: false,
        }},
        methods: {
            async return_item(return_number: number, resource_id: number): Promise<void> {
                let returnItemResponse = await fetch(`http://localhost:8000/api/user/${this.user.id}/return/${this.order.id}/${resource_id}/`, {
                        method: 'PUT',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                            'Content-Type' : 'application/json',
                        },
                        body: JSON.stringify(return_number)
                    })
                if (!returnItemResponse.ok) {
                    this.error = 'Error updating return status. Please try again.'
                    return
                }
                if (return_number > 0) {
                    this.select_item_error = ''
                }
                let data: {user: User, resource: Resource} = await returnItemResponse.json()
                useUserStore().saveUser(data.user)
                useUsersStore().updateUser(data.user)
                useResourcesStore().updateResource(data.resource)
            },
            cancel_edit(attribute: number): void {
                if (attribute === 0) {
                    this.changing_number = false
                } else {
                    this.changing_address = false
                }
            },
            clear_address_error(): void {
                const address1Element: HTMLInputElement = document.getElementById('address1') as HTMLInputElement
                const address2Element: HTMLInputElement = document.getElementById('address2') as HTMLInputElement
                const cityElement: HTMLInputElement = document.getElementById('city') as HTMLInputElement
                const postcodeElement: HTMLInputElement = document.getElementById('postcode') as HTMLInputElement
                if (!address1Element || !address2Element || !cityElement || !postcodeElement) return
                address1Element.setCustomValidity('')
                address2Element.setCustomValidity('')
                cityElement.setCustomValidity('')
                postcodeElement.setCustomValidity('')
            },
            clear_number_error(): void {
                const numberElement: HTMLInputElement = document.getElementById('number_input') as HTMLInputElement
                if (!numberElement) return
                numberElement.setCustomValidity('')
            },
            async change_address(): Promise<void> {
                const address1Element: HTMLInputElement = document.getElementById('address1') as HTMLInputElement
                const address2Element: HTMLInputElement = document.getElementById('address2') as HTMLInputElement
                const cityElement: HTMLInputElement = document.getElementById('city') as HTMLInputElement
                const postcodeElement: HTMLInputElement = document.getElementById('postcode') as HTMLInputElement
                if (!address1Element || !address2Element || !cityElement || !postcodeElement) return

                // validate address line 1 
                const address1Input = address1Element.value
                if (address1Input.length === 0) {
                    address1Element.setCustomValidity('Cannot be empty')
                    address1Element.reportValidity()
                    return
                } else if (!(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/.test(address1Input))) {
                    address1Element.setCustomValidity('No special characters allowed')
                    address1Element.reportValidity()
                    return
                }

                // validate address line 2
                const address2Input = address2Element.value
                if (address2Input.length !== 0 && !(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/.test(address2Input))) {
                    address2Element.setCustomValidity('No special characters allowed')
                    address2Element.reportValidity()
                    return
                }

                // validate city
                const cityInput = cityElement.value
                if (cityInput.length === 0) {
                    cityElement.setCustomValidity('Cannot be empty')
                    cityElement.reportValidity()
                    return
                } else if (!(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/.test(cityInput))) {                     
                    cityElement.setCustomValidity('No special characters allowed')
                    cityElement.reportValidity()
                    return
                }

                // validate postcode
                const postcodeInput = postcodeElement.value
                if (postcodeInput.length === 0) {
                    postcodeElement.setCustomValidity('Cannot be empty')
                    postcodeElement.reportValidity()
                    return
                } else if (!(/^[A-Za-z0-9]{5,7}$/.test(postcodeInput))) {
                    postcodeElement.setCustomValidity('Enter 5-7 character postcode without spaces')
                    postcodeElement.reportValidity()
                    return
                }
                this.changing_address = false
                await this.update_address('address_line_one', address1Input)
                await this.update_address('address_line_two', address2Input)
                await this.update_address('city', cityInput)
                await this.update_address('postcode', postcodeInput)
            },
            async update_address(attribute: string, data: string): Promise<void> {
                let userResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/${attribute}/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                if (userResponse.ok) {
                    const user: User = await userResponse.json()
                    useUsersStore().updateUser(user)
                    useUserStore().saveUser(user)
                } else {
                    this.error = 'Error updating address. Please try again'
                }
            },
            async change_phone_number(): Promise<void> {
                const numberElement: HTMLInputElement = document.getElementById('number_input') as HTMLInputElement
                if (!numberElement) return
                const input = numberElement.value
                if (input.length === 0) {
                    numberElement.setCustomValidity('Phone number cannot be empty')
                    numberElement.reportValidity()
                    return
                } else if (!(/^07(\d{8,9})$/.test(input))) {
                    numberElement.setCustomValidity('Must be 10 or 11 digit number starting with 07')
                    numberElement.reportValidity()
                    return
                }
                let correctNumber: boolean = this.attribute_existence(input)
                if (correctNumber) {
                    numberElement.setCustomValidity('Account already exists with this phone number')
                    numberElement.reportValidity()
                    return
                } 
                let userResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/number/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(input)
                })
                if (userResponse.ok) {
                    const user: User = await userResponse.json()
                    useUsersStore().updateUser(user)
                    useUserStore().saveUser(user)
                    this.changing_number = false
                    numberElement.blur()
                } else {
                    this.error = 'Error updating number. Please try again.'
                }
            },
            async submit_return(order: Order, cancel: boolean): Promise<void> {
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
                let returnResponse = await fetch(`http://localhost:8000/api/user/${this.user.id}/return/${this.order.id}/`, {
                        method: 'PUT',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                            'Content-Type' : 'application/json',
                        },
                        body: JSON.stringify({cancel: cancel ? 'true' : 'false', return_reason: this.return_reason, return_method: this.return_method})
                    })
                if (!returnResponse.ok) {
                    this.error = 'Error submitting return. Please try again.'
                    return
                }
                let data: {user: User, resources: Resource[]} = await returnResponse.json()
                useUserStore().saveUser(data.user)
                useUsersStore().updateUser(data.user)
                useResourcesStore().saveResources(data.resources)
                const window_location: string[] = window.location.href.split('/')
                if (window_location.length <= 5) {
                    window.location.href = `/order/${window_location[4]}`
                    return
                }
                window.location.href = `/order/${window_location[4]}/${this.order.status}/${window_location[6]}/${window_location[7]}`
            },
            attribute_existence(data: string): boolean {
                const user = useUsersStore().users.filter(user => user.id !== this.user.id).find(user => user.phone_number === data)
                return user === undefined ? false : true
            },
            back(): void {
                const window_location: string[] = window.location.href.split('/')
                if (window_location.length <= 5) {
                    window.location.href = `/order/${window_location[4]}`
                    return
                }
                window.location.href = `/order/${window_location[4]}/${this.order.status}/${window_location[6]}/${window_location[7]}`
            },
            getResource(resource_id: number): Resource {
                const resource: Resource | undefined = this.all_resources.find(resource => resource.id === resource_id)
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
                if (!this.order || !this.order.resources) return
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
                return this.all_resources.find(resource => resource.id === resourceID)?.allow_return || false
            },
        },
        computed: {
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
                const window_location: string[] = window.location.href.split('/')
                const id: number = parseInt(window_location[4])
                if (!this.user || !this.user.placed_orders || !this.user.placed_orders.find(order => order.id === id)) return {} as Order
                let order: Order = this.user.placed_orders.find(order => order.id === id) as Order
                return order
            }
        },
        async mounted(): Promise<void> {
            for (const resource of useResourcesStore().resources) {
                resource.price = await this.listedprice(resource)
            }
            this.placed_order = false
            this.get_total()
            this.return_method = this.order.return_method
            this.return_reason = this.order.return_reason
            document.addEventListener('keydown', (event) => {
                if (this.error != '') {
                    event.preventDefault()
                    return
                }
                if ((event.key === 'ArrowDown' || event.key === 'Enter') && this.changing_address) {
                    const input: HTMLInputElement = event.target as HTMLInputElement
                    if (!input) return
                    if (input.id === 'address1') {
                        const input2: HTMLInputElement = document.getElementById('address2') as HTMLInputElement
                        if (input2) input2.focus()
                    } else if (input.id === 'address2') {
                        const input2: HTMLInputElement = document.getElementById('city') as HTMLInputElement
                        if (input2) input2.focus()
                    } else if (input.id === 'city') {
                        const input2: HTMLInputElement = document.getElementById('postcode') as HTMLInputElement
                        if (input2) input2.focus()
                    } else if (input.id === 'postcode') {
                        this.change_address()
                    }
                } else if (event.key === 'ArrowUp' && this.changing_address) {
                    const input: HTMLInputElement = event.target as HTMLInputElement
                    if (!input) return
                    if (input.id === 'address2') {
                        const input2: HTMLInputElement = document.getElementById('address1') as HTMLInputElement
                        if (input2) input2.focus()
                    } else if (input.id === 'city') {
                        const input2: HTMLInputElement = document.getElementById('address2') as HTMLInputElement
                        if (input2) input2.focus()
                    } else if (input.id === 'postcode') {
                        const input2: HTMLInputElement = document.getElementById('city') as HTMLInputElement
                        if (input2) input2.focus()
                    }
                } else if (event.key === 'Enter' && this.changing_number) {
                    this.change_phone_number()
                }
            })
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
        font-size: 1.3rem;
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
        gap: 1rem;
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
        font-size: 1.3rem;
    }

    #header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    #header div, .title, button {
        font-size: 1.3rem;
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
        font-size: 1.3rem;
    }

    #return_reason textarea {
        padding: 0.5rem;
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

    @media (max-width: 859px) {
        input {
            width: 20rem !important;
        }
    }

    @media (max-width: 782px) {
        #content { 
            flex-direction: column;
            gap: 4rem;
            overflow-y: scroll;
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
            width: 20rem !important;
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
        }

        #number_of_items {
            left: 7rem;
        }

        #resources {
            height: 76vh;
        }
    }
</style>