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
                        <img v-if="(user.id === exchange.user1 && (Object.keys(get_resource(exchange.resource1)).length > 0) && get_resource(exchange.resource1).image1) || (user.id === exchange.user2 && (Object.keys(get_resource(exchange.resource2)).length > 0) && get_resource(exchange.resource2).image1)" :src="user.id === exchange.user1 ? `http://localhost:8000/${get_resource(exchange.resource1).image1}` : `http://localhost:8000/${get_resource(exchange.resource2).image1}`">
                    </div>
                    <div class="select">
                        <div class="label">Resource</div>
                        <div class="label">Status</div>
                    </div>
                    <div class="select">
                        <select id="selected_resource" v-model="selected_resource" @input="set_resource('resource')">
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
                        <img v-if="(user.id === exchange.user1 && get_resource(exchange.resource2).image1) || (user.id === exchange.user2 && get_resource(exchange.resource1).image1)" :src="user.id === exchange.user1 ? get_resource(exchange.resource2).image1 ? `http://localhost:8000/${get_resource(exchange.resource2).image1}` : '' : get_resource(exchange.resource1).image1 ? `http://localhost:8000/${get_resource(exchange.resource1).image1}` : ''">
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
            <button v-if="(user.id === exchange.user1) && (user.id === exchange.user1 ? exchange.status1 : exchange.status2) !== 'Pending'" @click="cancel">Cancel</button>
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
    import { useUserStore } from '@/stores/user';
    import { useUsersStore } from '@/stores/users';
    import type { Exchange, User, Resource } from '@/types';
    import { defineComponent, nextTick } from 'vue';
    export default defineComponent({
        components: { Error, Loading },
        data(): { 
            exchange: Exchange, 
            error: string, 
            selected_resource: number, 
            status: 'Pending' | 'Rejected' | 'Accepted',
         } { return {
            exchange: {} as Exchange,
            error: '',
            selected_resource: -1,
            status: 'Pending',
        }},
        methods: {
            back(): void {
                window.location.href = '/exchanges'
            },
            view(): void {
                if (this.user.id === this.exchange.user1) {
                    window.location.href = `/view/${this.exchange.resource2}`
                } else {
                    window.location.href = `/view/${this.exchange.resource2}`
                }
            },
            show_status(): boolean {
                if ((this.exchange.user1 === this.user.id) && (this.exchange.status2 !== 'Pending')) {
                    return true
                } else if ((this.exchange.user1 !== this.user.id) && (this.exchange.status1 !== 'Pending')) {
                    return true
                }
                return false
            },
            async cancel(): Promise<void> {
                const exchangeResponse: Response = await fetch(`http://localhost:8000/api/exchange/user/${this.user.id}/seller/${this.user2.id}/resource/${this.exchange.id}/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                    },
                })
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
            async set_resource(field: string): Promise<void> {
                const exchangeResponse: Response = await fetch(`http://localhost:8000/api/exchange/user/${this.user.id}/seller/${this.user2.id}/resource/${this.exchange.id}/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify({'field': field, data: field === 'resource' ? (document.getElementById('selected_resource') as HTMLSelectElement).value : (document.getElementById('status') as HTMLSelectElement).value})
                })
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
                const resource: Resource | undefined = useResourcesStore().resources.find(resource => resource.id === resource_id)
                return resource || {} as Resource
            }
        },
        computed: {
            user(): User {
                return useUserStore().user || {} as User
            },
            user2(): User {
                return useUsersStore().users.find(user => user.id === (this.user.id === this.exchange.user2 ? this.exchange.user1 : this.exchange.user2)) || {} as User
            },
            resources(): Resource[] {
                return useResourcesStore().resources.filter(resource => resource.user === this.user.id)
            }
        },
        async mounted(): Promise<void> {
            const window_location = window.location.href.split('/')
            const exchangeResponse: Response = await fetch(`http://localhost:8000/api/exchange/user/${this.user.id}/seller/0/resource/${window_location[window_location.length-1]}/`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken' : useUserStore().csrf,
                },
            })
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
        margin-bottom: 1rem;
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
        background-color: red;
        border: none;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-top: 2rem;
    }

    #button button:hover {
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

    /* Responsive Design */
    @media (max-width: 808px) {
        .image {
            height: 8rem;
            width: 8rem;
        }

        #exchange-area {
            flex-direction: column;
            gap: 3rem;
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