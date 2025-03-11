<template>
    <div>
        <!-- https://pixabay.com/gifs/gradient-web-loader-design-online-5812/ -->
        <img src="./loading.gif" alt="Loading">
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
            percent(rating: number): number {
                let sum_of_rating: number = 0
                let number_of_reviews: number = 0
                this.allResources.forEach((resource) => {
                    resource.reviews.forEach((review) => {
                        number_of_reviews +=1
                        if (review.rating == rating) {
                            sum_of_rating +=1
                        }
                })})
                if (number_of_reviews === 0) return 0
                return (sum_of_rating/number_of_reviews) * 100
            },
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
            allResources(): Resource[] {
                const window_location: string[] = window.location.href.split('/')
                const name: string = window_location[window_location.length-1]
                return useResourcesStore().resources.filter(resource => resource.name === name)
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
