<template>
    <div id="exchange-container" v-if="Object.keys(exchange).length > 0 && Object.keys(user).length > 0 && Object.keys(user2).length > 0">
        <div>
            <div id="header">
                <div id="back" @click="back">
                    <i class="bi bi-arrow-left-circle-fill"></i>
                    <p>Exchanges</p>
                </div>
                <p>Resource Exchange</p>
            </div>
            <div id="exchange-area">
                <div class="resource">
                    <div class="name">Me</div>
                    <div class="image">
                        <img v-if="(user.id === exchange.user1 && (Object.keys(get_resource(exchange.resource1)).length > 0) && get_resource(exchange.resource1).image1) || (user.id === exchange.user2 && (Object.keys(get_resource(exchange.resource2)).length > 0) && get_resource(exchange.resource2).image1)" :src="user.id === exchange.user1 ? `${url}/${get_resource(exchange.resource1).image1}` : `${url}/${get_resource(exchange.resource2).image1}`">
                    </div>
                    <div id="toggle">
                        <div id="resnum">{{ user.id === exchange.user1 ? exchange.resource1_number : exchange.resource2_number }}</div>
                        <div id=controls>
                            <div id="plus" v-if="me_within_stock()" @click="set_resource('user1', user.id === exchange.user1 ? exchange.resource1_number+1 : exchange.resource2_number+1)">+</div>
                            <hr v-if="me_within_stock() && (((user.id === exchange.user1) && (exchange.resource1_number > 0)) || ((user.id === exchange.user2) && (exchange.resource2_number > 0)))">
                            <div v-if="((user.id === exchange.user1) && (exchange.resource1_number > 0)) || ((user.id === exchange.user2) && (exchange.resource2_number > 0))" id="minus" :class="me_within_stock() ? '' : 'round-border'" @click="set_resource('user1', user.id === exchange.user1 ? exchange.resource1_number-1 : exchange.resource2_number-1)">-</div> 
                        </div>
                    </div>
                    <div class="select">
                        <div class="label">Resource</div>
                        <div class="label">Status</div>
                    </div>
                    <div class="select">
                        <select id="selected_resource" :v-model="selected_resource" @input="set_resource('resource')">
                            <option style="display: none;" selected>Select</option>
                            <option :value="resource.id" v-for="resource in resources">{{ resource.name }}</option>
                        </select>
                        <select id="status" v-model="status" @input="set_resource('status')">
                            <option value="Rejected">Rejected</option>
                            <option value="Accepted">Accepted</option>
                        </select>
                    </div>
                </div>
                <div id="swap">
                    <i class="bi bi-arrow-repeat"></i>
                </div>
                <div class="resource">
                    <div class="name">{{ user2.username }}</div>
                    <div class="image clickable" @click="view">
                        <img v-if="(user.id === exchange.user1 && get_resource(exchange.resource2).image1) || (user.id === exchange.user2 && get_resource(exchange.resource1).image1)" :src="user.id === exchange.user1 ? get_resource(exchange.resource2).image1 ? `${url}/${get_resource(exchange.resource2).image1}` : '' : get_resource(exchange.resource1).image1 ? `${url}/${get_resource(exchange.resource1).image1}` : ''">
                    </div>
                    <div id="toggle">
                        <div id="resnum">{{ user.id === exchange.user1 ? exchange.resource2_number : exchange.resource1_number }}</div>
                        <div id=controls>
                            <div id="plus" v-if="seller_within_stock()" @click="set_resource('user2', user.id === exchange.user1 ? exchange.resource2_number+1 : exchange.resource1_number+1)">+</div>
                            <hr v-if="seller_within_stock() && (((user.id === exchange.user1) && (exchange.resource2_number > 0)) || ((user.id === exchange.user2) && (exchange.resource1_number > 0)))">
                            <div v-if="((user.id === exchange.user1) && (exchange.resource2_number > 0)) || ((user.id === exchange.user2) && (exchange.resource1_number > 0))" id="minus" :class="seller_within_stock() ? '' : 'round-border'" @click="set_resource('user2', user.id === exchange.user1 ? exchange.resource2_number-1 : exchange.resource1_number-1)">-</div> 
                        </div>
                    </div>
                    <div class="select">
                        <div class="label seller-res">Resource</div>
                        <div class="label">Status</div>
                    </div>
                    <div class="select">
                        <div id="view" class="seller-res" @click="view">View</div>
                        <div>{{ user.id === exchange.user1 ? exchange.status2 : exchange.status1 }}</div>
                    </div>
                </div>
            </div>
        </div>
        <div id="button">
            <button :disabled="api_call" id="cancel" v-if="(user.id === exchange.user1) && (user.id === exchange.user1 ? exchange.status1 : exchange.status2) !== 'Pending'" @click="cancel">Cancel</button>
            <button :disabled="api_call" id="submit" v-if="(exchange.status1 === 'Accepted') && (exchange.status2 === 'Accepted') && (exchange.resource1_number > 0) && (exchange.resource2_number > 0)" @click="submit">Place Order</button>
        </div>
        <div v-if="error !== ''">
            <Error :message="error" @close-error="error=''" />
        </div>
    </div>
    <div v-else>
        <Loading />
    </div>
</template>

<script lang="ts">
    import Error from '@/components/user experience/error/Error.vue';
    import Loading from '@/components/user experience/loading/Loading.vue';
    import { useResourcesStore } from '@/stores/resources';
    import { useURLStore } from '@/stores/url';
    import { useUserStore } from '@/stores/user';
    import { useUsersStore } from '@/stores/users';
    import type { Exchange, User, Resource } from '@/types';
    import { defineComponent } from 'vue';
    export default defineComponent({
        components: { Error, Loading },
        data(): { 
            exchange: Exchange, 
            error: string, 
            selected_resource: number, 
            api_call: boolean,
            status: 'Pending' | 'Rejected' | 'Accepted',
         } { return {
            exchange: {} as Exchange,
            api_call: false,
            error: '',
            selected_resource: -1,
            status: 'Pending',
        }},
        methods: {
            me_within_stock(): boolean {
                // Check if number of items is within the stock of the user
                return ((this.user.id === this.exchange.user1) && (this.exchange.resource1_number < this.get_resource(this.exchange.resource1).stock)) || ((this.user.id === this.exchange.user2) && (this.exchange.resource2_number < this.get_resource(this.exchange.resource2).stock))
            },
            seller_within_stock(): boolean {
                // Check if number of items is within the stock of the seller
                return ((this.user.id === this.exchange.user1) && (this.exchange.resource2_number < this.get_resource(this.exchange.resource2).stock)) || ((this.user.id === this.exchange.user2) && (this.exchange.resource1_number < this.get_resource(this.exchange.resource1).stock))
            },
            back(): void {
                // Go back to exchanges page
                window.location.href = '/exchanges'
            },
            view(): void {
                // Allow user to view resource
                if (this.user.id === this.exchange.user1) {
                    window.location.href = `/view/${this.exchange.resource2}`
                } else {
                    window.location.href = `/view/${this.exchange.resource2}`
                }
            },
            show_status(): boolean {
                // Show user exchange acceptance status
                if ((this.exchange.user1 === this.user.id) && (this.exchange.status2 !== 'Pending')) {
                    return true
                } else if ((this.exchange.user1 !== this.user.id) && (this.exchange.status1 !== 'Pending')) {
                    return true
                }
                return false
            },
            async submit(): Promise<void> {
                // Submit exchange as new order
                this.api_call = true
                const submitResponse = await fetch(`${useURLStore().url}/api/user/${this.user.id}/order/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify({'exchange_id': this.exchange.id})
                })
                this.api_call = false
                if (!submitResponse.ok) { 
                    this.error = 'Error submitting. Please try again.'
                    return 
                } else { 
                    const data: {user: User, resources: Resource[]} = await submitResponse.json()
                    useUserStore().saveUser(data.user)
                    useUsersStore().updateUser(data.user)
                    useResourcesStore().saveResources(data.resources)
                    window.location.href = '/order-confirmation'
                }
            },
            async cancel(): Promise<void> {
                // Cancel exchange
                this.api_call = true
                const exchangeResponse: Response = await fetch(`${useURLStore().url}/api/exchange/user/${this.user.id}/seller/${this.user2.id}/resource/${this.exchange.id}/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                    },
                })
                this.api_call = false
                if (!exchangeResponse.ok) { 
                    this.error = 'Error deleting. Please try again.'
                    return 
                } else { 
                    const user: User = await exchangeResponse.json()
                    useUserStore().saveUser(user)
                    useUsersStore().updateUser(user)
                    window.location.href = '/exchanges'
                }
            },
            async set_resource(field: string, number?: number): Promise<void> {
                // Set resource to the one selected by the user
                this.api_call = true
                const exchangeResponse: Response = await fetch(`${useURLStore().url}/api/exchange/user/${this.user.id}/seller/${this.user2.id}/resource/${this.exchange.id}/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify({'field': field, data: field === 'resource' ? (document.getElementById('selected_resource') as HTMLSelectElement).value 
                        : field === 'status' ? (document.getElementById('status') as HTMLSelectElement).value : number
                    })
                })
                this.api_call = false
                if (!exchangeResponse.ok) { 
                    this.error = 'Error saving change. Please try again.'
                    return 
                } else { 
                    const data: {user: User, exchange: Exchange} = await exchangeResponse.json()
                    useUserStore().saveUser(data.user)
                    useUsersStore().updateUser(data.user)
                    this.exchange = data.exchange
                }
            },
            get_resource(resource_id: number): Resource {
                // Retrieve resource based on given id
                const resource: Resource | undefined = useResourcesStore().resources.find(resource => resource.id === resource_id)
                return resource || {} as Resource
            }
        },
        computed: {
            url(): string {
                return useURLStore().url
            },
            user(): User {
                return useUserStore().user || {} as User
            },
            user2(): User {
                return useUsersStore().users.find(user => user.id === (this.user.id === this.exchange.user2 ? this.exchange.user1 : this.exchange.user2)) || {} as User
            },
            resources(): Resource[] {
                const resources: Resource[] = useResourcesStore().resources.filter(resource => resource.user === this.user.id)
                return resources
            }
        },
        async mounted(): Promise<void> {
            const window_location = window.location.href.split('/')
            this.api_call = true
            // Find exchange between users and initialise variables accordingly
            const exchangeResponse: Response = await fetch(`${useURLStore().url}/api/exchange/user/${this.user.id}/seller/0/resource/${window_location[window_location.length-1]}/`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken' : useUserStore().csrf,
                },
            })
            this.api_call = false
            if (!exchangeResponse.ok) { 
                this.error = 'Error retrieving exchange. Please refresh page.'
                return 
            } else { 
                const data: Exchange = await exchangeResponse.json()
                this.exchange = data
                this.selected_resource = this.user.id === data.user1 ? data.resource1 : data.resource2
                this.status = this.user.id === data.user1 ? data.status1 : data.status2
            }
        }
    })
</script>

<style scoped>
    #exchange-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
        margin-top: 1rem;
        height: 90vh;
        position: relative;
    }

    #dark #exchange-container {
        color: white !important;
    }

    div, p, select {
        font-size: 1.2rem;
    }

    #header div {
        font-size: 1.3rem;
    }

    #header {
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .image {
        height: 15rem;
        width: 15rem;
        border: 0.2rem solid black;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    #dark .image {
        border: 0.2rem solid white;
    }

    #exchange-area {
        display: flex;
        gap: 4rem;
        align-items: center;
        height: 80vh;
        padding-right: 1rem;
        overflow-y: auto;
    }

    .resource {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
    }

    select {
        border-radius: 0.5rem;
    }

    img {
        height: 100%;
        width: 100%;
        object-fit: contain;
    }

    #swap i {
        background-color: #0DCAF0;
        padding: 0.5rem;
        padding-left: 0.65rem;
        padding-right: 0.65rem;
        border-radius: 0.5rem;
        font-size: 2rem;
    }

    #dark #swap i {
        background-color: white;
        color: black;
    }

    #swap {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
    }

    .select {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .select div, select, .label {
        width: 8rem;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .label {
        font-weight: bold;
    }

    #button button {
        border: none;
        padding: 0.5rem;
        color: white;
        border-radius: 0.5rem;
    }

    #button {
        display: flex;
        gap: 1rem;
    }

    #cancel {
        background-color: red;
    }

    #submit {
        background-color: rgb(45, 168, 45);
    }

    #submit:hover {
        background-color: green;
    }

    button:hover {
        cursor: pointer;
    }

    #cancel:hover {
        background-color: darkred;
        cursor: pointer;
    }

    .clickable:hover {
        cursor: pointer;
        background-color: lightgray;
    }

    #view {
        background-color: #0DCAF0;
        border-radius: 0.5rem;
        width: 4rem;
        padding-top: 0.3rem;
        padding-bottom: 0.3em;
    }

    .seller-res {
        width: 8rem !important;
    }

    #dark #view {
        background-color: white; 
        color: black;
    }

    #view:hover {
        cursor: pointer;
        background-color: #116879;
    }

    #dark #view:hover {
        background-color: darkgray;
   } 

   #back {
        display: flex;
        gap: 1rem;
        align-items: center;
        position: absolute;
        left: 3rem;
    }

    #back:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    #back i:hover {
        cursor: pointer;
        color: rgb(86, 85, 85);
    }

    #dark #back i:hover {
        color: rgb(206, 206, 206);
    }

    #back i {
        font-size: 1.3rem;
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
        color: black;
        text-align: center;
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

    button:disabled, button:disabled:hover {
        background-color: darkgray !important;
        cursor: not-allowed !important;
    }

    /* Responsive Design */
    @media (max-width: 808px) {
        .image {
            height: 8rem;
            width: 8rem;
        }

        #exchange-area {
            flex-direction: column;
            gap: 2rem;
        }

        #back p, #back i {
            font-size: 0.8rem;
        }

        #back {
            top: 0.25rem;
            left: 1rem;
            gap: 0.4rem;
        }
    }
</style>