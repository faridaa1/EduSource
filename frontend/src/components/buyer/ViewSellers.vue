<template>
    <div id="view-sellers">
        <div id="seller" v-for="resource in resources">
            <div id="profile-pic">
                <i class="bi bi-person-circle icon"></i>
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
                <div>
                    <label>Price</label>
                    <p>{{ resource.price }}</p>
                </div>
                <div>
                    <label>Condition</label>
                    <p>{{ resource.condition }}</p>
                </div>
                <div>
                    <label>Media</label>
                    <p>{{ resource.media }}</p>
                </div>
                <div>
                    <label>Source</label>
                    <p>{{ resource.source }}</p>
                </div>
            </div>
            <div id="buttons">
                <button>Select</button>
                <button>Contact Seller</button>
            </div>
            <hr>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick, watch, type PropType } from 'vue';
    import type { Resource, Review, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    export default defineComponent({
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
            allResources(): Resource[] {
                return useResourcesStore().resources
                // const window_location: string[] = window.location.href.split('/')
                // const name: string = window_location[window_location.length-1]
                // return useResourcesStore().resources.filter(resource => resource.name === name)
            },
        },
        watch: {
            async user(new_user: User): Promise<void> {
                for (const resource of this.allResources) {
                    resource.price = await this.listedprice(resource)
                }
            },
            allResources(newResources: Resource[]) {
            }
        },
        mounted(): void {
            console.log('hi')
        },
    })
</script>

<style scoped>
    #rating {
        display: flex;
        align-items: center;
        gap: 0.5rem;
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

    #view-sellers {
        background-color: #D9D9D9;
        position: absolute;
        height: 95vh;
        width: 50vw;
        top: 1.8rem;
        right: 0;
        border-radius: 1rem;
        padding: 0.5rem;
        border: 0.1rem solid black;
        overflow-y: scroll;
    }

    #seller {
        display: grid;
        grid-template-areas: "profile-pic data buttons"
                             "hr hr hr";
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
        font-size: 3rem;
    }

    #data {
        grid-area: data;
    }

    #buttons {
        grid-area: buttons;
    }
</style>