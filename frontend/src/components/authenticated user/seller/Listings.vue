<template>
    <div id="seller-home" v-if="seller">
        <div id="user">
            <div id="profile-picture">
                <i class="bi bi-person-circle"></i>
            </div>
            <div id="user-rating">
                <p>{{ seller.username }}</p>
                <div id="rating">
                    <i id="one" class="bi bi-star-fill"></i>
                    <i id="two" class="bi bi-star-fill"></i>
                    <i id="three" class="bi bi-star-fill"></i>
                    <i id="four" class="bi bi-star-fill"></i>
                    <i id="five" class="bi bi-star-fill"></i>
                    <p>{{ seller.rating }}</p>
                </div>
                <button id="message_seller" v-if="Object.keys(user).length > 0">Message Seller</button>
            </div>
        </div>
        <div id="about-me">
            <p>Seller Description</p>
            <textarea id="desc" :v-model="user.description" disabled>{{ seller.description }}</textarea>
        </div>
        <div id="textbooks">
            <div class="header">
                <div class="viewing">
                    <p> Textbooks</p>
                </div>
            </div>
            <div class="displays">
                <p v-if="textbooks.length === 0">No textbook listings to display</p>
                <div v-for="listing in textbooks">
                    <div class="listed" @click="showResourcePage(listing.id)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Textbook">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : '' }}{{ listing.price }}
                    </div>
                </div>
            </div>
        </div>
        <div id="notes">
            <div class="header">
                <div class="viewing">
                    <p> Notes</p>
                </div>
            </div>
            <div class="displays">
                <p v-if="notes.length === 0">No note listings to display</p>
                <div v-for="listing in notes">
                    <div class="listed" @click="showResourcePage(listing.id)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Note">
                        {{ listing.price }}
                    </div>
                </div>
            </div>
        </div>
        <div id="stationery">
            <div>
                <div class="header">
                    <div class="viewing">
                        <p>Stationery</p>
                    </div>
                </div>
                <div class="displays">
                    <p v-if="stationery.length === 0">No stationery listings to display</p>
                    <div v-for="listing in stationery">
                        <div class="listed" @click="showResourcePage(listing.id)">
                            <img :src="`http://localhost:8000${listing.image1}`" alt="Stationery">
                            {{ listing.price }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Resource, User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            editingDescription: boolean
            textbookMessage: 'All' | 'Sold' | 'Drafted',
            notesMessage: 'All' | 'Sold' | 'Drafted',
            stationeryMessage: 'All' | 'Sold' | 'Drafted',
        } { return {
            editingDescription: false,
            textbookMessage: 'All',
            notesMessage: 'All',
            stationeryMessage: 'All'
        }},
        methods: {
            unauth_currency(resource: Resource): string {
                return resource.price_currency === 'GBP' ? '£' : resource.price_currency === 'USD' ? '$' : '€' 
            },
            showResourcePage(resourceId: number): void {
                window.location.href = `/view/${resourceId}`
            },
            clear(): void {
                const textarea: HTMLTextAreaElement = document.getElementById('desc') as HTMLTextAreaElement
                textarea.setCustomValidity('')
                textarea.reportValidity()
            },
            async listedprice(resource: Resource): Promise<number> {
                if (resource === undefined) return 0
                let convertedPrice: Response = await fetch(`http://localhost:8000/api/currency-conversion/${resource.id}/${this.user.currency}/${resource.price_currency}/`, {
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
            fill_stars(): void {
                nextTick(() => {
                    const star1: HTMLElement = document.getElementById('one') as HTMLElement
                    const star2: HTMLElement = document.getElementById('two') as HTMLElement
                    const star3: HTMLElement = document.getElementById('three') as HTMLElement
                    const star4: HTMLElement = document.getElementById('four') as HTMLElement
                    const star5: HTMLElement = document.getElementById('five') as HTMLElement
                    if (star1 && star2 && star3 && star4 && star5 && this.seller) {
                        star1.style.color = this.seller.rating >= 1 ? 'orange' : ''
                        star2.style.color = this.seller.rating >= 2 ? 'orange' : ''
                        star3.style.color = this.seller.rating >= 3 ? 'orange' : ''
                        star4.style.color = this.seller.rating >= 4 ? 'orange' : ''
                        star5.style.color = this.seller.rating == 5 ? 'orange' : ''
                    }
                })
            }
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
            users(): User[] {
                return useUsersStore().users
            },
            textbooks(): Resource[] {
                if (!this.seller || !this.seller.listings) return []
                return this.seller.listings.filter(listing => listing.type === 'Textbook' && !listing.is_draft)
            },
            notes(): Resource[] {
                if (!this.seller || !this.seller.listings) return []
                return this.seller.listings.filter(listing => listing.type === 'Notes' && !listing.is_draft)
            },
            stationery(): Resource[] {
                if (!this.seller || !this.seller.listings) return []
                return this.seller.listings.filter(listing => listing.type === 'Stationery' && !listing.is_draft)
            },
            seller(): User | undefined {
                const window_location: string[] = window.location.href.split('/')
                const username: string = window_location[window_location.length-1]
                return this.users.find(user => user.username === username)
            },  
        },
        watch: {
            async seller(new_seller: User): Promise<void> {
                this.fill_stars()
                if (!this.seller || Object.keys(this.user).length === 0) return
                for (const resource of this.seller.listings) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resources(resources: Resource[]): Promise<void> {
                for (const resource of resources) {
                    resource.price = await this.listedprice(resource)
                }
            }
        },
        async mounted(): Promise<void> {
            this.fill_stars()
        }
    })
</script>

<style scoped>
    #seller-home {
        display: grid;
        grid-template-areas: "user about-me"
                             "textbooks textbooks"
                             "notes stationery";
        padding-right: 30rem;
    }

    #user {
        grid-area: user;
        display: flex;
        gap: 2rem;
        align-items: center;
    }

    #user #profile-picture i {
        font-size: 4rem;
    }

    #user #user-rating {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }

    #user #user-rating p {
        font-weight: bold;
    }

    #user #rating {
        display: flex;
        gap: 0.3rem;
        align-items: center;
    }

    #user #rating i {
        font-size: 1.2rem;
    }

    #user #rating p {
        margin-left: 0.5rem;
    }

    #about-me {
        width: 30vw;
        margin: 0 !important;
        grid-area: about-me;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        padding-top: 0.3rem;
    }

    #about-me textarea {
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        max-height: 5rem;
        padding: 0.3rem;
    }

    #about-me textarea:focus {
        background-color: white;
    }

    #textbooks {
        grid-area: textbooks;
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 2rem;
        width: 98vw;
    }

    .header {
        display: flex;
        justify-content: space-between;
    }

    img {
        height: 10rem;
        width: 10rem;
        object-fit: contain;
    }

    .listed {
        display: flex;
        flex-direction: column;
        align-items: center;
    } 

    .displays {
        display: flex;
        gap: 4rem;
        overflow-x: scroll;
        margin-top: 1rem;
        padding-bottom: 1rem;
    }

    #notes {
        grid-area: notes;
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 2rem;
        margin-right: 1rem;
        width: 96.5%;
    }

    #stationery {
        grid-area: stationery;
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 2rem;
        width: 90.5%;
    }

    .header button {
        background: none;
        border: none;
    }

    .header button i {
        font-size: 2rem;
    }

    .header button:hover { 
        color: #0DCAF0;
        cursor: pointer;
    }

    #about-me div {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    #about-me div button {
        background: #0DCAF0;
        border: none;
        border-radius: 0.5rem;
        padding: 0.3rem;
    }

    #about-me div button:hover {
        background: #3b90a1;
    }

    .save {
        background-color: green !important;
        color: white;
    }

    .save:hover {
        background-color: rgb(83, 210, 83) !important;
        cursor: pointer;
    }

    .revert {
        background-color: red !important;
        color: white;
    }

    .revert:hover {
        background-color: rgb(211, 91, 91) !important;
        cursor: pointer;
    }

    .listed:hover {
        background-color: lightgray;
        border-radius: 0.5rem;
        cursor: pointer;
    }

    .viewing {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .viewing p {
        margin-right: 1rem;
    }

    .viewing button {
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    .drafted, .all {
        background-color: #0DCAF0 !important; 
    }

    #dark .drafted, #dark .all {
        background-color: white !important; 
    }

    .drafted, .all {
        background-color: #0DCAF0 !important; 
    }

    .drafted:hover, .all:hover {
        background-color: #3b90a1 !important; 
        color: black !important;
    }

    #dark .drafted:hover, #dark .all:hover {
        background-color: darkgray !important; 
    }

    #message_seller { 
        border-radius: 0.5rem;
        background-color: #0DCAF0;
        padding: 0.2rem;
        border: none;
        margin-top: 0.2rem;
    }

    #dark #message_seller { 
        background-color: white;
    }

    #message_seller:hover {
        cursor: pointer; 
        background-color: #3b90a1;
    }

    #dark #message_seller:hover { 
        background-color: darkgray;
    }
</style>