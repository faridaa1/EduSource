<template>
    <div id="search-container">
        <div id="search-heading">
            <div id="heading1">
                <p>Search Results</p>
            </div>
            <div id="heading2">
                <div id="sort_by" v-if="filtered_resources.length > 0">
                    <label id="label">Sort by</label>
                    <select v-model="sort_by">
                        <option value="listing-new">Listing: New to Old</option>
                        <option value="listing-old">Listing: Old to New</option>
                        <option value="rating-low">Rating: Low to High</option>
                        <option value="rating-high">Rating: High to Low</option>
                        <option value="price-low" v-if="Object.keys(user).length > 0">Price: Low to High</option>
                        <option value="price-high" v-if="Object.keys(user).length > 0">Price: High to Low</option>
                    </select>
                </div>
                <div id="filter">
                    <label id="label">Filter <i class="bi bi-sliders" @click="filtering=!filtering"></i></label>
                    <div id="filter-area" v-if="filtering">
                        <div id="condition">
                            <label>Condition</label>
                            <p :class="condition_new ? 'new' : 'not'" @click="condition_new=!condition_new">New</p>
                            <p :class="condition_used ? 'used' : 'not'" @click="condition_used=!condition_used">Used</p>
                        </div>
                        <div id="rating">
                            <label>Rating</label>
                            <div>
                                <p :class="rating_all ? 'new' : 'not'" @click="() => { rating_all=!rating_all, one=true; two=true; three=true; four=true; five=true } ">All</p>
                                <p :class="one ? 'new' : 'not'" @click="() => {one=!one; check_all()}">1</p>
                                <p :class="two ? 'used' : 'not'" @click="() => {two=!two; check_all()}">2</p>
                                <p :class="three ? 'used' : 'not'" @click="() => {three=!three; check_all()}">3</p>
                                <p :class="four ? 'used' : 'not'" @click="() => {four=!four; check_all()}">4</p>
                                <p :class="five ? 'used' : 'not'" @click="() => {five=!five; check_all()}">5</p>
                            </div>
                        </div>
                        <div id="type">
                            <label>Type</label>
                            <div>
                                <p :class="type_all ? 'new' : 'not'" @click="() => { type_all=!type_all, textbook=true; notes=true; stationery=true } ">All</p>
                                <p :class="textbook ? 'new' : 'not'" @click="() => {textbook=!textbook; check_type_all()}">Textbook</p>
                                <p :class="notes ? 'used' : 'not'" @click="() => {notes=!notes; check_type_all()}">Notes</p>
                                <p :class="stationery ? 'used' : 'not'" @click="() => {stationery=!stationery; check_type_all()}">Stationery</p>
                            </div>
                        </div>
                        <div v-if="Object.keys(user).length > 0" class="filter-row">
                            <label>Price</label>
                            <div id="price-filter">
                                <input type="number" min="0" step="0.01" v-model="min_price">
                                <p>to</p>
                                <input type="number" :min="min_price" step="0.01" v-model="max_price">
                            </div>
                        </div>
                        <!-- 
            'height': self.height,
            'width': self.width,
            'weight': self.weight,
            'price': self.price,
            'estimated_delivery_time': self.estimated_delivery_time,
            'subject': self.subject,
            'author': self.author,
            'self_made': self.self_made,
            'page_start': self.page_start,
            'page_end': self.page_end,
            'height_unit': self.height_unit,
            'width_unit': self.width_unit,
            'estimated_delivery_units': self.estimated_delivery_units,
            'type': self.type,
            subject
            'colour': self.colour,
            'source': self.source,
            'media': self.media,
            'allow_delivery': self.allow_delivery,
            'allow_collection': self.allow_collection,
            'allow_return': self.allow_return, -->
                    </div>
                </div>
            </div>
        </div>
        <div id="search-content">
            <div id="noresources" v-if="filtered_resources.length === 0">No resources found</div>
            <div class="search-item" v-for="resource in filtered_resources" @click="showResourcePage(resource.id)">
                <div id="search-picture">
                    <img :src="`http://localhost:8000${resource.image1}`" alt="">
                </div>
                <div id="search-data">
                    <p>{{ resource.name }}</p>
                    <p>{{ Object.keys(user).length > 0 ? currency : unauth_currency(resource) }}{{ Object.keys(user).length > 0 ? parseFloat(resource.price.toString().replace('€','').replace('£','').replace('$','')).toFixed(2) : parseFloat(resource.price.toString()).toFixed(2) }}</p>
                    <div id="stars">
                        <p>{{ resource.rating }}</p>
                        <i v-if="resource.rating > 0" class="bi bi-star-fill" style="color: orange;"></i>
                        <i v-if="resource.rating < 1" class="bi bi-star-fill"></i>
                        <i v-if="resource.rating > 1" class="bi bi-star-fill" style="color: orange;"></i>
                        <i v-if="resource.rating < 2" class="bi bi-star-fill"></i>
                        <i v-if="resource.rating > 2" class="bi bi-star-fill" style="color: orange;"></i>
                        <i v-if="resource.rating < 3" class="bi bi-star-fill"></i>
                        <i v-if="resource.rating > 3" class="bi bi-star-fill" style="color: orange;"></i>
                        <i v-if="resource.rating < 4" class="bi bi-star-fill"></i>
                        <i v-if="resource.rating > 4" class="bi bi-star-fill" style="color: orange;"></i>
                        <i v-if="resource.rating < 5" class="bi bi-star-fill"></i>
                    </div>
                </div>
                <div v-if="Object.keys(user).length > 0">
                </div>
                <div v-if="Object.keys(user).length > 0">
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
            resources: Resource[],
            search_value: string,
            sorting: boolean,
            one: boolean, 
            two: boolean,
            three: boolean,
            four: boolean,
            five: boolean,
            min_price: number,
            max_price: number,
            rating_all: boolean,
            type_all: boolean,
            textbook: boolean,
            notes: boolean,
            stationery: boolean,
            filtering: boolean,
            condition_new: boolean,
            condition_used: boolean, 
            sort_by: 'listing-new' | 'listing-old' | 'rating-low' | 'rating-high' | 'price-low' | 'price-high'
        } { return {
            search_value: '',
            one: true,
            two: true,
            min_price: 0,
            max_price: 100,
            three: true,
            four: true,
            five: true,
            rating_all: true,
            type_all: true,
            textbook: true,
            stationery: true,
            notes: true,
            resources: [],
            condition_new: true,
            condition_used: true,
            sorting: false,
            filtering: false,
            sort_by: 'listing-new'
        }},
        async mounted(): Promise<void> {
            const search: HTMLInputElement = document.getElementById('search') as HTMLInputElement
            if (search) {
                const window_location: string[] = window.location.href.split('/')
                const search_query: string = window_location[window_location.length-1]
                search.value = search_query.replaceAll('%', ' ');
                this.search_value = search.value
            }
            if (!useUserStore().csrf) {
                // unauth
                for (let cookie of document.cookie.split(';')) {
                    const cookie_pair = cookie.split('=')
                    if (cookie_pair[0] === 'csrftoken') {
                        useUserStore().saveCsrf(cookie_pair[1])
                    }
                }
            }
            const searchResponse = await fetch(`http://localhost:8000/api/semantic-search/`, {
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
                this.sort_resources()
            }
        },
        methods: {
            check_all(): void {
                if (this.one && this.two && this.three && this.four && this.five) {
                    this.rating_all = true
                } else {
                    this.rating_all = false
                }
            },
            check_type_all(): void {
                if (this.textbook && this.notes && this.stationery) {
                    this.type_all = true
                } else {
                    this.type_all = false
                }
            },
            message(userID: number): void {
                window.location.href = `/message/${this.user.id}/${userID}`
            },
            unauth_currency(resource: Resource): string {
                return resource.price_currency === 'GBP' ? '£' : resource.price_currency === 'USD' ? '$' : '€' 
            },
            showResourcePage(resourceId: number): void {
                window.location.href = `/view/${resourceId}` 
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
            sort_resources(): void {
                this.resources.sort((a,b) => {
                    if (this.sort_by === 'listing-new') {
                        return new Date(b.upload).getTime() - new Date(a.upload).getTime()
                    } else if (this.sort_by === 'listing-old') {
                        return new Date(a.upload).getTime() - new Date(b.upload).getTime()
                    } else if (this.sort_by === 'rating-high') {
                        return b.rating - a.rating
                    } else if (this.sort_by === 'rating-low') {
                        return a.rating - b.rating
                    } else if (this.sort_by === 'price-high') {
                        return b.price - a.price
                    }
                    return a.price - b.price
                })
            },
        },
        computed: {
            currency(): string {
                return this.user.currency === 'GBP' ? '£' : this.user.currency === 'USD' ? '$' : '€' 
            },
            users(): User[] {
                return useUsersStore().users
            },
            user(): User {
                return useUserStore().user
            },
            filtered_resources(): Resource[] {
                let seen_resources: { [key: string]: string } = {}
                let temp_resources = []
                for (let resource of this.resources) {
                    if (resource.unique) {
                        temp_resources.push(resource) 
                        continue
                    }
                    if (temp_resources.find(res => res.name === resource.name && resource.author === res.author && !resource.unique)) {
                        continue
                    } else {
                        temp_resources.push(resource) 
                    }
                }
                return temp_resources.filter(resource => {
                    if (
                        ((parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€','')) >= this.min_price)
                        && (parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€','')) <= this.max_price))
                        && (this.condition_new && resource.condition === 'New'
                        || this.condition_used && resource.condition === 'Used'
                        || this.rating_all
                        || this.type_all
                        || (this.one && resource.rating >= 1)
                        || (this.two && resource.rating >= 2)
                        || (this.three && resource.rating >= 3)
                        || (this.four && resource.rating >= 4)
                        || (this.five && resource.rating >= 5)
                        || (this.textbook && resource.type === 'Textbook')
                        || (this.stationery && resource.type === 'Stationery')
                        || (this.notes && resource.type === 'Notes'))
                    ) {
                        console.log(
                            (parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€','')) >= this.min_price)
                        && (parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€','')) <= this.max_price)
                        )
                        return true
                    }  
                    return false
                })
            }
        },
        watch: {
            async user(new_user: User): Promise<void> {
                for (const resource of this.user.listings) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resources(resources: Resource[]): Promise<void> {
                if (Object.keys(this.user).length < 1 || Object.keys(resources).length < 1) return
                for (const resource of resources) {
                    resource.price = await this.listedprice(resource)
                }
            },
            sort_by(): void {
                this.sort_resources()
            },
            min_price(): void {
                if (this.min_price.toString() === '' || this.min_price < 0) this.min_price = 0
                if (this.min_price > this.max_price) {
                    this.max_price = this.min_price
                } 
            },
            max_price(): void {
                if (this.max_price.toString() === '' || this.max_price < 0) this.max_price = 0
                if (this.min_price > this.max_price) {
                    this.min_price = this.max_price
                }
            }
        },
    })
</script>

<style scoped>
    img {
        width: 10rem;
    }

    #stars {
        display: flex;
        gap: 0.2rem;
    }

    #price-filter {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    #price-filter input {
        text-align: center;
        width: 5rem;
    }

    input {
        border-radius: 0.5rem;
    }

    #search-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        margin: 1rem;
        color: white;
    }

    #search-heading {
        display: flex;
        justify-content: space-between;
    }

    #heading1 p, #heading2 #label, #filter i {
        font-size: 1.5rem;
    }

    #heading2 {
        display: flex;
        gap: 2rem;
    }

    select {
        padding: 0.4rem;
        font-size: 1.3rem;
        border-radius: 0.5rem;
        background-color: #d9d9d9;
        border: none;
    }

    option {
        font-size: 1.3rem;
    }

    #sort_by {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    #search-content {
        height: 88vh;
        overflow-y: auto;
    }

    select:hover {
        cursor: pointer;
    }

    #filter i:hover, .new:hover, .used:hover, .not:hover {
        cursor: pointer;
    }

    #filter-area {
        height: 30rem;
        position: absolute;
        background-color: white;
        overflow-y: auto;
        padding: 0.5rem;
        border-radius: 0.8rem;
        right: 3rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        border: 0.1rem solid black;
    }

    #dark #filter-area {
        background-color: rgb(41, 41, 41);
        border: 0.1rem solid white;
    }

    #condition {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .new, .used {
        background-color: green;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    #dark .new, #dark .used {
        background-color: #d9d9d9;
        color: black;
    }

    .new:hover, .used:hover {
        background-color: rgb(97, 205, 97);
    }

    #dark .new:hover, #dark .used:hover{
        background-color: darkgray;
    }

    .not {
        background-color: #d9d9d9;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    #dark .not {
        background-color: darkgray;
        color: black;
    }

    .not:hover {
        background-color: green;
        color: white;
    }

    #dark .not:hover {
        background-color: #d9d9d9;
        color: black;
    }

    #noresources {
        font-size: 1.5rem;
        text-align: center;
    }

    #rating, #type {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }

    #rating div, #type div {
        display: flex;
        gap: 0.3rem;
    }

    #rating div p {
        width: 1rem;
        text-align: center;
    }

    .search-item:hover {
        border: 0.2rem solid black;
        cursor: pointer;
        border-radius: 0.5rem;
    }




</style>
