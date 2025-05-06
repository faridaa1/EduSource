<template>
    <div id="compare-container">
        <div id="header">Compare</div>
        <div id="back" @click="back">
            <i class="bi bi-arrow-left-circle-fill"></i>
            <p>Search</p>
        </div>
        <div id="border">
            <div id="main-block">
                <div id=search class="item">
                    <div class="data header"></div>
                    <div class="data search-div">
                        <div class="search">
                            <input id="item-search" placeholder="Enter Resource 1 Name" v-model="resource1_search" type="text" @input="conduct_search('resource1')" @click="update_search('resource1')" @keydown.enter="conduct_search('resource1')"><i class="bi bi-search" @click="conduct_search('resource1')"></i>
                        </div>
                        <div class="search_results" v-if="searching_resource1">
                            <div id="item-search" @click="resource1=resource; searching_resource1=false; resource1_search=resource.name" :class="(resource === resource1_search_results[0]) && (resource === resource1_search_results[resource1_search_results.length-1]) ? 'search_item rounded-top rounded-bottom' : resource === resource1_search_results[0] ? 'search_item rounded-top' : resource === resource1_search_results[resource1_search_results.length-1] ? 'search_item rounded-bottom' : 'search_item'" v-for="resource in resource1_search_results">{{ resource.name }}</div>
                        </div>
                    </div>
                    <div class="data search-div">
                        <div class="search">
                            <input id="item-search" placeholder="Enter Resource 2 Name" v-model="resource2_search" type="text" @input="conduct_search('resource2')" @click="update_search('resource2')" @keydown.enter="conduct_search('resource2')"><i class="bi bi-search" @click="conduct_search('resource2')"></i>
                        </div>
                        <div class="search_results" v-if="searching_resource2">
                            <div id="item-search" @click="resource2=resource; searching_resource2=false; resource2_search=resource.name" :class="(resource === resource2_search_results[0]) && (resource === resource2_search_results[resource2_search_results.length-1]) ? 'search_item rounded-top rounded-bottom' : resource === resource2_search_results[0] ? 'search_item rounded-top' : resource === resource2_search_results[resource2_search_results.length-1] ? 'search_item rounded-bottom' : 'search_item'" v-for="resource in resource2_search_results">{{ resource.name }}</div>
                        </div>
                    </div>
                </div>
                <div class="item" id="images">
                    <div class="data header"></div>
                    <div class="data image">
                        <img class="img" v-if="Object.keys(resource1).length > 0" :src="`${url}${resource1.image1}`" @click="view(resource1.id)">
                        <div v-else class="img"><i class="bi bi-file-image"></i></div>
                    </div>
                    <div class="data image">
                        <img class="img" v-if="Object.keys(resource2).length > 0" :src="`${url}${resource2.image1}`" @click="view(resource2.id)">
                        <div v-else class="img"><i class="bi bi-file-image"></i></div>
                    </div>
                </div>
                <hr class="divider">
                <div class="item">
                    <div class="data header">Rating</div>
                    <div class="data">
                        <p v-if="Object.keys(resource1).length>0">{{ parseFloat(resource1.rating.toString()) }} stars</p>
                    </div>
                    <div class="data">
                        <p v-if="Object.keys(resource2).length>0">{{ parseFloat(resource2.rating.toString()) }} stars</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Name</div>
                    <div class="data image">
                        <p>{{ resource1.name }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.name }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Type</div>
                    <div class="data image">
                        <p>{{ resource1.type }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.type }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Description</div>
                    <div class="data image">
                        <p>{{ resource1.description }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.description }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Listing Date</div>
                    <div class="data image">
                        <p>{{ Object.keys(resource1).length > 0 ? get_date(resource1.upload) : '' }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ Object.keys(resource2).length > 0 ? get_date(resource2.upload) : '' }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Height</div>
                    <div class="data image">
                        <p>{{ resource1.height }} {{ resource1.height_unit }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.height }} {{ resource2.height_unit }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Width</div>
                    <div class="data image">
                        <p>{{ resource1.width }} {{ resource1.width_unit }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.width }} {{ resource2.width_unit }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Weight</div>
                    <div class="data image">
                        <p>{{ resource1.weight }} {{ resource1.weight_unit }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.weight }} {{ resource2.weight_unit }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Price</div>
                    <div class="data image">
                        <p v-if="Object.keys(resource1).length > 0">{{ resource1.price }}</p>
                    </div>
                    <div class="data image">
                        <p v-if="Object.keys(resource2).length > 0">{{ resource2.price }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Estimated Delivery</div>
                    <div class="data image">
                        <p v-if="Object.keys(resource1).length>0">{{ parseFloat(resource1.estimated_delivery_time.toString()) }} {{ resource1.estimated_delivery_units }}</p>
                    </div>
                    <div class="data image">
                        <p v-if="Object.keys(resource2).length>0">{{ parseFloat(resource2.estimated_delivery_time.toString()) }} {{ resource2.estimated_delivery_units }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Subject</div>
                    <div class="data image">
                        <p>{{ resource1.subject }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.subject }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Author</div>
                    <div class="data image">
                        <p>{{ resource1.author }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.author }}</p>
                    </div>
                </div>
                <hr class="divider" v-if="(resource1.type !== 'Stationery') || (resource2.type !== 'Stationery')">
                <div class="item" id="images" v-if="(resource1.type !== 'Stationery') || (resource2.type !== 'Stationery')">
                    <div class="data header">Pages</div>
                    <div class="data image">
                        <p v-if="(Object.keys(resource1).length > 0) && (resource1.type !== 'Stationery') && (resource1.page_start === resource1.page_end) && (resource1.page_start === 1)">1</p>
                        <p v-else-if="(Object.keys(resource1).length > 0) && (resource1.type !== 'Stationery')">{{ resource1.page_start }} to {{ resource1.page_end }}</p>
                        <p v-else="(Object.keys(resource1).length > 0) && resource1.type">-</p>
                    </div>
                    <div class="data image">
                        <p v-if="(Object.keys(resource2).length > 0) && (resource2.type !== 'Stationery') && (resource2.page_start === resource2.page_end) && (resource2.page_start === 1)">1</p>
                        <p v-else-if="(Object.keys(resource2).length > 0) && (resource2.type !== 'Stationery')">{{ resource2.page_start }} to {{ resource2.page_end }}</p>
                        <p v-else="(Object.keys(resource2).length > 0) && resource2.type">-</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Color</div>
                    <div class="data image">
                        <p>{{ resource1.colour }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.colour }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Condition</div>
                    <div class="data image">
                        <p>{{ resource1.condition }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.condition }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Media</div>
                    <div class="data image">
                        <p>{{ resource1.media }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.media }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images" v-if="resource1.self_made || resource2.self_made">
                    <div class="data header">Source</div>
                    <div class="data image">
                        <p>{{ resource1.source }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.source }}</p>
                    </div>
                </div>
                <hr class="divider" v-if="resource1.self_made || resource2.self_made">
                <div class="item" id="images">
                    <div class="data header">Delivery Options</div>
                    <div class="data image">
                        <p>{{ resource1.allow_delivery ? 'Delivery': '' }}{{ resource1.allow_collection && resource1.allow_delivery ? ', ' : '' }}{{ resource1.allow_collection ? 'Collection' : '' }}</p>
                    </div>
                    <div class="data image">
                        <p>{{ resource2.allow_delivery ? 'Delivery': '' }}{{ resource2.allow_collection && resource2.allow_delivery ? ', ' : '' }}{{ resource2.allow_collection ? 'Collection' : '' }}</p>
                    </div>
                </div>
                <hr class="divider">
                <div class="item" id="images">
                    <div class="data header">Allows Returns</div>
                    <div class="data image" v-if="Object.keys(resource1).length > 0">
                        <p>{{ resource1.allow_return ? 'Yes': 'No' }}</p>
                    </div>
                    <div class="data image" v-if="Object.keys(resource2).length > 0">
                        <p>{{ resource2.allow_return ? 'Yes': 'No' }}</p>
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
    import Error from '../user experience/error/Error.vue';
    import { useURLStore } from '@/stores/url';
    export default defineComponent({
        components: { Error },
        data(): {
            resource1: Resource,
            resource2: Resource,
            resources: Resource[],
            resource1_search: string,
            resource1_search_results: Resource[],
            resource2_search_results: Resource[],
            resource2_search: string,
            search_value: string,
            searching_resource1: boolean,
            searching_resource2: boolean
        } { return {
            resource1: {} as Resource, resource2: {} as Resource,
            search_value: '',
            searching_resource1: false,
            searching_resource2: false,
            resource1_search_results: [],
            resource2_search_results: [],
            resource1_search: '',
            resource2_search: '',
            resources: [],
        }},
        async mounted(): Promise<void> {
            document.addEventListener('click', (event) => {
                // Close search results on click
                if (!event.target) return
                if (((event.target as HTMLDivElement).id !== 'item-search')) {
                    if (this.searching_resource1) this.searching_resource1 = false
                    if (this.searching_resource2) this.searching_resource2 = false
                    return
                }
            })
            const search: HTMLInputElement = document.getElementById('search') as HTMLInputElement
            if (search) {
                const window_location: string[] = window.location.href.split('/')
                const search_query: string = window_location[window_location.length-1]
                search.value = search_query.replaceAll('%20', ' ');
                this.search_value = search.value
            }
            if (!useUserStore().csrf) {
                // Store CSRF token of aunauthenticated user
                for (let cookie of document.cookie.split(';')) {
                    const cookie_pair = cookie.split('=')
                    if (cookie_pair[0].trim() === 'csrftoken') {
                        useUserStore().saveCsrf(cookie_pair[1])
                    }
                }
            }
            // Perform semnatic search to generate comparable resources
            const searchResponse = await fetch(`${useURLStore().url}/api/semantic-search/${Object.keys(this.user).length > 0 ? this.user.id : -1}/`, {
                method: 'PUT',
                credentials: 'include',
                headers: {
                    'Content-Type' : 'application/json',
                    'X-CSRFToken' : useUserStore().csrf
                },
                body: JSON.stringify(this.search_value)
            })
            if (searchResponse.ok) {
                const searchResults: Resource[] = await searchResponse.json()
                this.resources = searchResults.filter(resource => resource.stock > 0 && !resource.is_draft)
            }
        },
        methods: {
            view(id: number): void {
                window.location.href = `/view/${id}`
            },
            back(): void {
                // Take user to search page
                window.location.href = `/search/${this.search_value}`
            },
            get_date(date: string): string {
                // Formatting upload date
                const current_time = new Date()
                let date_format = new Date(date)
                if (current_time.getDate() === date_format.getDate() && current_time.getMonth() === date_format.getMonth() && current_time.getFullYear() === date_format.getFullYear()) {
                    // Show time if the day is the same
                    return `${String(date_format.getHours()).padStart(2, '0')}:${String(date_format.getMinutes()).padStart(2, '0')}`
                }
                // Show date if it happened more than one day ago
                return `${String(date_format.getDate()).padStart(2, '0')}/${String(date_format.getMonth()+1).padStart(2, '0')}/${String(date_format.getFullYear()).slice(-2)}`
            },
            update_search(resource: 'resource1' | 'resource2'): void {
                // Update which search results are being shown
                if (resource === 'resource1') {
                    // Show resource 1 search results if its search bar has been clicked
                    if (this.resource1_search.trim() === '') {
                        if (this.searching_resource1) {
                            this.searching_resource1 = false
                            return
                        }
                        this.searching_resource1 = true
                        this.resource1_search_results = this.resources.slice(0,5)
                        this.searching_resource2 = false
                        // this.searching_resource1 = false
                        return
                    }
                    this.searching_resource1 = !this.searching_resource1
                    if (this.searching_resource1) {
                        this.searching_resource2 = false
                    } 
                } else {
                    // Show resource 2 search results if its search bar has been clicked
                    if (this.resource2_search.trim() === '') {
                        if (this.searching_resource2) {
                            this.searching_resource2 = false
                            return
                        }
                        this.searching_resource2 = true
                        this.searching_resource1 = false
                        this.resource2_search_results = this.resources.slice(0,5)
                        return
                    }
                    this.searching_resource2 = !this.searching_resource2
                    if (this.searching_resource2) {
                        this.searching_resource1 = false
                    }
                }
            },
            async conduct_search(resource: 'resource1' | 'resource2'): Promise<void> {
                // Show top 5 search results 
                if (resource === 'resource1') {
                        if (this.resource1_search.trim() === '') {
                        this.searching_resource1 = false
                        this.searching_resource1 = true
                        this.resource1_search_results = this.resources.slice(0,5)
                        this.resource1_search = ''
                        return
                    }
                    this.searching_resource1 = true
                    this.searching_resource2 = false
                    let temp_resources = this.resources
                    temp_resources = temp_resources.sort((resourceA, resourceB) => {
                        // Algorithm that places most alphabetically similar first
                        if (resourceA.name === resourceB.name) return 0
                        const number_of_letters: number = this.resource1_search.length
                        let index:number = 0
                        while ((index < number_of_letters) && (resourceA.name.length >= number_of_letters) && (resourceB.name.length >= number_of_letters)) {
                            /* Go through each letter, comparing how far ASCII values deviate from search */
                            const currentSearchLetterASCII = this.resource1_search.toLocaleLowerCase().charCodeAt(index)
                            const currentALetterDifferenceASCII = (resourceA.name.toLocaleLowerCase().charCodeAt(index)) - currentSearchLetterASCII
                            const currentBLetterDifferenceASCII = (resourceB.name.toLocaleLowerCase().charCodeAt(index)) - currentSearchLetterASCII
                            if (currentALetterDifferenceASCII !== currentBLetterDifferenceASCII) {
                                return Math.abs(currentALetterDifferenceASCII) < Math.abs(currentBLetterDifferenceASCII) ? -1 : 1
                            }
                            index+=1
                        }
                        return 0
                    })
                    this.resource1_search_results = temp_resources.slice(0,5)
                } else {
                    if (this.resource2_search.trim() === '') {
                        this.searching_resource2 = false
                        this.resource2_search = ''
                        return
                    }
                    this.searching_resource2 = true
                    this.searching_resource1 = false
                    let temp_resources = this.resources
                    temp_resources = temp_resources.sort((resourceA, resourceB) => {
                        // Algorithm that places most alphabetically similar first
                        if (resourceA.name === resourceB.name) return 0
                        const number_of_letters: number = this.resource2_search.length
                        let index:number = 0
                        while ((index < number_of_letters) && (resourceA.name.length >= number_of_letters) && (resourceB.name.length >= number_of_letters)) {
                            /* Go through each letter, comparing how far ASCII values deviate from search */
                            const currentSearchLetterASCII = this.resource2_search.toLocaleLowerCase().charCodeAt(index)
                            const currentALetterDifferenceASCII = (resourceA.name.toLocaleLowerCase().charCodeAt(index)) - currentSearchLetterASCII
                            const currentBLetterDifferenceASCII = (resourceB.name.toLocaleLowerCase().charCodeAt(index)) - currentSearchLetterASCII
                            if (currentALetterDifferenceASCII !== currentBLetterDifferenceASCII) {
                                return Math.abs(currentALetterDifferenceASCII) < Math.abs(currentBLetterDifferenceASCII) ? -1 : 1
                            }
                            index+=1
                        }
                        return 0
                    })
                    this.resource2_search_results = temp_resources.slice(0,5)
                }
            },
            async listedprice(resource: Resource): Promise<number> {
                // Performing currency conversion
                if (resource === undefined) return 0
                let currency: string;
                if (Object.keys(this.user).length === 0) {
                    // if user is unauthenticated
                    if (!localStorage.getItem('currency')) {
                        localStorage.setItem('currency', 'GBP')
                    } 
                    currency = localStorage.getItem('currency') as string
                } else {
                    currency = this.user.currency
                }
                let convertedPrice: Response = await fetch(`${useURLStore().url}/api/currency-conversion/${resource.id}/${currency}/${resource.price_currency}/`, {
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
            currency(): string {
                if (Object.keys(this.user).length === 0) {
                    if (!localStorage.getItem('currency')) {
                        localStorage.setItem('currency', 'GBP')
                    } 
                    const currency = localStorage.getItem('currency')
                    return currency === 'GBP' ? '£' : currency === 'USD' ? '$' : '€' 
                }
                return this.user.currency === 'GBP' ? '£' : this.user.currency === 'USD' ? '$' : '€' 
            },
            users(): User[] {
                return useUsersStore().users
            },
            user(): User {
                return useUserStore().user
            },
        },
        watch: {
            async user(new_user: User): Promise<void> {
                for (const resource of this.user.listings) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resources(resources: Resource[]): Promise<void> {
                if (Object.keys(resources).length < 1) return
                for (const resource of resources) {
                    resource.price = await this.listedprice(resource)
                }
            },
        },
    })
</script>

<style scoped>
    #compare-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100vh;
        width: 100vw;
        margin-top: 1rem;
        gap: 1rem;
    }

    #header {
        font-size: 1.3rem;
    }

    #main-block {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        height: 84vh;
        overflow-y: auto;
        padding-right: 2rem;
    }
    .item {
        display: flex;
        gap: 1rem;
    }

    .item .data {
        width: 30vw;
    }

    #images .img {
        height: 7rem;
        padding: 0.5rem;
        background-color: #d9d9d9;
        border-radius: 0.5rem;
        width: 7rem;
        object-fit: contain;
    }

    img:hover {
        cursor: pointer;
    }

    #images i {
        padding: 0.5rem;
        font-size: 6rem;
    }

    .image {
        display: flex;
        align-items: center;
    }

    #back {
        display: flex;
        gap: 1rem;
        align-items: center;
        position: absolute;
        left: 1rem;
    }

    #back:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    #back i:hover {
        cursor: pointer;
        color: rgb(86, 85, 85);
    }

    #dark #back i:hover {
        color: rgb(206, 206, 206);
    }

    #back i {
        font-size: 1.3rem;
    }

    .search {
        display: flex;
        align-items: center;
        background-color: #d9d9d9;
        border-radius: 0.5rem;
        padding: 0.2rem;
    }

    .search i {
        padding-left: 0.3rem;
        padding-right: 0.3rem;
    }

    #dark .search i{
        color: black;
    }

    .search-div {
        position: relative;
    }

    .stars {
        display: flex;
        gap: 0.3rem;
    }

    .stars p {
        margin-left: 0.5rem;
    }

    .search_results {
        background-color: white;
        border-radius: 0.5rem;
        position: absolute;
        width: 100%;
        top: 2.3rem;
        border: 0.1rem solid darkgray;
    }

    .search_item {
        padding: 0.3rem;    
    }

    .search_item:hover {
        cursor: pointer;
        background-color: #d9d9d9;
    }

    .search i:hover {
        cursor: pointer;
    }

    .rounded-top {
        border-top-left-radius: 0.5rem;
        border-top-right-radius: 0.5rem;
    }

    .rounded-bottom {
        border-bottom-left-radius: 0.5rem;
        border-bottom-right-radius: 0.5rem;
    }

    .header {
        width: 14rem !important;
        font-size: 1.2rem;
        font-weight: bold;
    }

    #dark #compare-container {
        color: white;
    }

    #dark #compare-container .img i {
        color: black;
    }

    #dark .search_results {
        color: black;
    }

    .search input {
        background-color: #d9d9d9 !important;
        -webkit-box-shadow: 0 0 0 10000000px #d9d9d9 inset !important;
    }

    /* Responsive Design */
    @media (max-width: 855px) {
        .item .data {
            width: 24vw;
        }

        .header {
            width: 7rem !important;
            font-size: 1rem;
        }

        img, #images .img {
            height: 5.5rem !important;
            width: 5.5rem !important;
        }

        #images i {
            font-size: 4.5rem !important;
        }
    }

    @media (max-height: 824px) {
        #main-block {
            height: 80vh;
        }
    }

    @media (max-height: 615px) {
        #main-block {
            height: 75vh;
        }
    }
</style>
