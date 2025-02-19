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
                    <div id="body">
                        <div class="resource" v-for="resource in user.cart.resources">
                            <div id="image"><img :src="`http://localhost:8000/${getResource(resource.resource).image1}`" alt=""></div>
                            <div class="name">
                                <div>{{ getResource(resource.resource).name }}</div>
                                <div id="toggle">
                                    <div id="resnum">{{ resource.number }}</div>
                                    <div id=controls>
                                        <div id="plus" v-if="resource.number < getResource(resource.resource).stock" @click="add_to_cart(resource)">+</div>
                                        <hr>
                                        <div id="minus" @click="remove_from_cart(resource)">-</div>
                                    </div>
                                </div>
                                <div>{{ currency }}{{ (resource.number*parseFloat(getResource(resource.resource).price?.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
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
                        <div>{{ user.address_line_one }}</div>
                        <div v-if="user.address_second_line">{{ user.address_second_line }}</div>
                        <div>{{ user.city }}</div>
                        <div>{{ user.postcode }}</div>
                        <div class="change_text">Change Address</div>
                    </div>
                </div>
                <div id="number">
                    <div>Phone Number</div>
                    <div id="user_number">
                        <div v-if="!changing_number">{{ user.phone_number }}</div>
                        <div v-if="changing_number" id="number_container">
                            <div><input id="number_input" type="text" :value="user.phone_number" @input="clear_number_error"></div>
                            <div class="edit-buttons">
                                <button class="save" @click="change_phone_number"><i class="bi bi-floppy-fill"></i></button>
                                <button class="clockwise" @click="cancel_edit(0)"><i class="bi bi-arrow-counterclockwise"></i></button>
                            </div>
                        </div>
                        <div class="change_text" @click="changing_number = true">Change Phone Number</div>
                    </div>
                </div>
            </div>
        </div>
        <div id="buttons">
            <button id="place_order">Place Order</button>
            <button id="cancel" @click="home">Cancel</button>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Cart, CartResource, Resource, Review, User, Wishlist } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            total: number
            changing_number: boolean
            valid_number: boolean
        } { return {
            changing_number: false,
            valid_number: false,
            total: 0
        }},
        methods: {
            cancel_edit(attribute: number): void {
                if (attribute === 0) {
                    this.changing_number = false
                }
            },
            clear_number_error(): void {
                const numberElement: HTMLInputElement = document.getElementById('number_input') as HTMLInputElement
                if (!numberElement) return
                numberElement.setCustomValidity('')
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
                    'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(input)
                })
                if (userResponse.ok) {
                    const user: User = await userResponse.json()
                    useUsersStore().updateUser(user)
                    useUserStore().saveUser(user)
                    this.changing_number = false
                } else {
                    console.error('Error updating number')
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
                    if (!confirm('Are you sure you want to delete this item')) {
                        return
                    }
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
                    console.error('Error editing cart')
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
                    console.error('Error editing cart')
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
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return returnedPrice.new_price
            },
            get_total(): void {
                this.total = 0
                if (!this.user.cart || !this.user.cart.resources) return
                for (let item of this.user.cart.resources) {
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
            "user.cart"(): void {
                this.get_total()
            }
        },
    })
</script>

<style scoped>
    #checkout {
        margin-left: 2rem;
        margin-right: 2rem;
        margin-left: 2rem;
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

    #checkout-title {
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }

    #body {
        height: 25rem;
        overflow-y: scroll;
        border: 0.1rem solid #0DCAF0;
        padding: 1rem;
        border-radius: 0.8rem;
        display: flex;
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

    #minus:hover {
        border-top-right-radius: 0.2rem;
        border-bottom-right-radius: 0.2rem;
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

    #header div {
        font-size: 1.3rem;
    }

    #two {
        font-weight: bold;
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

    #dark #body, #dark #user_number, #dark #address_lines, #dark #card_ending {
        border: 0.1rem solid white;
    }

    #buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 2rem;
    }

    #buttons button {
        width: 7rem;
        border-radius: 0.4rem;
        border: none;
        padding: 0.4rem;
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

    #number_container button {
        border: none;
        color: white;
        border-radius: 0.2rem;
        width: 1.5rem;
        height: 1.5rem;
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
</style>