<template>
    <div id="message-container" v-if="user && other_user">
        <div id="heading">
            <div id="back" @click="back">
                <i class="bi bi-arrow-left-circle-fill"></i>
                <p id="back-msg">Messages</p>
            </div>
            <p id="header" @click="view_profile(false)">{{ other_user.username }}</p>
        </div>
        <div id="messages" v-if="messages_set && messages && messages.messages && Object.keys(messages.messages).length > 0">
            <div id="message-area" :class="message.user === user.id ? 'right end' : 'left'" v-for="message in messages.messages.sort((a,b) => {return new Date(a.sent).getTime() - new Date(b.sent).getTime() })">
                <p id="unread" v-if="message.id === unread_index"><hr>Unread Messages<hr></p>
                <p id="unread1" v-if="new_date(message.id)">{{ convert_date(message.sent) }}</p>
                <i @click="view_profile(false)" v-if="message.user !== user.id" class="bi bi-person-circle icon"></i>
                <div>
                    <p v-if="message.user === user.id" id="time">{{ String(new Date(message.sent).getHours()).padStart(2, '0') }}:{{ String(new Date(message.sent).getMinutes()).padStart(2, '0') }}</p>                    
                    <p v-if="message.user !== user.id" id="time1">{{ String(new Date(message.sent).getHours()).padStart(2, '0') }}:{{ String(new Date(message.sent).getMinutes()).padStart(2, '0') }}</p>                    
                    <p id="value" :class="message.user === user.id ? 'push' : ''" >{{ message.message }}</p>
                </div>
                <i @click="view_profile(true)" v-if="message.user === user.id" class="bi bi-person-circle icon2"></i>
            </div>
        </div>
        <div id="message-box">
            <textarea @input="clear" id="message-content" placeholder="Write a message here"></textarea>
            <button @keydown.enter="send_message" @click="send_message"><i class="bi bi-send"></i></button>
        </div>
        <div v-if="error !== ''">
            <Error :message="error" @close-error="error = ''" />
        </div>
    </div>
    <div v-else>
        <Loading />
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Messages, User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    import Loading from '@/components/user experience/loading/Loading.vue';
    import Error from '@/components/user experience/error/Error.vue';
    export default defineComponent({
        components: { Loading, Error },
        data(): {
            error: string,
            messages: Messages,
            messages_set: boolean,
            unread_index: number,
        } { return {
            error: '',
            unread_index: -1,
            messages_set: false,
            messages: {} as Messages
        }},
        methods: {
            to_month(month_number: number): string {
                return month_number === 1 ? 'Jan' 
                : month_number === 2 ? 'Feb'
                : month_number === 3 ? 'Mar'
                : month_number === 4 ? 'Apr'
                : month_number === 5 ? 'May'
                : month_number === 6 ? 'Jun'
                : month_number === 7 ? 'Jul'
                : month_number === 8 ? 'Aug'
                : month_number === 9 ? 'Sep'
                : month_number === 10 ? 'Oct'
                : month_number === 11 ? 'Nov'
                : 'Dec'
            },
            convert_date(message: string): string {
                return `${new Date(message).getDate() } ${this.to_month(new Date(message).getMonth()+1)} ${String(new Date(message).getFullYear())}`
            },
            new_date(id: number): boolean {
                let previous_id: number = -1
                for (let message of this.messages.messages) {
                    if (message.id === id) break
                    previous_id += 1 
                }
                if (previous_id === -1) return true
                const previous_message = this.messages.messages[previous_id]
                const current_message = this.messages.messages[previous_id+1]
                if (previous_message) {
                    const current_time = new Date(current_message.sent)
                    let date_format = new Date(previous_message.sent)
                    if (current_time.getDate() === date_format.getDate() && current_time.getMonth() === date_format.getMonth() && current_time.getFullYear() === date_format.getFullYear()) {
                        return false
                    }
                } 
                return true
            },
            back(): void {
                window.location.href = '/messages'
            },
            view_profile(my_profile: boolean): void {
                window.location.href = my_profile ? '/listings' : `/seller/${this.other_user.username}`
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
                if (!this.messages_set) {
                    this.get_messages()
                    this.messages_set = true
                    return
                }
                const message_value = message.value
                message.value = ''
                let messageResponse: Response = await fetch(`http://localhost:8000/api/message/${this.messages.id}/${this.user.id}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json'
                    },
                    body: JSON.stringify(message_value)
                })
                if (!messageResponse.ok) {
                    this.error = 'Error sending message. Please try again.'
                    return
                } 
                this.error = ''
                let data: User[] = await messageResponse.json()
                useUsersStore().updateUsers(data)
                useUserStore().saveUser(this.users.find(u => u.id === this.user.id) as User)
                const messages: Messages | undefined = this.user.messages.find(message => message.id === this.messages.id)
                if (messages) {
                    this.messages = messages
                } 
                this.update_last_seen()
            },
            async create_messages(): Promise<void> {
                if (Object.keys(this.other_user).length === 0 || Object.keys(this.user).length === 0) return
                let messagesResponse: Response = await fetch(`http://localhost:8000/api/messages/${this.user.id}/${this.other_user.id}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json'
                    },
                })
                if (!messagesResponse.ok) {
                    this.error = 'Error creating message. Please refresh page.'
                    return
                } 
                this.error = ''
                let data: User[] = await messagesResponse.json()
                useUsersStore().updateUsers(data)
                useUserStore().saveUser(this.users.find(u => u.id === this.user.id) as User)
                const messages: Messages | undefined = this.user.messages.find(message => (message.user1 === this.user.id && message.user2 === this.other_user.id))
                if (messages) {
                    this.messages = messages
                } 
                this.messages_set = true
                this.send_message()
            },
            get_messages(): void {
                if (Object.keys(this.other_user).length === 0 || Object.keys(this.user).length === 0) return
                if (Object.keys(this.user.messages).length === 0 || !(this.user.messages.find(message => (message.user1 === this.user.id && message.user2 === this.other_user.id)))) {
                    this.create_messages()
                    return
                }
            },
            get_unread_message_index(): void {
                for (let message of this.messages.messages) {
                    if (message.user === this.user.id) continue
                    if ((this.messages.user2 === this.user.id && (new Date(message.sent).getTime() >= new Date(this.messages.user2_seen).getTime())) || (this.messages.user1 === this.user.id && (new Date(message.sent).getTime() >= new Date(this.messages.user1_seen).getTime()))) {
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
            },
            messages(new_messages: Messages): void {
                this.scroll()
            }
        },
        mounted(): void {
            if (!this.messages_set && Object.keys(this.user.messages).length > 0) {
                const message = this.user.messages.find(message => (message.user1 === this.user.id && message.user2 === this.other_user.id) || (message.user2 === this.user.id && message.user1 === this.other_user.id))
                if (message) {
                    this.messages = message
                    this.messages_set = true
                    this.update_last_seen()
                    return
                }
            }
        }
    })
</script>

<style scoped>
    #time {
        text-align: right;
        color: rgb(81, 80, 80);
    }

    #time1 {
        text-align: left;
        color: rgb(81, 80, 80);
    }

    #heading {
        display: flex;
        align-items: center;
        width: 100%;
        justify-content: space-between;
    }

    #back {
        display: flex;
        gap: 1rem;
        font-size: 2rem;
        align-items: center;
        position: absolute;
        margin-left: 2rem;
    }

    #back:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    #back-msg {
        font-size: 1.5rem;
    }

    #back i:hover {
        cursor: pointer;
        color: rgb(86, 85, 85);
    }

    #dark #back i:hover {
        color: rgb(206, 206, 206);
    }

    #back i {
        font-size: 1.5rem;
    }

    #message-container {
        margin-top: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 86vh;
    }

    #dark #message-container {
        color: white;
    }

    #header {
        font-size: 2rem;
        margin: auto;
   }

   #header:hover {
        text-decoration: underline;
        cursor: pointer;
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
        width: 29rem;
        align-items: flex-end;
   }

   .end {
        justify-content: end;
   }

   #message-area i {
        font-size: 2rem;
   }

   .icon {
        margin-right: 2rem;
   }

   .icon2 {
        margin-left: 2rem;
   }

   .icon:hover, .icon2:hover {
        color: darkgray;
        cursor: pointer;
   }

   #messages {
        padding-right: 2rem;
        overflow-y: auto;
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
        word-wrap: break-word;
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
        margin-bottom: 1rem;
        text-align: center;
        gap: 1rem;
   }

   #unread1 {
        text-align: center;
        flex: 0 0 100%;
        color: rgb(86, 85, 85);
        justify-content: center;
        margin-bottom: 1rem;
   }

   hr {
        background-color: black;
        border: none;
        height: 0.1rem;
        width: 7rem;
   }

   #dark #time, #dark #time, #dark #time1, #dark #unread, #dark #unread1 {
        color: rgb(206, 206, 206);
   }

   #dark hr {
        background-color: rgb(206, 206, 206);
    }

    /* Responsive design */
    @media (max-width: 734px) {
        #messages {
            width: 20rem;
            margin-top: 1rem;
        }

        #messages #value {
            max-width: 10rem;
        }

        #message-area {
            width: 19rem;
        }

        #message-box textarea {
            width: 15rem;
        }

        #message-box {
            margin-top: 1rem;
        }

        #back i, #back-msg {
            font-size: 1rem;
        }

        #header {
            font-size: 1.6rem;
        }
    }
</style>