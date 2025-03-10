<template>
    <div id="stars">
        <div class="rating">
            1
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
            </div>
            <p>{{ percent(1) }}%</p>
        </div>
        <div class="rating">
            2
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i id="two" class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
            </div>
            <p>{{ percent(2) }}%</p>
        </div>
        <div class="rating">
            3
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i id="two" class="bi bi-star-fill"></i>
                <i id="three" class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
            </div>
            <p>{{ percent(3) }}%</p>
        </div>
        <div class="rating">
            4
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i id="two" class="bi bi-star-fill"></i>
                <i id="three" class="bi bi-star-fill"></i>
                <i id="four" class="bi bi-star-fill"></i>
                <i class="bi bi-star-fill"></i>
            </div>
            <p>{{ percent(4) }}%</p>
        </div>
        <div class="rating">
            5
            <div class="stars">
                <i id="one" class="bi bi-star-fill"></i>
                <i id="two" class="bi bi-star-fill"></i>
                <i id="three" class="bi bi-star-fill"></i>
                <i id="four" class="bi bi-star-fill"></i>
                <i id="five" class="bi bi-star-fill"></i>
            </div>
            <p>{{ percent(5) }}%</p>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    export default defineComponent({
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
                const id: number = parseInt(window_location[window_location.length-1])
                const resource = useResourcesStore().resources.filter(resource => resource.id === id)
                if (!resource) return []
                if (resource[0].unique) return resource
                return useResourcesStore().resources.filter(res => resource[0].name === resource[0].name && resource[0].author && res.author && !res.unique)
            },
        },
        watch: {
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
