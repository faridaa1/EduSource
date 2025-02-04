<template>
    <div id="view-sellers-container">
        <div id="view-sellers">
            <div id="exit" @click="$emit('close-view')">
                <i class="bi bi-x-lg"></i>
            </div>
            <div id="seller" v-for="resource in resources">
                <div id="profile-pic">
                    <div id="profile-section">
                        <i class="bi bi-person-circle icon"></i>
                        <p>{{ resource.author }}</p>
                    </div>
                    <p>{{ to_date(resource.upload) }}</p>
                    <div id="rating">
                        <div id="stars">
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) < 1"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) >= 1" style="color: orange;"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) >= 2" style="color: orange;"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) < 2"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) >= 3" style="color: orange;"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) < 3"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) >= 4" style="color: orange;"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) < 4"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) === 5" style="color: orange;"></i>
                            <i class="bi bi-star-fill" v-if="parseFloat(resource.rating.toString()) < 5"></i>
                        </div>
                        <p>{{ parseFloat(resource.rating.toString()) }}</p>
                    </div>
                </div>
                <div id="data">
                    <div class="data-item">
                        <label>Price</label>
                        <p>{{ resource.price }}</p>
                    </div>
                    <div class="data-item">
                        <label>Condition</label>
                        <p>{{ resource.condition }}</p>
                    </div>
                    <div class="data-item">
                        <label>Media</label>
                        <p>{{ resource.media }}</p>
                    </div>
                    <div class="data-item" v-if="resource.self_made">
                        <label>Assisted Sources</label>
                        <p>{{ resource.source }}</p>
                    </div>
                </div>
                <div id="buttons">
                    <button>Select</button>
                    <button>Message</button>
                </div>
                <hr>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, type PropType } from 'vue';
    import type { Resource, Review, User } from '@/types';
    export default defineComponent({
        emits: ['close-view'],
        props: {
            resources: {
                type: Array as PropType<Resource[]>,
                required: true
            }
        },
        data(): {
        } { return {
        }},
        methods: {
            to_date(date: string): string {
                const full_date: Date = new Date(date) 
                const year = full_date.getFullYear()
                const day = full_date.getDate()
                const month_number = full_date.getMonth() + 1
                const month = 
                month_number === 1 ? 'Jan' 
                : month_number === 2 ? 'Feb'
                : month_number === 3 ? 'Mar'
                : month_number === 4 ? 'Apr'
                : month_number === 5 ? 'May'
                : month_number === 6 ? 'Jun'
                : month_number === 7 ? 'Jul'
                : month_number === 8 ? 'Aug'
                : month_number === 9 ? 'Sep'
                : month_number === 10 ? 'Oct'
                : month_number === 11 ? 'Nov'
                : 'Dec'
                return `${day} ${month} ${year}`
            },
            async listedprice(resource: Resource): Promise<number> {
                let convertedPrice: Response = await fetch(`http://localhost:8000/api/currency-conversion/${resource.id}/${this.user.currency}/${resource.price_currency}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    }
                })
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return returnedPrice.new_price
            },
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
            reviews(): Review[] {
                return []
            },
        },
        watch: {
            async user(new_user: User): Promise<void> {
                for (const resource of this.resources) {
                    resource.price = await this.listedprice(resource)
                }
            },
        },
        mounted(): void {
        }
    })
</script>

<style scoped>
    #rating {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    #profile-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    #stars {
        display: flex;
        gap: 0.2rem;
    }

    #stars i {
        font-size: 1rem !important;
    }

    hr {
        grid-area: hr;
        border: 0;
        border-top: 0.1rem solid black;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
    }

    .data-item {
        display: flex;
    }

    .data-item label {
        width: 11rem;
    }
    
    #view-sellers-container {
        z-index: 50;
        background-color: rgba(0, 0, 0, 0.5);
        position: absolute;
        height: 100%;
        width: 100%;
    }

    #view-sellers {
        margin-right: 1rem;
        background-color: #D9D9D9;
        position: absolute;
        height: 89vh;
        width: 50rem;
        top: 1rem;
        right: 0;
        padding: 0.5rem;
        border: 0.3rem solid #D9D9D9;
        border-radius: 0.5rem;
        overflow-y: scroll;
        display: flex;
        flex-direction: column;
    }

    #seller {
        display: grid;
        grid-template-areas: "profile-pic data buttons"
                             "hr hr hr";
        column-gap: 3rem;
        row-gap: 0.3rem;
    }

    #profile-pic {
        grid-area: profile-pic;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.3rem;
    }

    #profile-pic i {
        font-size: 2.5rem;
    }

    #data {
        grid-area: data;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        width: 15rem;
    }

    #buttons {
        grid-area: buttons;
        display: flex;
        align-items: center;
        gap: 1rem;
        justify-content: center;
        width: 16rem;
    }

    #buttons button {
        background-color: #0DCAF0;
        border: none;
        padding: 0.5rem;
        width: 8rem;
        border-radius: 0.5rem;
    }

    #buttons button:hover {
        cursor: pointer;
        color: white;
        background-color: #177183;
    }

    #exit {
        color: red;
        align-self: flex-end;
        transform: scale(1);
    }

    #exit i {
        font-size: 1.5rem;
    }

    #exit i:hover {
        cursor: pointer;
        color: darkred;
    }

    #exit:hover {
        transform: scale(1.5);
    }
</style>