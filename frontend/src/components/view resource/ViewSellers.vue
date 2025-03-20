<template>
    <div id="view-sellers-container">
        <div id="view-sellers">
            <div id="exit" @click="$emit('close-view')">
                <i class="bi bi-x-lg"></i>
            </div>
            <div id="seller" v-for="resource in listed_resources">
                <div id="profile-pic">
                    <div id="profile-section" @click="view_seller(resource.user)">
                        <i class="bi bi-person-circle icon"></i>
                        <p>{{ users.find((user: User) => user.id === resource.user)?.username }}</p>
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
                        <label>Author</label>
                        <p>{{ resource.author }}</p>
                    </div>
                    <div class="data-item">
                        <label>Price</label>
                        <p>{{ Object.keys(user).length === 0 ? unauth_currency(resource as Resource) : '' }}{{ resource.price }}</p>
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
                    <div class="data-item" v-if="resource.type !== 'Stationery'">
                        <label>Pages</label>
                        <p>{{ resource.page_start }} to {{ resource.page_end }}</p>
                    </div>
                    <div class="data-item">
                        <label>Estimated Delivery</label>
                        <p>{{ parseFloat(resource.estimated_delivery_time.toString()) }} {{ resource.estimated_delivery_units }}</p>
                    </div>
                    <div class="data-item">
                        <label>Delivery Options</label>
                        <p>{{ resource.allow_collection ? 'Collection' : '' }}{{ resource.allow_collection && resource.allow_delivery ? ' & ' : '' }}{{ resource.allow_delivery ? 'Delivery' : '' }}</p>
                        <p></p>
                    </div>
                    <div class="data-item">
                        <label>Returns</label>
                        <p>{{ resource.allow_return ? 'Available' : 'Unavailable' }}</p>
                    </div>
                </div>
                <div id="buttons" v-if="Object.keys(user).length > 0">
                    <button v-if="seller !== resource.id" @click="$emit('update_seller', resource.id)">Select</button>
                    <button id="selected" v-if="seller === resource.id" @click="$emit('update_seller', resource.id)">Selected</button>
                    <button v-if="resource.user !== user.id" @click="message(resource.user)">Message</button>
                </div>
                <div id="media">
                    <img class="hoverable" :src="`${url}${resource.image1}`" alt="Image1" @click="media_clicked=`${resource.id}image1`">
                    <img class="hoverable" :src="`${url}${resource.image2}`" alt="Image2" @click="media_clicked=`${resource.id}image2`">
                    <video class="hoverable" :src="`${url}${resource.video}`" @click="media_clicked=`${resource.id}video`"></video>
                    <div class="large-media" v-if="media_clicked === `${resource.id}video`">
                        <div class="big-media" v-if="media_clicked === `${resource.id}video`">
                            <i class="bi bi-x-lg" @click="media_clicked=''"></i>
                            <video :src="`${url}${resource.video}`" controls @click="media_clicked=`${resource.id}video`"></video>
                        </div>
                    </div>
                    <div @click="media_clicked=''" class="large-media" v-if="media_clicked === `${resource.id}image1`">
                        <div class="big-media">
                            <i class="bi bi-x-lg"></i>
                            <img :src="`${url}${resource.image1}`">
                        </div>
                    </div>
                    <div @click="media_clicked=''" class="large-media" v-if="media_clicked === `${resource.id}image2`">
                        <div class="big-media" v-if="media_clicked === `${resource.id}image2`">
                            <i class="bi bi-x-lg"></i>
                            <img :src="`${url}${resource.image2}`">
                        </div>
                    </div>
                </div>
                <hr v-if="resource !== listed_resources[listed_resources.length-1]">
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, type PropType } from 'vue';
    import type { Resource, Review, User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    import { useURLStore } from '@/stores/url';
    export default defineComponent({
        emits: ['close-view', 'update_seller'],
        props: {
            resources: {
                type: Array as PropType<Resource[]>,
                required: true
            },
            seller: {
                type: Number,
                required: true
            }
        },
        data(): {
            media_clicked: string
        } { return {
            media_clicked: ''
        }},
        methods: {
            message(userID: number): void {
                // Take user to message page
                window.location.href = `/message/${this.user.id}/${userID}`
            },
            view_seller(seller_id: number): void {
                // Allow user to view seller profile
                window.location.href = this.user.id === seller_id ? '/listings' : `/seller/${this.users.find(user => user.id === seller_id)?.username}`
            },
            unauth_currency(resource: Resource): string {
                return resource.price_currency === 'GBP' ? '£' : resource.price_currency === 'USD' ? '$' : '€' 
            },
            to_date(date: string): string {
                // Convert listing date 
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
                if (Object.keys(this.user).length === 0) return resource.price
                if (resource === undefined) return 0
                // Perform currency conversion
                let convertedPrice: Response = await fetch(`${useURLStore().url}/api/currency-conversion/${resource.id}/${this.user.currency}/${resource.price_currency}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    }
                })
                if (!convertedPrice.ok) return resource.price
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return returnedPrice.new_price
            },
        },
        computed: {
            url(): string {
                return useURLStore().url
            },
            user(): User {
                const users: User = useUserStore().user
                return users
            },
            reviews(): Review[] {
                return []
            },
            users(): User[] {
                const users: User[] = useUsersStore().users
                return users
            },
            listed_resources(): Resource[] { 
                // Sort sellers based on ratings
                let sorted_resources = this.resources.sort((a, b) => {
                    const user_b: User | undefined = this.users.find(user => user.id === b.user)
                    const user_a: User | undefined = this.users.find(user => user.id === a.user)
                    if (user_b && user_a) return user_b.rating - user_a.rating
                    return 0
                })
                return sorted_resources
            }
        },
        watch: {
            async user(new_user: User): Promise<void> {
                for (const resource of this.resources) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resources(): Promise<void> {
                for (const resource of this.resources) {
                    resource.price = await this.listedprice(resource)
                }
            }
        },
        async mounted(): Promise<void> {
            for (const resource of this.resources) {
                resource.price = await this.listedprice(resource)
            }
            document.addEventListener('click', (event) => {
                // Close div on click
                const container: HTMLDivElement = event.target as HTMLDivElement
                if (container.id === 'view-sellers-container') {
                    this.$emit('close-view')
                }
                if (this.media_clicked !== '') {
                    if ((event.target as HTMLDivElement).className === 'large-media') {
                        this.media_clicked = ''
                    }
                }
            })
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

    #profile-section:hover {
        cursor: pointer;
    }

    #profile-section p:hover {
        text-decoration: underline;
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
        z-index: 2;
        background-color: rgba(0, 0, 0, 0.5);
        position: fixed;
        height: 100%;
        width: 100%;
        color: black !important;
    }

    #view-sellers {
        margin-right: 1rem;
        background-color: #D9D9D9;
        position: absolute;
        max-height: 85vh;
        width: 50rem;
        top: 1rem;
        right: 0;
        padding: 0.5rem;
        border: 0.3rem solid #D9D9D9;
        border-radius: 0.5rem;
        overflow-y: auto;
        padding-right: 1rem;
        display: flex;
        flex-direction: column;
    }

    #seller {
        display: grid;
        grid-template-areas: "profile-pic data buttons"
                             "media media media"
                             "hr hr hr";
        column-gap: 3rem;
        row-gap: 0.3rem;
    }

    #media {
        grid-area: media;
        display: flex;
        flex-direction: row;
        gap: 2rem;
        margin-top: 0.7rem;
    }

    #media img, #media video {
        border-radius: 0.5rem;
        padding: 0.5rem;
        height: 5rem;
    }

    .hoverable:hover {
        cursor: pointer;
        background-color: #999898;
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
        gap: 0.5rem;
        width: 21rem;
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

    #dark button {
        background-color: black;
        color: white;
    }

    #dark button:hover {
        background-color: darkgray !important;
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
        position: absolute;
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

    #selected {
        background-color: green !important;
        color: white;
    }

    .big-media {
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        height: 30rem;
        width: 30rem;
        position: relative;
    }

    .large-media {
        position: fixed;
        height: 100vh;
        width: 100vw;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 3;
        top: 0;
        right: 0;
        background-color: rgb(53, 53, 53, 50%);
    }

    .large-media i {
        color: red;
        font-size: 1.3rem;
        right: 1rem;
        top: 0.5rem;
        position: absolute;
        z-index: 3;
    }

    .large-media i:hover {
        cursor: pointer;
        transform: scale(1.5);
        color: darkred;
    }

    .large-media img, .large-media video {
        height: 30rem !important;
        width: 30rem !important;
        object-fit: contain !important;
        padding: 0 !important;
    }

    /* Responsive Design */
    @media (max-width: 863px) {
        #seller {
            display: grid;
            grid-template-areas: "profile-pic data"
                                "buttons buttons"
                                "media media"
                                "hr hr";
            column-gap: 0rem;
            row-gap: 1rem;
        }

        #profile-pic, #data {
            justify-self: start;
        }

        #view-sellers {
            margin-right: 1rem;
            width: 35rem;
        }

        #buttons {
            margin-top: 1rem;
            gap: 2rem;
        }

        hr {
            margin-bottom: 1.5rem;
        }
    }

    @media (max-width: 626px) {
        #seller {
            display: grid;
            grid-template-areas: "profile-pic buttons"
                                "data data"
                                "media media"
                                "hr hr";
        }

        #view-sellers {
            margin-right: 1rem;
            width: 28rem;
            padding: 1rem;
        }

        #buttons {
            margin-top: 1rem;
            flex-direction: column;
            gap: 1rem;
        }

        #data {
            margin-top: 1rem;
        }

        hr {
            margin-bottom: 1.5rem;
        }
    }

    @media (max-width: 558px) {
        .large-media img, .large-media video {
            height: 23rem !important;
            width: 23rem !important;
        }

        .big-media {
            height: 23rem;
            width: 23rem;
        }
    }

    @media (max-width: 514px) {
        #seller {
            display: grid;
            grid-template-areas: "profile-pic buttons"
                                "data data"
                                "media media"
                                "hr hr";
        }

        #view-sellers {
            padding-right: 1.5rem !important;
            width: 23rem;
            padding-left: 0.4rem;
        }

        #buttons {
            margin-top: 1rem;
            flex-direction: column;
            gap: 1rem;
        }

        #media {
            padding-bottom: 0.5rem;
            overflow-y: auto;
        }

        #data {
            justify-self: center;
            margin-top: 1rem;
        }

        hr {
            margin-bottom: 1.5rem;
        }
    }
</style>