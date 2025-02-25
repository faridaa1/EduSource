<template>
    <div id="seller-home" v-if="!viewing_profile || (viewing_profile && seller !== undefined)">
        <div id="user">
            <div id="profile-picture">
                <i class="bi bi-person-circle"></i>
            </div>
            <div id="user-rating">
                <p>{{ viewing_profile ? seller?.username : user.username }}</p>
                <div id="rating">
                    <i id="one" class="bi bi-star-fill"></i>
                    <i id="two" class="bi bi-star-fill"></i>
                    <i id="three" class="bi bi-star-fill"></i>
                    <i id="four" class="bi bi-star-fill"></i>
                    <i id="five" class="bi bi-star-fill"></i>
                    <p>{{ viewing_profile ? seller?.rating : user.rating }}</p>
                </div>
                <button id="message_seller" v-if="viewing_profile && Object.keys(user).length > 0">Message Seller</button>
            </div>
        </div>
        <div id="about-me">
            <p>Seller Description</p>
            <div>
                <textarea @input="clear" name="" id="desc" :v-model="user.description" :disabled="!editingDescription">{{ viewing_profile ? seller?.description : user.description }}</textarea>
                <button v-if="!viewing_profile && !editingDescription" @click="editingDescription=true"><i class="bi bi-pencil-fill"></i></button>
                <button id="save" class="save" @click="saveDescription" v-if="editingDescription"><i class="bi bi-floppy-fill"></i></button>
                <button id="revert" class="revert" v-if="editingDescription" @click="revert"><i class="bi bi-x-lg"></i></button>
            </div>
        </div>
        <div id="textbooks">
            <div class="header">
                <div class="viewing">
                    <p> {{ viewing_profile ? '' : textbookMessage }} Textbooks</p>
                    <button v-if="!viewing_profile && all_textbooks.length > 0" @click="updateTextbookMessage(true)" class="drafted">View {{ textbookMessage === 'All' ? 'Sold' : 'All'}}</button>
                    <button v-if="!viewing_profile && all_textbooks.length > 0" @click="updateTextbookMessage(false)" class="all">View {{ textbookMessage === 'All' ? 'Drafted' : textbookMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                    <select class="filter" v-if="all_textbooks.length > 0" v-model="textbook_filter">
                        <option value="listing-new">Listing: New to Old</option>
                        <option value="listing-old">Listing: Old to New</option>
                        <option v-if="!viewing_profile" value="edit-new">Edited: New to Old</option>
                        <option v-if="!viewing_profile" value="edit-old">Edited: Old to New</option>
                    </select>
                </div>
                <button v-if="!viewing_profile" @click="new_listing('textbook')"><i class="bi bi-plus-circle"></i></button>
            </div>
            <div class="displays">
                <p v-if="textbooks.length === 0">No textbook listings to display</p>
                <div v-for="listing in textbooks">
                    <div class="listed" @click="showResourcePage(listing.id)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Textbook">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
            </div>
        </div>
        <div id="notes">
            <div class="header">
                <div class="viewing">
                    <p>{{ viewing_profile ? '' :  notesMessage }} Notes</p>
                    <button v-if="!viewing_profile && all_notes.length > 0" @click="updateNotesMessage(true)" class="drafted">View {{ notesMessage === 'All' ? 'Sold' : 'All'}}</button>
                    <button v-if="!viewing_profile && all_notes.length > 0" @click="updateNotesMessage(false)" class="all">View {{ notesMessage === 'All' ? 'Drafted' : notesMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                    <select class="filter" v-if="all_notes.length > 0" v-model="notes_filter">
                        <option value="listing-new">Listing: New to Old</option>
                        <option value="listing-old">Listing: Old to New</option>
                        <option v-if="!viewing_profile" value="edit-new">Edited: New to Old</option>
                        <option v-if="!viewing_profile" value="edit-old">Edited: Old to New</option>
                    </select>
                </div>
                <button v-if="!viewing_profile" @click="new_listing('notes')"><i class="bi bi-plus-circle"></i></button>
            </div>
            <div class="displays">
                <p v-if="notes.length === 0">No note listings to display</p>
                <div v-for="listing in notes">
                    <div class="listed" @click="showResourcePage(listing.id)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Note">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
            </div>
        </div>
        <div id="stationery">
            <div>
                <div class="header">
                    <div class="viewing">
                        <p>{{ viewing_profile ? '' : stationeryMessage }} Stationery</p>
                        <button v-if="!viewing_profile && all_stationery.length > 0" @click="updateStationeryMessage(true)" class="drafted">View {{ stationeryMessage === 'All' ? 'Sold' : 'All'}}</button>
                        <button v-if="!viewing_profile && all_stationery.length > 0" @click="updateStationeryMessage(false)" class="all">View {{ stationeryMessage === 'All' ? 'Drafted' : stationeryMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                        <select class="filter" v-if="all_stationery.length > 0" v-model="stat_filter">
                            <option value="listing-new">Listing: New to Old</option>
                            <option value="listing-old">Listing: Old to New</option>
                            <option v-if="!viewing_profile" value="edit-new">Edited: New to Old</option>
                            <option v-if="!viewing_profile" value="edit-old">Edited: Old to New</option>
                        </select>
                    </div>
                    <button v-if="!viewing_profile" @click="new_listing('stationery')"><i class="bi bi-plus-circle"></i></button>
                </div>
                <div class="displays">
                    <p v-if="stationery.length === 0">No stationery listings to display</p>
                    <div v-for="listing in stationery">
                        <div class="listed" @click="showResourcePage(listing.id)">
                            <img :src="`http://localhost:8000${listing.image1}`" alt="Stationery">
                            {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
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
        mounted(): void {
            if (window.location.href.includes('seller')) {
                this.viewing_profile = true
            } else {
                this.viewing_profile = false
            }
            this.fill_stars()
        },
        data(): {
            textbook_filter: 'listing-new' | 'listing-old' | 'edit-new' | 'edit-old',
            notes_filter: 'listing-new' | 'listing-old' | 'edit-new' | 'edit-old',
            stat_filter: 'listing-new' | 'listing-old' | 'edit-new' | 'edit-old',
            viewing_profile: boolean,
            editingDescription: boolean
            textbookMessage: 'All' | 'Sold' | 'Drafted',
            notesMessage: 'All' | 'Sold' | 'Drafted',
            stationeryMessage: 'All' | 'Sold' | 'Drafted',
        } { return {
            textbook_filter: 'listing-new',
            notes_filter: 'listing-new',
            stat_filter: 'listing-new',
            viewing_profile: false,
            editingDescription: false,
            textbookMessage: 'All',
            notesMessage: 'All',
            stationeryMessage: 'All'
        }},
        methods: {
            unauth_currency(resource: Resource): string {
                return resource.price_currency === 'GBP' ? '£' : resource.price_currency === 'USD' ? '$' : '€' 
            },
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
                window.location.href = this.viewing_profile ? `/view/${resourceId}` : `/resource/${resourceId}`
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
                nextTick(() => {
                    const star1: HTMLElement = document.getElementById('one') as HTMLElement
                    const star2: HTMLElement = document.getElementById('two') as HTMLElement
                    const star3: HTMLElement = document.getElementById('three') as HTMLElement
                    const star4: HTMLElement = document.getElementById('four') as HTMLElement
                    const star5: HTMLElement = document.getElementById('five') as HTMLElement
                    if (this.viewing_profile && !this.seller) return
                    if (!this.viewing_profile && !this.user) return
                    if (star1 && star2 && star3 && star4 && star5) {
                        star1.style.color = (this.viewing_profile ? (this.seller as User).rating : this.user.rating) >= 1 ? 'orange' : ''
                        star2.style.color = (this.viewing_profile ? (this.seller as User).rating : this.user.rating) >= 2 ? 'orange' : ''
                        star3.style.color = (this.viewing_profile ? (this.seller as User).rating : this.user.rating) >= 3 ? 'orange' : ''
                        star4.style.color = (this.viewing_profile ? (this.seller as User).rating : this.user.rating) >= 4 ? 'orange' : ''
                        star5.style.color = (this.viewing_profile ? (this.seller as User).rating : this.user.rating) == 5 ? 'orange' : ''
                    }
                })
            }
        },
        computed: {
            currency(): string {
                return this.user.currency === 'GBP' ? '£' : this.user.currency === 'USD' ? '$' : '€' 
            },
            users(): User[] {
                return useUsersStore().users
            },
            seller(): User | undefined {
                const window_location: string[] = window.location.href.split('/')
                const username: string = window_location[window_location.length-1]
                return this.users.find(user => user.username === username)
            },
            user(): User {
                return useUserStore().user
            },
            all_textbooks(): Resource[] {
                if ((!this.viewing_profile && (!this.user || !this.user.listings)) || (this.viewing_profile && (!this.seller || !this.seller?.listings))) return []
                return this.viewing_profile ? (this.seller as User).listings.filter(listing => listing.type === 'Textbook') : this.user.listings.filter(listing => listing.type === 'Textbook')
            },
            all_notes(): Resource[] {
                if ((!this.viewing_profile && (!this.user || !this.user.listings)) || (this.viewing_profile && (!this.seller || !this.seller?.listings))) return []
                return this.viewing_profile ? (this.seller as User).listings.filter(listing => listing.type === 'Notes') : this.user.listings.filter(listing => listing.type === 'Notes')
            },
            all_stationery(): Resource[] {
                if ((!this.viewing_profile && (!this.user || !this.user.listings)) || (this.viewing_profile && (!this.seller || !this.seller?.listings))) return []
                return this.viewing_profile ? (this.seller as User).listings.filter(listing => listing.type === 'Stationery') : this.user.listings.filter(listing => listing.type === 'Stationery')
            },
            textbooks(): Resource[] {
                if ((!this.viewing_profile && (!this.user || !this.user.listings)) || (this.viewing_profile && (!this.seller || !this.seller?.listings))) return []
                let textbooks = this.all_textbooks
                if (this.textbookMessage === 'Sold') {
                    textbooks = this.user.listings.filter(listing => listing.type === 'Textbook' && !listing.is_draft)
                } else if (this.textbookMessage === 'Drafted') {
                    textbooks = this.user.listings.filter(listing => listing.type === 'Textbook' && listing.is_draft)
                }
                textbooks = textbooks.sort((a, b) => {
                    if (this.textbook_filter === 'edit-new') {
                        return new Date(b.last_edited).getTime() - new Date(a.last_edited).getTime() 
                    } else if (this.textbook_filter === 'edit-old') {
                        return new Date(a.last_edited).getTime()  - new Date(b.last_edited).getTime() 
                    } else if (this.textbook_filter === 'listing-new') {
                        return b.id - a.id
                    }else {
                        return a.id - b.id
                    }
                })
                if (this.viewing_profile) {
                    textbooks = textbooks.filter(listing => !listing.is_draft && listing.stock > 0)
                }
                return textbooks
            },
            notes(): Resource[] {
                if ((!this.viewing_profile && (!this.user || !this.user.listings)) || (this.viewing_profile && (!this.seller || !this.seller?.listings))) return []
                let notes = this.all_notes
                if (this.notesMessage === 'Sold') {
                    notes = this.user.listings.filter(listing => listing.type === 'Notes' && !listing.is_draft)
                } else if (this.notesMessage === 'Drafted') {
                    notes = this.user.listings.filter(listing => listing.type === 'Notes' && listing.is_draft)
                }
                notes = notes.sort((a, b) => {
                    if (this.notes_filter === 'edit-new') {
                        return new Date(b.last_edited).getTime() - new Date(a.last_edited).getTime() 
                    } else if (this.notes_filter === 'edit-old') {
                        return new Date(a.last_edited).getTime()  - new Date(b.last_edited).getTime() 
                    } else if (this.notes_filter === 'listing-new') {
                        return b.id - a.id
                    }else {
                        return a.id - b.id
                    }
                })
                if (this.viewing_profile) {
                    notes = notes.filter(listing => !listing.is_draft  && listing.stock > 0)
                }
                return notes
            },
            stationery(): Resource[] {
                if ((!this.viewing_profile && (!this.user || !this.user.listings)) || (this.viewing_profile && (!this.seller || !this.seller?.listings))) return []
                let stationery = this.all_stationery
                if (this.stationeryMessage === 'Sold') {
                    stationery = this.user.listings.filter(listing => listing.type === 'Stationery' && !listing.is_draft)
                } else if (this.stationeryMessage === 'Drafted') {
                    stationery = this.user.listings.filter(listing => listing.type === 'Stationery' && listing.is_draft)
                }
                stationery = stationery.sort((a, b) => {
                    if (this.stat_filter === 'edit-new') {
                        return new Date(b.last_edited).getTime() - new Date(a.last_edited).getTime() 
                    } else if (this.stat_filter === 'edit-old') {
                        return new Date(a.last_edited).getTime()  - new Date(b.last_edited).getTime() 
                    } else if (this.stat_filter === 'listing-new') {
                        return b.id - a.id
                    }else {
                        return a.id - b.id
                    }
                })
                if (this.viewing_profile) {
                    stationery = stationery.filter(listing => !listing.is_draft && listing.stock > 0)
                }
                return stationery
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
            },
            seller(new_seller: User) {
                this.fill_stars()
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

    .viewing button, .filter {
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    option {
        background-color: white !important;
    }

    .drafted, .all, .filter {
        background-color: #0DCAF0 !important; 
    }

    #dark .drafted, #dark .all, #dark .filter {
        background-color: white !important; 
    }

    .drafted:hover, .all:hover {
        cursor: pointer;
        background-color: #3b90a1 !important; 
        color: black !important;
    }

    .filter:hover {
        cursor: pointer;
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
