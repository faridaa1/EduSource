<template>
    <div id="help-container">
        <div>
            <p>Need live support? Need product recommendations? Speak to our ChatBot below:</p>
            <button>Start Chatting Now</button>
        </div>
        <div>Frequently Asked Questions</div>
        <div>
            <p class="heading">How do I exchange resources?</p>
            <div>
                <p>1. Search for the item</p>
                <p>2. Select the item</p>
                <p>3. Select 'Exchange'</p>
                <p>4. Select a resource you want to exchange</p>
            </div>
        </div>
        <div>
            <p class="heading">How do I place an order?</p>
            <div>
                <div>
                    <p>1. Search for the item</p>
                    <p>2. Select the item</p>
                    <p>3. Select Buy Now</p>
                    <p>4. Select Place Order</p>
                </div>
                <div>
                    <p>1. Search for the item</p>
                    <p>2. Select the item</p>
                    <p>3. Add item to Cart</p>
                    <p>4. Select Profile</p>
                    <p>5. Select Cart</p>
                    <p>6. Select Checkout</p>
                    <p>7. Select Place Order</p>
                </div>
            </div>
        </div>
        <div>
            <p class="heading">How do I list items?</p>
            <div>
                <p>1. Select Profile</p>
                <p>2. Select Listings</p>
                <p>3. Select the + within the listing container</p>
            </div>
        </div>
        <div>
            <p class="heading">How do I track on order?</p>
            <div>
                <p>1. Select Profile</p>
                <p>2. Select Orders</p>
                <p>3. Select Order</p>
                <p>4. View Order Status</p>
            </div>
        </div>
        <div>
            <p class="heading">How do I do a return?</p>
            <div>
                <p>1. Select Profile</p>
                <p>2. Select Orders</p>
                <p>3. Select Order</p>
                <p>4. Select Start Return</p>
                <p>5. Select number of items for return</p>
                <p>6. Select Return Method</p>
                <p>7. (Optional) Add Return Reason</p>
                <p>8. Click Submit</p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { User } from '@/types';
    import Error from '../user experience/error/Error.vue';
    export default defineComponent({
        components: { Error },
        data(): {
        } { return {
        }},
        methods: {
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
        },
    })
</script>

<style scoped>
    /* Responsive Design */
    @media (max-width: 855px) {
    }
</style>
