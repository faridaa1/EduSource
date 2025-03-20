<template>
    <div id="stars">
        <div class="rating">
            1
            <div class="stars">
                <i id="one" class="bi bi-star-fill" style="color: orange;"></i>
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
                <i id="one" class="bi bi-star-fill" ></i>
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
    import { defineComponent, type PropType } from 'vue';
    import type { Resource, User } from '@/types';
    export default defineComponent({
        props: {
            allResources: {
                type: Array as PropType<Resource[]>,
                required: true
            }
        },
        methods: {
            percent(rating: number): number {
                // Find the percentage of reviews with a certain number of stars
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
                return parseInt(((sum_of_rating/number_of_reviews) * 100).toString())
            },
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
        },
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
