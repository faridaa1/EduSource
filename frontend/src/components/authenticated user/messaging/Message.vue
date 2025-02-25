<template>
    <div id="message-container" v-if="user && other_user">
        <p id="header">Messages</p>
        <div id="messages" v-if="messages_set">
            <div v-for="message in messages.messages.sort((a,b) => {return new Date(a.sent).getTime() - new Date(b.sent).getTime() })">
                {{ message.message }}
            </div>
        </div>
        <div id="message-box">
            <textarea id="message-content" placeholder="Write a message here"></textarea>
            <button @click="send_message"><i class="bi bi-send"></i></button>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Messages, Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            messages: Messages
            messages_set: boolean,
        } { return {
            messages_set: false,
            messages: {} as Messages
        }},
        methods: {
            async send_message(): Promise<void> {
                const message: HTMLTextAreaElement = document.getElementById('message-content') as HTMLTextAreaElement
                if (!message) return
                let messageResponse: Response = await fetch(`http://localhost:8000/api/message/${this.messages.id}/${this.user.id}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(message.value)
                })
                if (!messageResponse.ok) {
                    console.error('Error sending message')
                    return
                } 
                let data: User[] = await messageResponse.json()
                useUsersStore().updateUsers(data)
                useUserStore().saveUser(this.users.find(u => u.id === this.user.id) as User)
                const messages: Messages | undefined = this.user.messages.find(message => message.id === this.messages.id)
                if (messages) {
                    this.messages = messages
                } 
            },
            async create_messages(): Promise<void> {
                if (Object.keys(this.other_user).length === 0 || Object.keys(this.user).length === 0) return
                let messagesResponse: Response = await fetch(`http://localhost:8000/api/messages/${this.user.id}/${this.other_user.id}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                })
                if (!messagesResponse.ok) {
                    console.error('Error creating message')
                    return
                } 
                let data: User[] = await messagesResponse.json()
                useUsersStore().updateUsers(data)
                useUserStore().saveUser(this.users.find(u => u.id === this.user.id) as User)
                const messages: Messages | undefined = this.user.messages.find(message => (message.user1 === this.user.id && message.user2 === this.other_user.id))
                if (messages) {
                    this.messages = messages
                } 
                this.messages_set = true
            },
            get_messages(): void {
                if (Object.keys(this.other_user).length === 0 || Object.keys(this.user).length === 0) return
                if (Object.keys(this.user.messages).length === 0) {
                    this.create_messages()
                    return
                }
            }
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
            other_user(): User {
                const window_location: string[] = window.location.href.split('/')
                const other_seller: number = parseInt(window_location[window_location.length-1])
                const user: User | undefined = this.users.find(user => user.id === other_seller)
                if (user === undefined) return {} as User
                return user
            },
        },
        watch: {
            user(new_user: User): void {
                if (Object.keys(this.user.messages).length > 0) {
                    const message = this.user.messages.find(message => (message.user1 === this.user.id && message.user2 === this.other_user.id) || (message.user2 === this.user.id && message.user1 === this.other_user.id))
                    if (message) {
                        this.messages = message
                        this.messages_set = true
                        return
                    }
                }
                if (!this.messages_set) this.get_messages()
            },
            other_user(new_user: User): void {
                if (Object.keys(this.other_user.messages).length > 0) {
                    const message = this.other_user.messages.find(message => (message.user1 === this.user.id && message.user2 === this.other_user.id) || (message.user2 === this.user.id && message.user1 === this.other_user.id))
                    if (message) {
                        this.messages = message
                        this.messages_set = true
                        return
                    }
                }
                if (!this.messages_set) this.get_messages()
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