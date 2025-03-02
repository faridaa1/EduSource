<template>
    <div id="outer">
        <div id="inner">
            <p>Whoops! We ran into an error.</p>
            <p id="message">{{ message }}</p>
            <button @click="$emit('close-error')">Ok</button>
        </div>
    </div>
</template>

<script lang="ts">
    import { defineComponent } from 'vue';
    export default defineComponent({
        props: {
            message: {
                type: String,
                required: true
            }
        },
        emits: ['close-error'],
    })
</script>

<style scoped>

    #outer {
        position: absolute;
        top: 0;
        right: 0;
        height: 100vh;
        width: 100vw;
        background-color: rgb(53, 53, 53, 50%);
        z-index: 3;
        justify-content: center;
        align-items: center;
        display: flex;
    }

    #inner {
        background-color: white;
        display: flex;
        align-items: center;
        flex-direction: column;
        gap: 0.5rem;
        padding: 1rem;
        border-radius: 1rem;
        justify-content: center;
    }

    p {
        font-size: 1.5rem;
        color: red;
    }

    #message {
        font-size: 1.3rem;
        color: black;
    }
    
    #dark #inner {
        background-color: darkgray;
    }

    button {
        border: none;
        background-color: black;
        color: white;
        padding: 0.7rem;
        border-radius: 0.5rem;
        width: 5rem;
        margin-top: 1.5rem;
    }

    button:hover {
        background-color: darkgray;
        cursor: pointer;
    }

</style>
