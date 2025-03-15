<template>
    <div>
        <!-- Creating loading page -->
        <!-- https://pixabay.com/gifs/gradient-web-loader-design-online-5812/ -->
        <img src="./loading.gif" alt="Loading">
    </div>
</template>

<script lang="ts">
    import { defineComponent } from 'vue';
    export default defineComponent({
    })
</script>

<style scoped>
    div {
        height: 100vh;
        width: 100vw;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    #dark div {
        background-color: #807E7E;
    }
    
    img {
        height: 3rem;
    }
</style>
