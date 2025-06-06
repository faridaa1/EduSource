<template>
    <div id="help-container">
        <div class="item">
            <p id="line">Need live support? Need product recommendations? Speak to our ChatBot below:</p>
            <button @click="chatbot">Start Chatting Now</button>
        </div>
        <div id="faqs">
            <div id="header">Frequently Asked Questions</div>
            <div class="item">
                <div class="heading" @click="one=!one">
                    <p>How do I exchange resources?</p>
                    <i v-if="!one" class="bi bi-arrow-down-circle-fill"></i>
                    <i v-if="one" class="bi bi-arrow-up-circle-fill"></i>
                </div>
                <div v-if="one" class="list">
                    <p>1. Log in</p>
                    <p>2. Search for the item</p>
                    <p>3. Select the item</p>
                    <p>4. Select 'Exchange'</p>
                    <p>5. Select a resource you want to exchange</p>
                </div>
            </div>
            <div class="item">
                <div class="heading" @click="two=!two">
                    <p>How do I place an order?</p>
                    <i v-if="!two" class="bi bi-arrow-down-circle-fill"></i>
                    <i v-if="two" class="bi bi-arrow-up-circle-fill"></i>
                </div>
                <div v-if="two" id="two">
                    <div class="list">
                        <p>Method 1:</p>
                        <p>1. Ensure you are logged in and in buyer mode (from settings)</p>
                        <p>2. Search for the item</p>
                        <p>3. Select the item</p>
                        <p>4. Select Buy Now</p>
                        <p>5. Select Place Order</p>
                    </div>
                    <div class="list">
                        <p>Method 2:</p>
                        <p>1. Ensure you are logged in and in buyer mode (from settings)</p>
                        <p>2. Search for the item</p>
                        <p>3. Select the item</p>
                        <p>4. Add item to Cart</p>
                        <p>5. Select Cart</p>
                        <p>6. Select Checkout</p>
                        <p>7. Select Place Order</p>
                    </div>
                </div>
            </div>
            <div class="item">
                <div class="heading" @click="three=!three">
                    <p>How do I list items?</p>
                    <i v-if="!three" class="bi bi-arrow-down-circle-fill"></i>
                    <i v-if="three" class="bi bi-arrow-up-circle-fill"></i>
                </div>
                <div v-if="three" class="list">
                    <p>1. Ensure you are logged in and in seller mode (from settings)</p>
                    <p>2. Select Account</p>
                    <p>3. Select Listings</p>
                    <p>4. Select the + within the listing container</p>
                </div>
            </div>
            <div class="item">
                <div class="heading" @click="four=!four">
                    <p>How do I track on order?</p>
                    <i v-if="!four" class="bi bi-arrow-down-circle-fill"></i>
                    <i v-if="four" class="bi bi-arrow-up-circle-fill"></i>
                </div>
                <div v-if="four" class="list">
                    <p>1. Log in</p>
                    <p>2. Select Account</p>
                    <p>3. Select Orders</p>
                    <p>4. Select Order</p>
                    <p>5. View Order Status</p>
                </div>
            </div>
            <div class="item">
                <div class="heading" @click="five=!five">
                    <p>How do I start a return?</p>
                    <i v-if="!five" class="bi bi-arrow-down-circle-fill"></i>
                    <i v-if="five" class="bi bi-arrow-up-circle-fill"></i>
                </div>
                <div v-if="five" class="list">
                    <p>1. Ensure you are logged in and in buyer mode (from settings)</p>
                    <p>2. Select Account</p>
                    <p>3. Select Orders</p>
                    <p>4. Select Order</p>
                    <p>5. Select Start Return</p>
                    <p>6. Select number of items for return</p>
                    <p>7. Select Return Method</p>
                    <p>8. (Optional) Add Return Reason</p>
                    <p>9. Click Submit</p>
                </div>
            </div>
        </div>
        <div class="item">
            <p>Something else? Submit feedback below:</p>
            <textarea v-model="feedback" placeholder="Enter text here"></textarea>
            <button @keydown.enter="submit_feedback" :disabled="!feedback_sent" id="submit" @click="submit_feedback">Submit</button>
        </div>
        <div v-if="error!==''">
            <Error :message="error" @close-error="error=''" />
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { User } from '@/types';
    import Error from '../user experience/error/Error.vue';
    import { useURLStore } from '@/stores/url';
    export default defineComponent({
        components: { Error },
        data(): {
            feedback: string,
            one: boolean,
            feedback_sent: boolean,
            two: boolean,
            three: boolean,
            four: boolean,
            five: boolean,
            error: string,
        } { return {
            feedback_sent: true,
            one: false,
            two: false,
            three: false,
            four: false,
            five: false,
            feedback: '',
            error: ''
        }},
        methods: {
            chatbot(): void {
                // Send user to chatbot page
                window.location.href = '/chatbot'
            },
            async submit_feedback(): Promise<void> {
                // Send feedback
                this.feedback_sent = false
                let send_feedback: Response = await fetch(`${useURLStore().url}/api/feedback/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json'
                    },
                    body: JSON.stringify(this.feedback)
                })
                if (!send_feedback.ok) {
                    this.error = 'Error submitting feedback. Please try again.'
                } else {
                    this.feedback_sent = true
                    this.feedback = ''
                }
            },
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
        },
    })
</script>

<style scoped>
    #help-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        height: 90vh;
        width: 96vw;
        overflow-y: auto;
        margin-top: 2rem;
        margin-left: 2rem;
    }

    #dark #help-container {
        color: white;
    }

    button {
        background-color: #0DCAF0;
        border: none;
        padding: 0.5rem;
        margin-right: auto;
        border-radius: 0.5rem;
        color: black;
    }

    .heading {
        display: flex;
        gap: 1rem;
    }

    #submit {
        margin-bottom: 3rem;
    }

    #dark .heading {
        color: rgb(235, 235, 235);
    }

    .heading:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    #two {
        display: flex;
        /* gap: 4rem; */
        flex-direction: column;
        gap: 1.3rem;
    }

    .list {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }

    #line {
        width: 80%;
    }

    #faqs #header {
        text-decoration: underline;
    }

    .item {
        display: flex;
        flex-direction: column;
        gap: 0.7rem;
    }

    #dark button {
        background-color: white;
    }

    button:hover {
        cursor: pointer;
        background-color: #1e7a8d;
    }

    #dark button:hover {
        background-color: darkgray;
    }

    textarea {
        resize: none;
        padding: 0.5rem;
        border-radius: 0.5rem;
        height: 5rem;
        width: 75%;
    }

    #faqs {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    button:disabled {
        background-color: #d9d9d9;
        cursor: not-allowed;
    }

    /* Responsive Design */
    @media (max-width: 500px) {
        #two {
            display: flex;
            gap: 3rem;
        }

        #help-container {
            width: 90vw;
        }
    }
</style>
