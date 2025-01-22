<template>
    <div id="listings">
        <button id="new_listing" @click="new_listing"><i class="bi bi-bag-plus-fill"></i></button>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { User } from '@/types';
    export default defineComponent({
        data(): {
        } { return {
        }},
        methods: {
            new_listing():void {
                window.location.href = '/new-listing'
            }
        },
        computed: {
            user(): User {
                let user: User = useUserStore().user
                return user
            }
        },
        watch: {
            user(new_user) {
            }
        },
        mounted(): void {
        }
    })
</script>

<style scoped>
    #new_listing {
        border: none;
        background: none;
    }

    #new_listing i {
        font-size: 3rem;
        background-color: rexd;
    }

    #light #new_listing {
        color: #0DCAF0;
    }
    

    #new_listing:hover {
        cursor: pointer;
    }

    #light #new_listing:hover {
        color: #084450;
    }

    #dark #new_listing:hover {
        color: darkgray;
    }
</style>
