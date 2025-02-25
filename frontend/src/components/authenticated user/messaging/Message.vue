<template>
    <div id="message-container" v-if="user && other_user">
        <p id="header">Messages</p>
        <div id="messages">

        </div>
        <div id="message-box">
            <textarea id="" placeholder="Write a message here"></textarea>
            <button><i class="bi bi-send"></i></button>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
        } { return {
        }},
        methods: {
        },
        computed: {
            users(): User[] {
                return useUsersStore().users
            },
            user(): User {
                return useUserStore().user
            },
            allResources(): Resource[] {
                const window_location: string[] = window.location.href.split('/')
                const id: string = window_location[window_location.length-1]
                let returnedResources = [] as Resource[]
                const initial_resource: Resource | undefined = useResourcesStore().resources.find(resource => resource.id === parseInt(id))
                if (initial_resource === undefined) return []
                if (initial_resource.unique) {
                    returnedResources.push(initial_resource)
                    return returnedResources
                }
                const resources: Resource[] = useResourcesStore().resources.filter(resource => resource.name === initial_resource.name && resource.author === initial_resource.author && !resource.unique && parseInt(resource.stock.toString()) > 0 && !resource.is_draft && (resource.allow_collection || resource.allow_delivery))
                returnedResources.push(...resources)
                return returnedResources
            },
            other_user(): User | undefined {
                const window_location: string[] = window.location.href.split('/')
                const other_seller: number = parseInt(window_location[window_location.length-1])
                return this.users.find(user => user.id === other_seller)
            },
        },
        watch: {
            async user(new_user: User): Promise<void> {
            },
            async resource(resource: Resource): Promise<void> {
            },
        },
    })
</script>

<style scoped>
    #message-container {
        margin-top: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 55rem;
    }

    #header {
        font-size: 2rem;
   }

   #message-box {
        margin-top: auto;
        display: flex;
        gap: 1rem;
        align-items: center;
   }

   #message-box button {
        background-color: green;
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 0.5rem;
   }

   #message-box button:hover {
        background-color: rgb(27, 108, 27);
        cursor: pointer;
   }

   #message-box textarea {
        background-color: #D9D9D9;
        border-radius: 1rem;
        width: 30rem;
        height: 6rem;
        border-right: 2rem;
        resize: none;
        padding: 1rem;
   }
</style>