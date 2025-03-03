<template>
    <div id="container">
        <div id="content-block">
            <p id="confirmed">Order Confirmed!</p>
            <p id="message">Thank you for shopping with EduSource</p>
            <div id="viewing">
                <p class="button" @click="view('orders')">View Orders</p>
                <p class="button" @click="view('home')">Return Home</p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { defineComponent } from 'vue';
    export default defineComponent({
        methods: {
            view(page: string): void {
                window.location.href = page === 'home' ? '/' : '/orders'
            }
        },
    })
</script>

<style scoped>
    #container {
        height: 100vh;
        width: 100vw;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    #content-block {
        display: flex;
        flex-direction: column;
        padding: 1rem;
        border: 0.15rem solid #0DCAF0;
        border-radius: 0.5rem;
        align-items: center;
        font-size: 2rem;
        width: 30rem;
        text-align: center;
    }

    #dark #content-block {
        border: 0.15rem solid white;
    }
    
    p {
        font-size: 1.5rem;
    }

    #confirmed {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    #viewing {
        margin-top: 2rem;
        display: flex;
        gap: 2rem;
    }

    #viewing p {
        font-size: 1.2rem !important;
    }

    .button {
        background-color: #0DCAF0;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    #dark .button {
        background-color: white;
    }

    .button:hover {
        background-color: #248da2 !important;
        cursor: pointer;
    }

    #dark .button:hover {
        background-color: darkgray !important;
    }

    #dark #container {
        color: white;
    }

    #dark #message {
        color: rgb(206, 206, 206);
    }

    #dark #viewing {
        color: black;
    }

    /* Responsive Design */
    @media (max-width: 500px) {
        #content-block {
            width: 20rem;
        }

        #content-block p {
            font-size: 1.2rem !important;
        }

        #content-block #confirmed {
            font-size: 1.4rem !important;
        }
    }
</style>