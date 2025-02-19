<template>
    <div id="seller-home">
        <div id="user">
            <div id="profile-picture">
                <i class="bi bi-person-circle"></i>
            </div>
            <div id="user-rating">
                <p>{{ user.username }}</p>
                <div id="rating">
                    <i id="one" class="bi bi-star-fill"></i>
                    <i id="two" class="bi bi-star-fill"></i>
                    <i id="three" class="bi bi-star-fill"></i>
                    <i id="four" class="bi bi-star-fill"></i>
                    <i id="five" class="bi bi-star-fill"></i>
                    <p>{{ user.rating }}</p>
                </div>
            </div>
        </div>
        <div id="about-me">
            <p>Seller Description</p>
            <div>
                <textarea @input="clear" name="" id="desc" :v-model="user.description" :disabled="!editingDescription">{{ user.description }}</textarea>
                <button v-if="!editingDescription" @click="editingDescription=true"><i class="bi bi-pencil-fill"></i></button>
                <button id="save" class="save" @click="saveDescription" v-if="editingDescription"><i class="bi bi-floppy-fill"></i></button>
                <button id="revert" class="revert" v-if="editingDescription" @click="revert"><i class="bi bi-x-lg"></i></button>
            </div>
        </div>
        <div id="textbooks">
            <div class="header">
                <div class="viewing">
                    <p> {{ textbookMessage }} Textbooks</p>
                    <button v-if="all_textbooks.length > 0" @click="updateTextbookMessage(true)" class="drafted">View {{ textbookMessage === 'All' ? 'Sold' : 'All'}}</button>
                    <button v-if="all_textbooks.length > 0" @click="updateTextbookMessage(false)" class="all">View {{ textbookMessage === 'All' ? 'Drafted' : textbookMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                </div>
                <button @click="new_listing('textbook')"><i class="bi bi-plus-circle"></i></button>
            </div>
            <div class="displays">
                <p v-if="textbooks.length === 0">No textbook listings to display</p>
                <div v-for="listing in textbooks">
                    <div class="listed" @click="showResourcePage(listing.id)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Textbook">
                        {{ listing.price }}
                    </div>
                </div>
            </div>
        </div>
        <div id="notes">
            <div class="header">
                <div class="viewing">
                    <p>{{ notesMessage }} Notes</p>
                    <button v-if="all_notes.length > 0" @click="updateNotesMessage(true)" class="drafted">View {{ notesMessage === 'All' ? 'Sold' : 'All'}}</button>
                    <button v-if="all_notes.length > 0" @click="updateNotesMessage(false)" class="all">View {{ textbookMessage === 'All' ? 'Drafted' : notesMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                </div>
                <button @click="new_listing('notes')"><i class="bi bi-plus-circle"></i></button>
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
                        <p>{{ stationeryMessage }} Stationery</p>
                        <button v-if="all_stationery.length > 0" @click="updateStationeryMessage(true)" class="drafted">View {{ stationeryMessage === 'All' ? 'Sold' : 'All'}}</button>
                        <button v-if="all_stationery.length > 0" @click="updateStationeryMessage(false)" class="all">View {{ stationeryMessage === 'All' ? 'Drafted' : stationeryMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                    </div>
                    <button @click="new_listing('stationery')"><i class="bi bi-plus-circle"></i></button>
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
    import { defineComponent } from 'vue';
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
            updateStationeryMessage(clickedByFirstButton: boolean): void {
                if (clickedByFirstButton) {
                    if (this.stationeryMessage === 'All') {
                        this.stationeryMessage = 'Sold'
                    } else {
                        this.stationeryMessage = 'All'
                    }
                } else {
                    if (this.stationeryMessage === 'Drafted') {
                        this.stationeryMessage = 'Sold'
                    } else {
                        this.stationeryMessage = 'Drafted'
                    }
                }
            },
            updateNotesMessage(clickedByFirstButton: boolean): void {
                if (clickedByFirstButton) {
                    if (this.notesMessage === 'All') {
                        this.notesMessage = 'Sold'
                    } else {
                        this.notesMessage = 'All'
                    }
                } else {
                    if (this.notesMessage === 'Drafted') {
                        this.notesMessage = 'Sold'
                    } else {
                        this.notesMessage = 'Drafted'
                    }
                }
            },
            updateTextbookMessage(clickedByFirstButton: boolean): void {
                if (clickedByFirstButton) {
                    if (this.textbookMessage === 'All') {
                        this.textbookMessage = 'Sold'
                    } else {
                        this.textbookMessage = 'All'
                    }
                } else {
                    if (this.textbookMessage === 'Drafted') {
                        this.textbookMessage = 'Sold'
                    } else {
                        this.textbookMessage = 'Drafted'
                    }
                }
            },
            showResourcePage(resourceId: number): void {
                window.location.href = `/resource/${resourceId}`
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
                let returnedPrice: {new_price: number} = await convertedPrice.json()
                return returnedPrice.new_price
            },
            async saveDescription(): Promise<void> {
                const textarea: HTMLTextAreaElement = document.getElementById('desc') as HTMLTextAreaElement
                if (textarea.value.length === 0) {
                    textarea.setCustomValidity('Cannot be empty')
                    textarea.reportValidity()
                    return
                } else if (!textarea.value.match(/^[a-zA-Z0-9]+(( [a-zA-Z0-9]+)*(: [a-zA-Z0-9]+)*(- [a-zA-Z0-9]+)*('[a-zA-Z0-9]+)*(, [a-zA-Z0-9]+)*(\([a-zA-Z0-9]+\))*(\[[a-zA-Z0-9]+\])*("[a-zA-Z0-9]+")*)*$/)) {
                    textarea.setCustomValidity('Incorrect format')
                    textarea.reportValidity()
                    return
                }
                const saveButton: HTMLButtonElement = document.getElementById('save') as HTMLButtonElement
                saveButton.disabled = true
                const revertButton: HTMLButtonElement = document.getElementById('revert') as HTMLButtonElement
                revertButton.disabled = true
                let updateDecriptionResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/description/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                    'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(textarea.value)
                })
                if (!updateDecriptionResponse.ok) {
                    console.error('Error updating description')
                    alert('Error updating description')
                    return
                }
                const updatedUser: User = await updateDecriptionResponse.json()
                useUserStore().saveUser(updatedUser)
                useUsersStore().updateUser(this.user)
                this.editingDescription = false
            },
            revert(): void {
                const textarea: HTMLTextAreaElement = document.getElementById('desc') as HTMLTextAreaElement
                if (textarea) {
                    textarea.value = this.user.description
                    this.editingDescription = false
                }
            },
            new_listing(url: string): void {
                window.location.href = `/new-listing/${url}`
            },
            fill_stars(): void {
                const star1: HTMLElement = document.getElementById('one') as HTMLElement
                const star2: HTMLElement = document.getElementById('two') as HTMLElement
                const star3: HTMLElement = document.getElementById('three') as HTMLElement
                const star4: HTMLElement = document.getElementById('four') as HTMLElement
                const star5: HTMLElement = document.getElementById('five') as HTMLElement
                if (star1 && star2 && star3 && star4 && star5) {
                    star1.style.color = this.user.rating >= 1 ? 'orange' : ''
                    star2.style.color = this.user.rating >= 2 ? 'orange' : ''
                    star3.style.color = this.user.rating >= 3 ? 'orange' : ''
                    star4.style.color = this.user.rating >= 4 ? 'orange' : ''
                    star5.style.color = this.user.rating == 5 ? 'orange' : ''
                }
            }
        },
        computed: {
            user(): User {
                let user: User = useUserStore().user
                return user
            },
            all_textbooks(): Resource[] {
                if (!this.user || !this.user.listings) return []
                return this.user.listings.filter(listing => listing.type === 'Textbook')
            },
            all_notes(): Resource[] {
                if (!this.user || !this.user.listings) return []
                return this.user.listings.filter(listing => listing.type === 'Notes')
            },
            all_stationery(): Resource[] {
                if (!this.user || !this.user.listings) return []
                return this.user.listings.filter(listing => listing.type === 'Stationery')
            },
            textbooks(): Resource[] {
                if (!this.user || !this.user.listings) return []
                if (this.textbookMessage === 'All') {
                    return this.user.listings.filter(listing => listing.type === 'Textbook')
                } else if (this.textbookMessage === 'Sold') {
                    return this.user.listings.filter(listing => listing.type === 'Textbook' && !listing.is_draft)
                }
                return this.user.listings.filter(listing => listing.type === 'Textbook' && listing.is_draft)
            },
            notes(): Resource[] {
                if (!this.user || !this.user.listings) return []
                if (this.notesMessage === 'All') {
                    return this.user.listings.filter(listing => listing.type === 'Notes')
                } else if (this.notesMessage === 'Sold') {
                    return this.user.listings.filter(listing => listing.type === 'Notes' && !listing.is_draft)
                }
                return this.user.listings.filter(listing => listing.type === 'Notes' && listing.is_draft)
            },
            stationery(): Resource[] {
                if (!this.user || !this.user.listings) return []
                if (this.stationeryMessage === 'All') {
                    return this.user.listings.filter(listing => listing.type === 'Stationery')
                } else if (this.stationeryMessage === 'Sold') {
                    return this.user.listings.filter(listing => listing.type === 'Stationery' && !listing.is_draft)
                }
                return this.user.listings.filter(listing => listing.type === 'Stationery' && listing.is_draft)
            }
        },
        watch: {
            async user(new_user: User): Promise<void> {
                // this.user = new_user
                this.fill_stars()
                for (const resource of this.user.listings) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resources(resources: Resource[]): Promise<void> {
                for (const resource of resources) {
                    resource.price = await this.listedprice(resource)
                }
            }
        },
        async created(): Promise<void> {
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
        width: fit-content;
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
</style>
