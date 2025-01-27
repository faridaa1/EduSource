<template>
    <div id="stars">
        <div class="rating">
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
            </div>
            <p>%</p>
        </div>
        <div class="rating">
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i id="two" class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
            </div>
            <p>%</p>
        </div>
        <div class="rating">
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i id="two" class="bi bi-star-fill"></i>
                <i id="three" class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
            </div>
            <p>%</p>
        </div>
        <div class="rating">
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i id="two" class="bi bi-star-fill"></i>
                <i id="three" class="bi bi-star-fill"></i>
                <i id="four" class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
            </div>
            <p>%</p>
        </div>
        <div class="rating">
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i id="two" class="bi bi-star-fill"></i>
                <i id="three" class="bi bi-star-fill"></i>
                <i id="four" class="bi bi-star-fill"></i>
                <i id="five" class="bi bi-star-fill"></i>
            </div>
            <p>%</p>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    export default defineComponent({
        data(): {
        } { return {
        }},
        methods: {
            fill_stars(): void {
                const star1: HTMLElement = document.getElementById('one') as HTMLElement
                const star2: HTMLElement = document.getElementById('two') as HTMLElement
                const star3: HTMLElement = document.getElementById('three') as HTMLElement
                const star4: HTMLElement = document.getElementById('four') as HTMLElement
                const star5: HTMLElement = document.getElementById('five') as HTMLElement
                if (star1 && star2 && star3 && star4 && star5) {
                    star1.style.color = (this.resource as Resource).rating >= 1 ? 'orange' : ''
                    star2.style.color = (this.resource as Resource).rating >= 2 ? 'orange' : ''
                    star3.style.color = (this.resource as Resource).rating >= 3 ? 'orange' : ''
                    star4.style.color = (this.resource as Resource).rating >= 4 ? 'orange' : ''
                    star5.style.color = (this.resource as Resource).rating == 5 ? 'orange' : ''
                }
            }
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
            resource(): Resource | {} {
                const window_location: string[] = window.location.href.split('/')
                const name: string = window_location[window_location.length-1]
                return useResourcesStore().getResource(name)
            },
        },
        watch: {
            user(new_user: User): void {
                // this.user = new_user
            },
            async resource(resource: Resource): Promise<void> {
                this.fill_stars()
            }
        },
        async mounted(): Promise<void> {
            this.fill_stars()
        }
    })
</script>

<style scoped>
    #stars {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #one, #two, #three, #four, #five {
        color: orange;
    }

    .rating {
        display: flex;
        gap: 0.5rem;
    }

    .stars {
        display: flex;
        gap: 0.1rem;
    }
</style>
