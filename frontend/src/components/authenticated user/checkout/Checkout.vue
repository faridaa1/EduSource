<template>
    <div v-if="user.cart" id="checkout">
        <div id="checkout-title">Checkout</div>
        <div id="content">
            <div id="col1">
                <div id="items">
                    <div id="header">
                        <div id="one">Items</div>
                        <div id="two">Total: {{ currency }}{{ total.toFixed(2) }} </div>
                    </div>
                    <div id="border">
                        <div id="body">
                            <div class="resource" v-for="resource in user.cart.resources.filter(resource => valid(resource))">
                                <div id="image"><img :src="`http://localhost:8000/${getResource(resource.resource).image1}`" alt=""></div>
                                <div class="name">
                                    <div>{{ getResource(resource.resource).name }}</div>
                                    <div id="toggle">
                                        <div id="resnum">{{ resource.number }}</div>
                                        <div id=controls>
                                            <div id="plus" v-if="resource.number < getResource(resource.resource).stock" @click="add_to_cart(resource)">+</div>
                                            <hr v-if="resource.number < getResource(resource.resource).stock">
                                            <div id="minus" :class="resource.number < getResource(resource.resource).stock ? '' : 'round-border'" @click="remove_from_cart(resource)"><i :class="resource.number === 1 ? 'bi bi-trash3-fill' : ''"></i>{{ resource.number === 1 ? '' : '-' }}</div>
                                        </div>
                                    </div>
                                    <div>{{ currency }}{{ (resource.number*parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="payment">
                    <div>Payment Method</div>
                    <div id="card_ending">
                        Card ending in 1234
                    </div>
                </div>
            </div>
            <div id="col2">
                <div id="address">
                    <div>Delivery Address</div>
                    <div id="address_lines">
                        <div v-if="!changing_address">{{ user.address_line_one }}</div>
                        <div v-if="user.address_second_line && !changing_address">{{ user.address_second_line }}</div>
                        <div v-if="!changing_address">{{ user.city }}</div>
                        <div v-if="!changing_address">{{ user.postcode }}</div>
                        <div v-if="!changing_address" class="change_text" @click="changing_address = true">Change Address</div>
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
                    <div>Phone Number</div>
                    <div id="user_number">
                        <div id="number_container">
                            <div><input id="number_input" type="text" :value="user.phone_number" @click="changing_number=true" @input="clear_number_error"></div>
                            <div class="edit-buttons" v-if="changing_number">
                                <button class="save" @click="change_phone_number"><i class="bi bi-floppy-fill"></i></button>
                                <button class="clockwise" @click="cancel_edit(0)"><i class="bi bi-arrow-counterclockwise"></i></button>
                            </div>
                        </div>
                        <div v-if="!changing_number" class="change_text" @click="changing_number = true">Change Phone Number</div>
                    </div>
                </div>
            </div>
        </div>
        <div id="buttons">
            <button id="place_order" @click="place_order">Place Order</button>
            <button id="cancel" @click="home">Cancel</button>
        </div>
        <div v-if="confirm !== ''">
            <Confirm :message="confirm" @confirm-no="confirm=''" @confirm-yes="remove_from_cart(stored_resource)" />
        </div>
        <div v-if="error !== ''">
            <Error :message="error" @close-error="error=''" />
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Cart, CartResource, Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    import Error from '@/components/user experience/error/Error.vue';
    import Confirm from '@/components/user experience/confirm/Confirm.vue';
    export default defineComponent({
        components: { Error, Confirm },
        data(): {
            total: number,
            changing_number: boolean,
            changing_address: boolean,
            placed_order: boolean,
            error: string,
            confirm: string,
            stored_resource: CartResource,
        } { return {
            error: '',
            confirm: '',
            placed_order: false,
            changing_number: false,
            changing_address: false,
            total: 0,
            stored_resource: {} as CartResource,
        }},
        methods: {
            valid(resource: CartResource): boolean {
                if (window.location.href.includes('fast')) {
                    const window_location: string[] = window.location.href.split('/')
                    const id: number = parseInt(window_location[window_location.length-1])
                    return resource.resource === id
                }
                return true
            },
            async place_order(): Promise<void> {
                let userResponse: Response
                if (window.location.href.includes('fast')) {
                    const window_location: string[] = window.location.href.split('/')
                    const id: number = parseInt(window_location[window_location.length-1])
                    const resource: number | undefined = this.user.cart.resources.find(resource => resource.resource === id)?.id
                    if (!resource) return
                    userResponse = await fetch(`http://localhost:8000/api/user/${this.user.id}/order/`, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf
                        },
                        body: JSON.stringify(resource)
                    })
                } else {
                    userResponse = await fetch(`http://localhost:8000/api/user/${this.user.id}/order/`, {
                        method: 'GET',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf
                        },
                    })
                }
                if (userResponse.ok) {
                    this.placed_order = true
                    const data: {user: User, resources: Resource[]} = await userResponse.json()
                    useUserStore().saveUser(data.user)
                    useResourcesStore().saveResources(data.resources)
                } else {
                    this.error = 'Error placing order. Please try again.'
                    return
                }
                window.location.href = '/order-confirmation'
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
            attribute_existence(data: string): boolean {
                const user = useUsersStore().users.filter(user => user.id !== this.user.id).find(user => user.phone_number === data)
                return user === undefined ? false : true
            },
            home(): void {
                window.location.href = '/cart'
            },
            async remove_from_cart(resource: CartResource): Promise<void> {
                if (resource.number === 1) {
                    if (this.confirm === '') {
                        this.stored_resource = resource
                        this.confirm = 'Are you sure you want to delete this item?'
                        return
                    }
                    resource = this.stored_resource
                    this.confirm = ''
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
                    this.error = 'Error editing cart. Please try again.'
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
                    this.error = 'Error editing cart. Please try again'
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
                if (!convertedPrice.ok) return resource.price
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return returnedPrice.new_price
            },
            get_total(): void {
                this.total = 0
                if (!this.user.cart || !this.user.cart.resources) return
                for (let item of this.user.cart.resources.filter(resource => this.valid(resource))) {
                    let resource = this.all_resources.find(resource => resource.id === item.resource)
                    if (resource) {
                        const price = parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))
                        this.total += item.number * price
                    }
                }
            }
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
            all_resources(): Resource[] {
                return useResourcesStore().resources
            }
        },
        async mounted(): Promise<void> {
            for (const resource of useResourcesStore().resources) {
                resource.price = await this.listedprice(resource)
            }
            this.placed_order = false
            this.get_total()
            document.addEventListener('keydown', (event) => {
                if (this.confirm !== '' || this.error != '') {
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
            changing_address(new_boolean: boolean): void {
                if (new_boolean) {
                    this.changing_number = false
                }
            },
            changing_number(new_boolean: boolean): void {
                if (new_boolean) {
                    this.changing_address = false
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
            "user.cart"(): void {
                const resources = this.user.cart.resources.filter(resource => this.valid(resource))
                if (!this.placed_order && resources.length === 0) {
                    window.location.href = '/cart'
                }
                this.get_total()
            }
        },
    })
</script>

<style scoped>
    #checkout {
        margin: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2rem;
    }

    #number_container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 2rem;
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

    #checkout-title {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }

    #body {
        height: 25rem;
        overflow-y: scroll;
        padding-right: 1rem;
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    #border {
        border-radius: 0.8rem;
        border: 0.1rem solid #0DCAF0;
        padding: 1rem;
    }

    #dark #border {
        border-color: white;
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

    #resnum {
        margin: auto;
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

    #payment, #number, #address {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    #payment div, #number div, #address div {
        gap: 0.8rem;
        font-size: 1.3rem;
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

    #header div {
        font-size: 1.3rem;
    }

    .change_text { 
        color: rgb(121, 189, 218);
    }

    #dark .change_text {
        color: rgb(206, 206, 206);
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

    #dark #user_number, #dark #address_lines, #dark #card_ending {
        border: 0.1rem solid white;
    }

    #buttons {
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin-top: 2rem;
    }

    #buttons button {
        border-radius: 0.4rem;
        font-size: 1.3rem;
        border: none;
        padding: 0.8rem;
    }

    #place_order {
        background-color: #0DCAF0;
    }

    #dark #place_order {
        background-color: white;
    }

    #place_order:hover {
        background-color: #3991a2;
        cursor: pointer;
    }

    #dark #place_order:hover {
        background-color: darkgray;
        cursor: pointer;
    }

    #cancel {
        background-color: red;
        color: white;
    }

    #cancel:hover {
        cursor: pointer;
        background-color: darkred;
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

    /* Responsive Design */
    @media (max-width: 1110px) {
        .input input {
            width: 92% !important;
        }
    }

    @media (max-width: 782px) {
        #content { 
            flex-direction: column;
            gap: 4rem;
            overflow-y: scroll;
            padding-right: 2rem;
            max-height: 70vh;
            margin-top: 0rem;
        }

        #checkout {
            gap: 1rem;
        }
    }
</style>