<template>
    <div id="message-container">
        <div id="heading">
            <p id="header">EduBot</p>
            <div id="front" @click="show_info=!show_info">
                <i class="bi bi-info-circle-fill"></i>
            </div>
        </div>
        <div id="background" v-if="show_info" @click="show_info=false">
            <div id="shown-info">
                <p id="x" @click="show_info=false"><i class="bi bi-x-lg"></i></p>
                <p>Hi! I am EduBot - a ChatBot designed for your assistance.</p>
                <p>Before we get started, there are certain ways to communicate with me to get the best results.</p>
                <p v-if="Object.keys(user).length > 0">Message 'Provide me with personalised recommendations' for personalised recommendations.</p>
                <p>Start your message with 'Can you provide resource recommendations for...' for resource recommendations.</p>
                <p>Start your message with 'What is the status of order [number]' for order tracking.</p>
                <p>Remember: You can always come back to this message by clicking the 𝒊 next to my name.</p>
                <p>Happy chatting!</p>
            </div>
        </div>
        <div id="messages">
            <div class="message-area">
                <i class="bi bi-chat-left-text icon"></i>
                <p class="value">Hi! I am EduBot. How can I help?</p>
            </div>
            <div class="message-area" :class="message.user === 'user' ? 'right end' : 'left'" v-for="message in messages.sort((a,b) => b.id - a.id)">
                <i v-if="message.user !== 'user'" class="bi bi-robot icon"></i>
                <p v-html="format(message.message)" class="value" :class="message.user === 'user' ? 'push' : ''" ></p>
                <i v-if="message.user === 'user'" class="bi bi-person-circle icon2"></i>
            </div>
            <div class="message-area left" v-if="chatbot_responding">
                <i class="bi bi-chat-left-text icon"></i>
                <p class="value"><i class="bi bi-three-dots"></i></p>
            </div>
        </div>
        <div id="message-box">
            <textarea @input="clear" id="message-content" placeholder="Write a message here"></textarea>
            <button :disabled="chatbot_responding" @click="send_message"><i class="bi bi-send"></i></button>
        </div>
        <div v-if="error !== ''">
            <Error :message="error" @close-error="error = ''" />
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    import Error from '@/components/user experience/error/Error.vue';
    export default defineComponent({
        components: { Error },
        data(): {
            show_info: boolean,
            chatbot_responding: boolean,
            error: string,
            messages: { id: number, user: 'user' | 'ai', message: string }[],
            messages_set: boolean,
            current_id: number,
        } { return {
            show_info: true,
            error: '',
            messages_set: true,
            chatbot_responding: false,
            messages: [],
            current_id: -1
        }},
        methods: {
            format(data: string): string {
                return data.replaceAll('\n','<br>')
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
                    this.messages_set = true
                    return
                }
                const message_value = message.value
                this.messages.push({id: this.current_id+1, user: 'user', message: message_value})
                this.scroll()
                message.value = ''
                this.chatbot_responding = true
                let messageResponse: Response = await fetch(`http://localhost:8000/api/chatbot/${Object.keys(this.user).length > 0 ? this.user.id : -1}/`, {
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
                } else {
                    this.error = ''
                    let data: string = await messageResponse.json()
                    this.chatbot_responding = false
                    this.messages.push({id: this.current_id+1, user: 'ai', message: data})
                    this.scroll()
                }
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
    })
</script>

<style scoped>
    #heading {
        display: flex;
        align-items: center;
        padding-top: 2rem;
        width: 100%;
        justify-content: space-between;
    }

    #front {
        display: flex;
        gap: 1rem;
        font-size: 2rem;
        align-items: center;
        position: absolute;
        right: 0;
        padding-right: 20rem;
    }

    #front:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    #front i:hover {
        cursor: pointer;
        color: rgb(86, 85, 85);
    }

    #dark #front i:hover {
        color: rgb(206, 206, 206);
    }

    #front i {
        font-size: 1.5rem;
    }

    #message-container {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 89vh;
        gap: 2rem;
    }

    #background {
        position: absolute;
        background-color: rgb(86, 85, 85, 0.2);
        z-index: 2;
        height: 100vh;
        width: 100vw;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    #dark #shown-info {
        background-color: black;
        color: white;
    }
    
    #dark #message-container {
        color: white;
    }

    #header {
        font-size: 2rem;
        margin: auto;
   }

   #message-box {
        padding-top: auto;
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

   .message-area {
        display: flex;
        width: 29rem;
        align-items: flex-end;
   }

   .end {
        justify-content: end;
   }

   .message-area i {
        font-size: 2rem;
   }

   .icon {
        margin-right: 2rem;
   }

   .icon2 {
        margin-left: 2rem;
   }

   #messages {
        padding-right: 2rem;
        overflow-y: auto;
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

   #messages .value {
        align-self: center;
        max-width: 20rem;
        word-wrap: break-word;
   }

   #messages .push {
        text-align: right;
   }

   hr {
        background-color: black;
        border: none;
        height: 0.1rem;
        width: 7rem;
   }

   #dark #time, #dark #time, #dark #time1 {
        color: rgb(206, 206, 206);
   }

   #dark hr {
        background-color: rgb(206, 206, 206);
    }

    #shown-info {
        background-color: #0DCAF0;
        border-radius: 0.5rem;
        padding: 1rem;
        width: 32rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        position: relative;
    }

    #shown-info p {
        font-size: 1.1rem;
    }

    #x {
        color: red;
        position: absolute;
        right: 1rem;
        top: 0.6rem;
    }

    #x i {
        font-size: 1.4rem !important;
    }

    #x:hover {
        cursor: pointer;
        color: darkred;
    }

    button:disabled {
        background-color: darkgray !important;
        cursor: not-allowed;
    }

    /* Responsive design */
    @media (max-width: 734px) {
        #messages {
            width: 20rem;
        }

        #shown-info {
            width: 23rem;
        }

        #messages .value {
            max-width: 10rem;
        }

        .message-area {
            width: 18rem;
        }

        #message-box textarea {
            width: 15rem;
        }

        #message-box {
            margin-top: 1rem;
        }

        #front i, #back-msg {
            font-size: 1rem;
        }

        #header {
            font-size: 1.6rem;
        }
    }
</style>