<template>
    <div id="main">
        <p id="messages">Messages</p>
        <div id="messages-container" v-if="user">
            <div id="handle">
                <div class="nav">
                    <label >Filter</label>
                    <select v-model="filter_by">
                        <option value="all">Messages: All</option>
                        <option value="read">Messages: Read</option>
                        <option value="unread">Messages: Unread</option>
                    </select>
                </div>
                <div class="nav">
                    <label>Sort By</label>
                    <select v-model="sort_by">
                        <option value="new">Messages: New</option>
                        <option value="old">Messages: Old</option>
                    </select>
                </div>
            </div>
            <div id="overflow">
                <div class="message" v-for="message in filtered_messages()" @click="get_message(message.user1 === user.id ? message.user2 : message.user1)">
                    <i @click="view_profile(message.user1 === user.id ? users.find(user => user.id === message.user2) as User : users.find(user => user.id === message.user1) as User)" class="bi bi-person-circle icon"></i>
                    <div class="message-block">
                        <div class="date-head">
                            <p class="username">{{ message.user1 === user.id ? users.find(user => user.id === message.user2)?.username :users.find(user => user.id === message.user1)?.username }}</p>
                        </div>
                        <p class="content">{{ most_recent_message(message).message }}</p>
                    </div>
                    <div class="message-block notiftime">
                        <p id="datee"> {{ to_date(message.last_edited) }}</p>
                        <p v-if="unseen(message)" id="notification"></p>
                    </div>
                </div>
                <div id="nomes" v-if="filtered_messages().length < 1">No messages to display</div>
            </div>

        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Message, Messages, User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            filter_by : 'read' | 'unread' | 'all',
            sort_by : 'new' | 'old'
        } { return {
            filter_by: 'all',
            sort_by: 'new'
        }},
        methods: {
            to_date(date: string): string {
                const current_time = new Date()
                let date_format = new Date(date)
                if (current_time.getDate() === date_format.getDate() && current_time.getMonth() === date_format.getMonth() && current_time.getFullYear() === date_format.getFullYear()) {
                    // show time if the day is the same
                    return `${String(date_format.getHours()).padStart(2, '0')}:${String(date_format.getMinutes()).padStart(2, '0')}`
                }
                // show date if it happened more than one day ago
                return `${String(date_format.getDate()).padStart(2, '0')}/${String(date_format.getMonth()+1).padStart(2, '0')}/${String(date_format.getFullYear()).slice(-2)}`
            },
            view_profile(seller: User): void {
                window.location.href = `/seller/${seller.username}`
            },
            get_message(userID: number): void {
                window.location.href = `/message/${this.user.id}/${userID}`
            },
            most_recent_message(message: Messages): Message {
                const sorted_messages = message.messages.sort((a, b) => { return new Date(a.sent).getTime() - new Date(b.sent).getTime() })
                return sorted_messages[sorted_messages.length-1]
            },
            unseen(message: Messages): boolean {
                const other_user_messages: Message[] = message.messages.filter(message => message.user !== this.user.id)
                if (!other_user_messages || other_user_messages.length < 1) return false
                const last_message_time: number = new Date(other_user_messages.sort((a, b) => { return new Date(a.sent).getTime() - new Date(b.sent).getTime() })[other_user_messages.length-1].sent).getTime()
                if (message.user1 === this.user.id) return last_message_time > new Date(message.user1_seen).getTime()
                return last_message_time > new Date(message.user2_seen).getTime()
            },
            filtered_messages(): Messages[] {
                if (!this.user.messages) return [] 
                let messages: Messages[] = this.user.messages.sort((a,b) => {
                    if (this.sort_by === 'new') {
                        if (new Date(a.last_edited).getTime() > new Date(b.last_edited).getTime()) {
                            return -1
                        } 
                        return 1
                    } else {
                        if (new Date(a.last_edited).getTime() < new Date(b.last_edited).getTime()) {
                            return -1
                        } 
                        return 1
                    }
                })
                if (this.filter_by === 'read' || this.filter_by === 'unread') {
                    messages = messages.filter(message => this.filter_by === 'read' ? !this.unseen(message) : this.unseen(message))
                }
                return messages
            }
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
            users(): User[] {
                return useUsersStore().users
            }
        },
    })
</script>

<style scoped>
    .notiftime {
        align-items: center;
        justify-content: start;
        align-self: flex-start;
        width: 6rem;
    }

    #datee {
        color: rgb(81, 80, 80);
        margin-left: auto;
        margin-bottom: 0.5rem;
    }
   
    .date-head {
        display: flex;
        justify-content: space-between;
    }

    #nomes {
        margin-top: 1rem;
    }

    .icon:hover {
        color: darkgray;
        cursor: pointer;
    }

    .message-block {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }
    
    #main {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 2rem;
    }

    #overflow {
        display: flex;
        overflow-y: scroll;
        flex-direction: column;
        height: 47rem;
        width: 40rem;
        gap: 1rem;
    }

    #messages-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .message {
        display: flex;
        gap: 1rem;
        font-size: 1.3rem;
        align-items: center;
        padding: 1rem;
        width: 37rem;
    }

    .message i {
        font-size: 2rem;
    }

    .message .content {
        width: 28rem;
        height: 1.3rem;
        padding: 0.5rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .message:hover {
        background-color: #D9D9D9;
        cursor: pointer;
        border-radius: 0.5rem;
    }

    .username {
        font-weight: bold;
        padding-left: 0.5rem;
    }

    #messages {
        font-weight: bold;
        text-align: center;
        font-size: 2rem;
        margin-top: 2rem;
    }

    #notification {
        height: 0.8rem;
        width: 0.8rem;
        background-color: #0DCAF0;

        border-radius: 50%;
    }

    #dark #notification {
        background-color: white;
    }

    .nav {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    #handle {
        display: flex;
        gap: 2rem;
        align-self: flex-end;
    }

    .nav select {
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        #handle {
            flex-direction: column;
            gap: 0.5rem;
            align-self: flex-start;
        }

        #overflow {
            display: flex;
            width: 24rem !important;
            height: 65vh !important;
        }

        .message .content {
            width: 10rem;
        }

        .message {
            width: 20rem;
        }
        
    }
</style>