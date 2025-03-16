<template>
    <div id="seller-home" v-if="!viewing_profile || (viewing_profile && seller !== undefined)">
        <div id="user">
            <div id="profile-picture">
                <i class="bi bi-person-circle"></i>
            </div>
            <div id="user-rating">
                <p>{{ viewing_profile ? seller?.username : user.username }}</p>
                <div id="rating" v-if="!viewing_profile || (user.id !== seller?.id && seller?.listings && seller.listings.length > 0)">
                    <i id="one" class="bi bi-star-fill"></i>
                    <i id="two" class="bi bi-star-fill"></i>
                    <i id="three" class="bi bi-star-fill"></i>
                    <i id="four" class="bi bi-star-fill"></i>
                    <i id="five" class="bi bi-star-fill"></i>
                    <p>{{ viewing_profile ? seller?.rating : user.rating }}</p>
                </div>
                <button id="message_seller" @click="message((seller as User).id)" v-if="viewing_profile && Object.keys(user).length > 0">Message</button>
            </div>
        </div>
        <div id="about-me" v-if="!viewing_profile || (user.id !== seller?.id && seller?.description)">
            <p>About Me</p>
            <div>
                <textarea @input="clear" id="desc" :v-model="user.description" :disabled="!editingDescription">{{ viewing_profile ? seller?.description : user.description }}</textarea>
                <div id="buttons">
                    <button id="edit" v-if="!viewing_profile && !editingDescription" @click="editingDescription=true"><i class="bi bi-pencil-fill"></i></button>
                    <button :disabled="making_change" id="save" class="save" @click="saveDescription" v-if="editingDescription"><i class="bi bi-floppy-fill"></i></button>
                    <button :disabled="making_change" id="revert" class="revert" v-if="editingDescription" @click="revert"><i class="bi bi-x-lg"></i></button>
                </div>
            </div>
        </div>
        <div id="textbooks">
            <div class="header">
                <div class="viewing">
                    <p> {{ viewing_profile ? '' : textbookMessage }} Textbooks</p>
                    <div class="viewing-buttons">
                        <button v-if="!viewing_profile && all_textbooks.length > 0" @click="updateTextbookMessage(true)" class="drafted">View {{ textbookMessage === 'All' ? 'Sold' : 'All'}}</button>
                        <button v-if="!viewing_profile && all_textbooks.length > 0" @click="updateTextbookMessage(false)" class="all">View {{ textbookMessage === 'All' ? 'Drafted' : textbookMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                    </div>
                </div>
                <div id="absolute">
                    <select class="filter" v-if="all_textbooks.length > 0" v-model="textbook_filter">
                            <option value="listing-new">Listing: New to Old</option>
                            <option value="listing-old">Listing: Old to New</option>
                            <option v-if="!viewing_profile" value="edit-new">Edited: New to Old</option>
                            <option v-if="!viewing_profile" value="edit-old">Edited: Old to New</option>
                        </select>
                    <button v-if="!viewing_profile" @click="new_listing('textbook')"><i class="bi bi-plus-circle"></i></button>
                </div>
            </div>
            <div class="displays">
                <div class="no_resources" v-if="textbooks.length===0"> 
                    <p>No textbook listings to display</p>
                </div>
                <div v-for="listing in textbooks">
                    <div class="listed" @click="showResourcePage(listing.id)">
                        <img :src="`${url}${listing.image1}`" alt="Textbook">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
            </div>
        </div>
        <div id="notes">
            <div class="header">
                <div class="viewing">
                    <p>{{ viewing_profile ? '' :  notesMessage }} Notes</p>
                    <div class="viewing-buttons">
                            <button v-if="!viewing_profile && all_notes.length > 0" @click="updateNotesMessage(true)" class="drafted">View {{ notesMessage === 'All' ? 'Sold' : 'All'}}</button>
                        <button v-if="!viewing_profile && all_notes.length > 0" @click="updateNotesMessage(false)" class="all">View {{ notesMessage === 'All' ? 'Drafted' : notesMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                    </div>
                </div>
                <div id="absolute">
                    <select class="filter" v-if="all_notes.length > 0" v-model="notes_filter">
                        <option value="listing-new">Listing: New to Old</option>
                        <option value="listing-old">Listing: Old to New</option>
                        <option v-if="!viewing_profile" value="edit-new">Edited: New to Old</option>
                        <option v-if="!viewing_profile" value="edit-old">Edited: Old to New</option>
                    </select>
                    <button v-if="!viewing_profile" @click="new_listing('notes')"><i class="bi bi-plus-circle"></i></button>
                </div>
            </div>
            <div class="displays">
                <div class="no_resources" v-if="notes.length===0"> 
                    <p>No note listings to display</p>
                </div>
                <div v-for="listing in notes">
                    <div class="listed" @click="showResourcePage(listing.id)">
                        <img :src="`${url}${listing.image1}`" alt="Note">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
            </div>
        </div>
        <div id="stationery">
            <div class="header">
                <div class="viewing">
                    <p>{{ viewing_profile ? '' : stationeryMessage }} Stationery</p>
                    <div class="viewing-buttons">
                        <button v-if="!viewing_profile && all_stationery.length > 0" @click="updateStationeryMessage(true)" class="drafted">View {{ stationeryMessage === 'All' ? 'Sold' : 'All'}}</button>
                        <button v-if="!viewing_profile && all_stationery.length > 0" @click="updateStationeryMessage(false)" class="all">View {{ stationeryMessage === 'All' ? 'Drafted' : stationeryMessage === 'Sold' ? 'Drafted' : 'Sold' }}</button>
                    </div>
                </div>
                <div id="absolute">
                    <select class="filter" v-if="all_stationery.length > 0" v-model="stat_filter">
                        <option value="listing-new">Listing: New to Old</option>
                        <option value="listing-old">Listing: Old to New</option>
                        <option v-if="!viewing_profile" value="edit-new">Edited: New to Old</option>
                        <option v-if="!viewing_profile" value="edit-old">Edited: Old to New</option>
                    </select>
                    <button v-if="!viewing_profile" @click="new_listing('stationery')"><i class="bi bi-plus-circle"></i></button>
                </div>
            </div>
            <div class="displays">
                <div class="no_resources" v-if="stationery.length===0"> 
                    <p>No stationery listings to display</p>
                </div>
                <div v-for="listing in stationery">
                    <div class="listed" @click="showResourcePage(listing.id)">
                        <img :src="`${url}${listing.image1}`" alt="Stationery">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
            </div>
        </div>
        <div v-if="error!==''">
            <Error :message="error" @close-error="error=''"/>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Resource, User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    import { useURLStore } from '@/stores/url';
    import Error from './user experience/error/Error.vue';
    export default defineComponent({
        components: { Error },
        mounted(): void {
            if (window.location.href.includes('seller')) {
                this.viewing_profile = true
            } else {
                this.viewing_profile = false
            }
            this.fill_stars()
        },
        data(): {
            making_change: boolean,
            textbook_filter: 'listing-new' | 'listing-old' | 'edit-new' | 'edit-old',
            notes_filter: 'listing-new' | 'listing-old' | 'edit-new' | 'edit-old',
            stat_filter: 'listing-new' | 'listing-old' | 'edit-new' | 'edit-old',
            viewing_profile: boolean,
            editingDescription: boolean
            textbookMessage: 'All' | 'Sold' | 'Drafted',
            notesMessage: 'All' | 'Sold' | 'Drafted',
            stationeryMessage: 'All' | 'Sold' | 'Drafted',
            error: string,
        } { return {
            error: '',
            making_change: false,
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
            message(userID: number): void {
                // Take user to message page between themselves and the other user
                window.location.href = `/message/${this.user.id}/${userID}`
            },
            unauth_currency(resource: Resource): string {
                // Set currency to price currency when user is unauthenticated - do not get currency conversion as we would need to store such a detail
                return resource.price_currency === 'GBP' ? '£' : resource.price_currency === 'USD' ? '$' : '€' 
            },
            updateStationeryMessage(clickedByFirstButton: boolean): void {
                // Toggle message based on what user is currently viewing
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
                // Toggle message based on what user is currently viewing
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
                // Toggle message based on what user is currently viewing
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
                // Show page of resource
                window.location.href = this.viewing_profile ? `/view/${resourceId}` : `/resource/${resourceId}`
            },
            clear(): void {
                // Remove previous error message
                const textarea: HTMLTextAreaElement = document.getElementById('desc') as HTMLTextAreaElement
                textarea.setCustomValidity('')
                textarea.reportValidity()
            },
            async listedprice(resource: Resource): Promise<number> {
                // Performing currency conversion
                if (resource === undefined) return 0
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
            async saveDescription(): Promise<void> {
                // Update description
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
                // Disable buttons when API call is being made
                const saveButton: HTMLButtonElement = document.getElementById('save') as HTMLButtonElement
                saveButton.disabled = true
                const revertButton: HTMLButtonElement = document.getElementById('revert') as HTMLButtonElement
                revertButton.disabled = true
                this.making_change = true
                let updateDecriptionResponse: Response = await fetch(`${useURLStore().url}/api/user/${this.user.id}/description/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(textarea.value)
                })
                if (!updateDecriptionResponse.ok) {
                    this.making_change = false
                    this.error = 'Error updating description. Please try again.'
                    return
                } else {
                    this.making_change = false
                    const updatedUser: User = await updateDecriptionResponse.json()
                    useUserStore().saveUser(updatedUser)
                    useUsersStore().updateUser(this.user)
                    this.editingDescription = false
                }
            },
            revert(): void {
                // Revert description change to original
                const textarea: HTMLTextAreaElement = document.getElementById('desc') as HTMLTextAreaElement
                if (textarea) {
                    textarea.value = this.user.description
                    this.editingDescription = false
                }
            },
            new_listing(url: string): void {
                // Allow user to create new listing
                window.location.href = `/new-listing/${url}`
            },
            fill_stars(): void {
                // Fill seller stars
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
            url(): string {
                return useURLStore().url
            },
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
                // Textbook ordering
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
                    // Only show in stock, undrafted textbooks when viewing profile
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
                // Notes ordering
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
                    // Only show in stock, undrafted notes when viewing profile
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
                // Stationery ordering
                stationery = stationery.sort((a, b) => {
                    if (this.stat_filter === 'edit-new') {
                        return new Date(b.last_edited).getTime() - new Date(a.last_edited).getTime() 
                    } else if (this.stat_filter === 'edit-old') {
                        return new Date(a.last_edited).getTime()  - new Date(b.last_edited).getTime() 
                    } else if (this.stat_filter === 'listing-new') {
                        return b.id - a.id
                    } else {
                        return a.id - b.id
                    }
                })
                if (this.viewing_profile) {
                    // Only show in stock, undrafted stationery when viewing profile
                    stationery = stationery.filter(listing => !listing.is_draft && listing.stock > 0)
                }
                return stationery
            }
        },
        watch: {
            $route(): void {
                window.location.reload()
            },
            viewing_profile(): void {
                if (this.viewing_profile) {
                    const displays = Array.from(document.getElementsByClassName('displays'))
                    if (!displays) return
                    for (const display of displays) {
                        // Generate styles based on whether user is viewing profile
                        const parent: HTMLDivElement = (display as HTMLDivElement).parentElement as HTMLDivElement
                        if (parent && (parent.id === 'textbooks') && (this.textbooks.length > 0)) {
                            (display as HTMLDivElement).style.setProperty('height', 'auto', 'important')
                        } else if (parent && (parent.id === 'textbooks') && (this.textbooks.length === 0)){
                            (display as HTMLDivElement).style.setProperty('height', '70%', 'important')
                        } if (parent && (parent.id === 'notes') && (this.notes.length > 0)) {
                            (display as HTMLDivElement).style.setProperty('height', 'auto', 'important')
                        } else if (parent && (parent.id === 'notes') && (this.notes.length === 0)){
                            (display as HTMLDivElement).style.setProperty('height', '70%', 'important')
                        } if (parent && (parent.id === 'stationery') && (this.stationery.length > 0)) {
                            (display as HTMLDivElement).style.setProperty('height', 'auto', 'important')
                        } else if (parent && (parent.id === 'stationery') && (this.stationery.length === 0)){
                            (display as HTMLDivElement).style.setProperty('height', '70%', 'important')
                        } 
                    }
                    const viewings = Array.from(document.getElementsByClassName('viewing'))
                    if (!viewings) return
                    for (const viewing of viewings) {
                        (viewing as HTMLDivElement).style.setProperty('flex-direction', 'row', 'important')
                        const child: HTMLParagraphElement = viewing.firstElementChild as HTMLParagraphElement
                        if (!child) return
                        child.style.setProperty('margin-top', '0rem', 'important')
                    }
                    const textbooks: HTMLDivElement = document.getElementById('textbooks') as HTMLDivElement
                    if (!textbooks) return
                    textbooks.style.setProperty('height', '12.5rem', 'important')
                    const notes: HTMLDivElement = document.getElementById('notes') as HTMLDivElement
                    if (!notes) return
                    notes.style.setProperty('height', '12.5rem', 'important')
                    const stationery: HTMLDivElement = document.getElementById('stationery') as HTMLDivElement
                    if (!stationery) return
                    stationery.style.setProperty('height', '12.5rem', 'important')
                }
            },
            async user(new_user: User): Promise<void> {
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
            seller() {
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
                             "notes notes"
                             "stationery stationery";
        height: 89vh;
        width: 98vw;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        overflow-y: auto;
        gap: 1.5rem;
    }

   #textbooks, #notes, #stationery {
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        height: 12.5rem;
        margin-left: 1.5rem;
        margin-right: 1.5rem;
        padding: 0.5rem;
        padding-bottom: 0rem;
    }

    #user {
        margin-left: 1.5rem;
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
        width: 100%;
        grid-area: about-me;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        padding-top: 0.3rem;
        margin-right: 1.5rem;
    }

    #dark #edit {
        background-color: black;
    }

    #about-me textarea {
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        max-height: 5rem;
        resize: none;
        padding: 0.3rem;
    }

    #about-me textarea:focus {
        background-color: white;
    }

    #textbooks {
        grid-area: textbooks;
    }

    .header {
        display: flex;
        justify-content: space-between;
        position: relative;
    }

    #absolute {
        position: absolute;
        top: 0;
        right: 0.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    img {
        margin-top: 0.4rem;
        height: 7rem;
        width: 7rem;
        object-fit: contain;
    }

    .no_resources {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .listed {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0.3rem;
    } 

    .displays {
        display: flex;
        gap: 3rem;
        overflow-x: auto;
        padding-bottom: 1rem;
        height: 70%;
    }

    #notes {
        grid-area: notes;
    }

    #stationery {
        grid-area: stationery;
    }

    .header button {
        background: none;
        border: none;
    }

    #buttons {
        align-self: flex-end;
    }

    .header button i {
        font-size: 2rem;
    }

    .header button:hover { 
        color: #0DCAF0;
        cursor: pointer;
    }

    button:hover {
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

    textarea:disabled {
        color: black;
    }

    #dark .listed:hover {
        color: black;
    }

    .viewing-buttons {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .viewing {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .viewing-buttons button, .filter {
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    option {
        background-color: white !important;
    }

    #desc {
        height: 5rem;
        width: 90%;
    }

    #dark #seller-home, #dark i {
        color: white;
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
        width: 8rem;
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

    button:disabled, button:disabled:hover {
        background-color: darkgray !important;
        cursor: not-allowed;
    }

    /* Responsive Design */

    @media (max-width: 658px) {
        .viewing {
            flex-direction: column;
            gap: 1rem;
            margin-left: 0.5rem;
            align-items: start;
        }

        #textbooks, #notes, #stationery {
            height: 15rem;
        }

        .displays {
            height: 57%;
        }

        #seller-home {
            display: grid;
            grid-template-areas: "user"
                                "about-me"
                                "textbooks"
                                "notes"
                                "stationery";
            width: 98vw;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }

        #about-me {
            width: 92%;
            margin-left: 1.5rem;
            padding-top: 0 !important;
            padding-right: 0 !important;
        }

        #desc {
            width: 100%;
        }

        .viewing p {
            margin-top: 0.5rem;
        }
    }

    @media (max-width: 546px) {
        .viewing-buttons {
            margin-top: 0.1rem;
        }

        #textbooks, #notes, #stationery {
            height: 15.5rem;
        }

        .displays {
            height: 55%;
        }
    }

    @media (max-width: 510px) {
        #textbooks, #notes, #stationery {
            width: 83vw;
        }
    }

    @media (max-width: 491px) {
        #textbooks, #notes, #stationery {
            width: 80vw;
        }
    }
</style>
