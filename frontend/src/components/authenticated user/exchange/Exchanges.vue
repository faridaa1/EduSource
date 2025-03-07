<template>
    <div id="exchanges-container" v-if="user.exchanges && filtered_exchanges">
        <div id="header">
            <p>Exchanges</p>
            <div>
                <label>Sort</label>
                <select v-model="sort">
                    <option value="new">New to Old</option>
                    <option value="old">Old to New</option>
                </select>
            </div>
        </div>
        <div id="exchanges-outer" v-if="filtered_exchanges.length > 0">
            <div id="exchanges">
                <div id="row-header" class="row">
                    <div class="border-right">Seller</div>
                    <div class="border-right">My Resource</div>
                    <div>Seller Resource</div>
                </div>
                <div :class="exchange === filtered_exchanges[filtered_exchanges.length-1] ? 'row rounded-bottom' : 'row border-bottom'" v-for="exchange in filtered_exchanges" @click="view_exchange(exchange.id)">
                    <div class="border-right">{{ exchange.user1 === user.id ? get_user(exchange.user2).username : get_user(exchange.user1).username }}</div>
                    <div class="border-right">{{ exchange.user1 === user.id ? Object.keys(get_resource(exchange.resource1)).length > 1 ? get_resource(exchange.resource1).name : 'Not chosen' : Object.keys(get_resource(exchange.resource2)).length > 1 ? get_resource(exchange.resource2).name : 'Not chosen' }}</div>
                    <div>{{ exchange.user1 === user.id ? Object.keys(get_resource(exchange.resource2)).length > 1 ? get_resource(exchange.resource2).name : 'Not chosen' : Object.keys(get_resource(exchange.resource1)).length > 1 ? get_resource(exchange.resource1).name : 'Not chosen' }}</div>
                </div>
            </div>
        </div>
        <div v-else>
            <p>No exchanges to display</p>
        </div>
    </div>
    <div v-else>
        <Loading />
    </div>
</template>

<script lang="ts">
    import Loading from '@/components/user experience/loading/Loading.vue';
    import { useResourcesStore } from '@/stores/resources';
    import { useUserStore } from '@/stores/user';
    import { useUsersStore } from '@/stores/users';
    import type { Exchange, User, Resource } from '@/types';
    import { defineComponent } from 'vue';
    export default defineComponent({
        components: { Loading },
        data(): { 
            sort: 'new' | 'old'
         } { return {
            sort: 'new'
        }},
        methods: {
            view_exchange(exchange_id: number): void {
                window.location.href = `/exchange/${exchange_id}`
            },
            get_user(user_id: number): User {
                return useUsersStore().users.find(user => user.id === user_id) as User
            },
            get_resource(resource_id: number): Resource {
                return useResourcesStore().resources.find(resource => resource.id === resource_id) as Resource || {}
            }
        },
        computed: {
            user(): User {
                return useUserStore().user || {} as User
            },
            filtered_exchanges(): Exchange[] {
                return this.user.exchanges.sort((a,b) => {
                    if (this.sort === 'new') return b.id - a.id
                    return a.id - b.id
                })
            }
        },
    })
</script>

<style scoped>
    #exchanges-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
        margin-top: 1rem;
    }

    #dark #exchanges-container {
        color: white;
    }

    #exchanges {
        border: 0.1rem solid black;
        border-radius: 0.5rem;
        margin-right: 0.5rem;
    }

    #dark #exchanges {
        border: 0.1rem solid white;
    }

    #exchanges-outer {
        overflow-y: auto;
        max-height: 80vh;
    }

    .row {
        display: flex;
    }

    #header {
        margin-bottom: 2rem;
        margin-top: 1rem;
        position: relative;
        width: 90vw;
        text-align: center;
    }

    #header p {
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .row div {
        width: 30vw;
        font-size: 1.1rem;
        text-align: center;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    #row-header {
        font-weight: bold;
    }

    #row-header, .border-bottom {
        border-bottom: 0.1rem solid black !important;
    }

    #dark #row-header, #dark .border-bottom {
        border-bottom: 0.1rem solid white !important;
    }

    #dark .border-right {
        border-right: 0.1rem solid white;
    }

    .border-right {
        border-right: 0.1rem solid black;
    }

    .row:hover {
        background-color: #0DCAF0;
        cursor: pointer;
    }

    #dark .row:hover {
        background-color: #d9d9d9;
        color: black;
    }

    #row-header:hover {
        background-color: transparent !important;
        cursor: auto;
    }

    #dark #row-header:hover {
        color: white;
    }

    .rounded-bottom {
        border-bottom-left-radius: 0.5rem;
        border-bottom-right-radius: 0.5rem;
    }

    #header div {
        display: flex;
        align-items: center;
        position: absolute;
        top: 1.8rem;
        gap: 0.3rem;
        right: 0;
        display: flex;
    }

    select {
        border-radius: 0.5rem;
        text-align: center;
    }

    /* Responsive Design */
    @media (max-width: 1240px) {
        .row div {
            width: 28vw;
        }

        #header {
            width: 84vw;
        }

        #row-header div {
            white-space: wrap !important;
        }
    }

</style>