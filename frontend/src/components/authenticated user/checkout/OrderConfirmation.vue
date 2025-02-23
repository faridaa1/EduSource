<template>
    <div id="container">
        <div id="content-block">
            <p id="confirmed">Order Confirmed!</p>
            <p>Thank you for shopping with EduSource</p>
            <div id="viewing">
                <p>View your orders <span @click="view('orders')">here</span></p>
                <p>Return Home <span @click="view('home')">here</span></p>
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
        display: flex;
    }

    #content-block {
        display: flex;
        flex-direction: column;
        margin: auto;
        padding: 1rem;
        border: 0.15rem solid #0DCAF0;
        border-radius: 0.5rem;
        align-items: center;
        font-size: 2rem;
        width: 30rem;
    }

    #dark #content-block {
        border: 0.15rem solid white;
    }
    
    p, span {
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

    #viewing p, span {
        font-size: 1.2rem !important;
    }

    span {
        background-color: #0DCAF0;
        border-radius: 0.5rem;
        padding: 0.4rem;
    }

    #dark span {
        background-color: white;
    }

    span:hover {
        text-decoration: underline;
        background-color: #248da2 !important;
        cursor: pointer;
    }

    #dark span:hover {
        background-color: darkgray !important;
    }
</style>