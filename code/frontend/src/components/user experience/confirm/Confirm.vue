<template>
    <!-- Creating confirmation popup -->
    <div id="outer">
        <div id="inner">
            <p id="message">{{ message }}</p>
            <div>
                <button @click="$emit('confirm-yes')">Yes</button>
                <button @click="$emit('confirm-no')">Cancel</button>
            </div>
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
        emits: ['confirm-yes', 'confirm-no'],
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
        z-index: 100;
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

    #message {
        font-size: 1.3rem;
        color: black;
        text-align: center;
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

    #inner div {
        display: flex;
        gap: 0.5rem;
    }

    button:hover {
        background-color: darkgray;
        cursor: pointer;
    }

    /* Responsive Design */
    @media (max-width: 522px) {
        #message, button {
            font-size: 1.1rem !important;
        }

        #inner {
            width: 50%;
        }
    }

</style>
