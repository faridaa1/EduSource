<template>
    <div id="message-container" v-if="user && other_user">
        <p id="header">{{ other_user.username }}</p>
        <div id="messages" v-if="messages_set">
            <div id="message-area" :class="message.user === user.id ? 'right' : 'left'" v-for="message in messages.messages.sort((a,b) => {return new Date(a.sent).getTime() - new Date(b.sent).getTime() })">
                <p id="unread" v-if="message.id === unread_index"><hr>Unread Messages<hr></p>
                <i @click="view_profile" v-if="message.user !== user.id" class="bi bi-person-circle icon"></i>
                <p id="value" :class="message.user === user.id ? 'push' : ''" >{{ message.message }}</p>
                <i v-if="message.user === user.id" class="bi bi-person-circle"></i>
            </div>
        </div>
        <div id="message-box">
            <textarea @input="clear" id="message-content" placeholder="Write a message here"></textarea>
            <button @click="send_message"><i class="bi bi-send"></i></button>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Messages, Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            messages: Messages,
            messages_set: boolean,
            unread_index: number,
        } { return {
            unread_index: -1,
            messages_set: false,
            messages: {} as Messages
        }},
        methods: {
            view_profile(): void {
                window.location.href = `/seller/${this.other_user.username}`
            },
            async update_last_seen(): Promise<void> {
                this.get_unread_message_index()
                let messageResponse: Response = await fetch(`http://localhost:8000/api/message/${this.messages.id}/${this.user.id}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                })
                if (!messageResponse.ok) {
                    return
                } 
                let data: User[] = await messageResponse.json()
                useUsersStore().updateUsers(data)
                useUserStore().saveUser(this.users.find(u => u.id === this.user.id) as User)
                const messages: Messages | undefined = this.user.messages.find(message => message.id === this.messages.id)
                if (messages) {
                    this.messages = messages
                } 
                this.scroll()
            },
            clear(): void {
                const message: HTMLTextAreaElement = document.getElementById('message-content') as HTMLTextAreaElement
                if (!message) return
                // validation 
                message.setCustomValidity('')
                message.reportValidity()
            },
            async send_message(): Promise<void> {
                const message: HTMLTextAreaElement = document.getElementById('message-content') as HTMLTextAreaElement
                if (!message) return
                
                // validation 
                if (message.value.trim() === '') {
                    message.setCustomValidity('Enter a message')
                    message.reportValidity()
                    return
                }
                this.clear()
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
                message.value = ''
                this.update_last_seen()
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
            },
            get_unread_message_index(): void {
                for (let message of this.messages.messages) {
                    if (message.user === this.user.id) continue
                    if ((this.messages.user2 === this.user.id && (new Date(message.sent).getTime() >= new Date(this.messages.user2_seen).getTime())) || (this.messages.user1 === this.user.id && (new Date(message.sent).getTime() >= new Date(this.messages.user1_seen).getTime()))) {
                        console.log('here')
                        this.unread_index = message.id
                        return
                    }
                }
                this.unread_index = -1
            },
            scroll(): void {
                nextTick(() => {
                    const messagesDiv: HTMLDivElement = document.getElementById('messages') as HTMLDivElement
                    if (messagesDiv) {
                        messagesDiv.scrollTo({ top: messagesDiv.scrollHeight })
                    }
                })
                
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
                if (!this.messages_set && Object.keys(this.user.messages).length > 0) {
                    const message = this.user.messages.find(message => (message.user1 === this.user.id && message.user2 === this.other_user.id) || (message.user2 === this.user.id && message.user1 === this.other_user.id))
                    if (message) {
                        this.messages = message
                        this.messages_set = true
                        this.update_last_seen()
                        return
                    }
                }
                if (!this.messages_set) {
                    this.get_messages()
                } 
            },
            other_user(new_user: User): void {
                if (!this.messages_set && Object.keys(this.other_user.messages).length > 0) {
                    const message = this.other_user.messages.find(message => (message.user1 === this.user.id && message.user2 === this.other_user.id) || (message.user2 === this.user.id && message.user1 === this.other_user.id))
                    if (message) {
                        this.messages = message
                        this.messages_set = true
                        this.update_last_seen()
                        return
                    }
                }
                if (!this.messages_set) {
                    this.get_messages()
                } 
            },
            messages(new_messages: Messages): void {
                this.scroll()
            }
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

   #message-area {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        gap: 2rem;
   }

   #message-area i {
        font-size: 2rem;
   }

   .icon:hover {
        color: darkgray;
        cursor: pointer;
   }

   #messages {
        padding-right: 2rem;
        overflow-y: scroll;
        margin-top: 2rem;
        height: 38rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        width: 30rem;
   }

   .right {
        margin-left: auto;
   }

   .left {
        margin-right: auto;
   }

   #messages #value {
        align-self: center;
        max-width: 20rem;
   }

   #messages .push {
        text-align: right;
   }

   #unread {
        font-weight: bold;
        text-align: center;
        flex: 0 0 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        gap: 1rem;
   }

   hr {
        background-color: black;
        border: none;
        height: 0.1rem;
        width: 7rem;
   }
</style>