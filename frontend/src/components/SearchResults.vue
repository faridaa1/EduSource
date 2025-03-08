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
                                <p :class="zero ? 'new' : 'not'" @click="() => {zero=!zero; check_all()}">0</p>
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
                            <label>Price ({{ currency }})</label>
                            <div class="number-filter">
                                <button :class="all_price ? 'all' : 'not'" @click="all_price=!all_price">All</button>
                                <input type="number" min="0" step="0.01" v-model="min_price">
                                <p>to</p>
                                <input type="number" :min="min_price" step="0.01" v-model="max_price">
                            </div>
                        </div>
                        <div class="filter-row">
                            <label>Height</label>
                            <div class="number-filter">
                                <input type="number" min="0" step="0.01" v-model="min_height">
                                <p>to</p>
                                <input type="number" :min="min_height" step="0.01" v-model="max_height">
                                <select v-model="dimension_unit">
                                    <option value="cm">cm</option>
                                    <option value="m">m</option>
                                    <option value="in">in</option>
                                </select>
                            </div>
                        </div>
                        <div class="filter-row">
                            <label>Width</label>
                            <div class="number-filter">
                                <input type="number" min="0" step="0.01" v-model="min_width">
                                <p>to</p>
                                <input type="number" :min="min_width" step="0.01" v-model="max_width">
                                <select v-model="dimension_unit">
                                    <option value="cm">cm</option>
                                    <option value="m">m</option>
                                    <option value="in">in</option>
                                </select>
                            </div>
                        </div>
                        <div class="filter-row">
                            <label>Weight</label>
                            <div class="number-filter">
                                <input type="number" min="0" step="0.01" v-model="min_weight">
                                <p>to</p>
                                <input type="number" :min="min_width" step="0.01" v-model="max_weight">
                                <select v-model="weight_dimension">
                                    <option value="lb">lb</option>
                                    <option value="kg">kg</option>
                                    <option value="ml">ml</option>
                                    <option value="L">L</option>
                                    <option value="mg">mg</option>
                                    <option value="oz">oz</option>
                                </select>
                            </div>
                        </div>
                        <div v-if="notes || textbook" class="filter-row">
                            <label>Pages</label>
                            <div class="number-filter">
                                <input type="number" min="01" step="1" v-model="min_pages">
                                <p>to</p>
                                <input type="number" :min="min_price" step="1" v-model="max_pages">
                            </div>
                        </div>
                        <!-- 
            'estimated_delivery_time': self.estimated_delivery_time,
            'subject': self.subject,
            'author': self.author,
            'self_made': self.self_made,
            'estimated_delivery_units': self.estimated_delivery_units,
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
    import { defineComponent } from 'vue';
    import type { Resource, User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            resources: Resource[],
            search_value: string,
            sorting: boolean,
            zero: boolean,
            one: boolean, 
            min_pages: number,
            max_pages: number,
            two: boolean,
            min_weight: number,
            max_weight: number,
            three: boolean,
            four: boolean,
            five: boolean,
            min_price: number,
            min_width: number,
            max_width: number,
            max_price: number,
            min_height: number,
            all_price: boolean,
            max_height: number,
            rating_all: boolean,
            type_all: boolean,
            all_height: boolean,
            all_width: boolean,
            all_weight: boolean,
            all_pages: boolean,
            textbook: boolean,
            notes: boolean,
            dimension_unit: 'in' | 'm' | 'cm',
            stationery: boolean,
            filtering: boolean,
            weight_dimension: 'lb' | 'kg' | 'ml' | 'L' | 'mg' |'oz',
            condition_new: boolean,
            condition_used: boolean, 
            sort_by: 'listing-new' | 'listing-old' | 'rating-low' | 'rating-high' | 'price-low' | 'price-high'
        } { return {
            search_value: '',
            one: true,
            dimension_unit: 'cm',
            two: true,
            min_price: 0,
            zero: true,
            max_price: 100,
            min_height: 0,
            max_height: 100,
            min_width:0,
            max_width: 100,
            three: true,
            four: true,
            five: true,
            rating_all: true,
            type_all: true,
            textbook: true,
            stationery: true,
            notes: true,
            min_pages: 1,
            max_pages: 100,
            resources: [],
            all_height: true,
            all_price: true,
            all_width: true,
            all_weight: true,
            all_pages: true,
            condition_new: true,
            condition_used: true,
            min_weight: 0,
            max_weight: 100,
            weight_dimension: 'kg',
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
            converted_weight(resource: Resource): number {
                if (
                    (resource.weight_unit === 'L' && this.weight_dimension === 'L')
                    || (resource.weight_unit === 'lb' && this.weight_dimension === 'lb')
                    || (resource.weight_unit === 'kg' && this.weight_dimension === 'kg')
                    || (resource.weight_unit === 'ml' && this.weight_dimension === 'ml')
                    || (resource.weight_unit === 'mg' && this.weight_dimension === 'mg')
                    || (resource.weight_unit === 'mg' && this.weight_dimension === 'mg') 
                ) {
                    return resource.weight
                }
                if (this.weight_dimension === 'lb') {
                    if (resource.weight_unit === 'kg') {
                        return resource.weight*2.205
                    } else if (resource.weight_unit === 'ml') {
                        return resource.weight*0.0022
                    } else if (resource.weight_unit === 'L') {
                        return resource.weight*2.2042
                    } else if (resource.weight_unit === 'mg') {
                        return resource.weight/453600
                    } else {
                        return resource.weight/16
                    }
                } else if (this.weight_dimension === 'kg') {
                    if (resource.weight_unit === 'lb') {
                        return resource.weight/2.205
                    } else if (resource.weight_unit === 'ml') {
                        return resource.weight*0.001
                    } else if (resource.weight_unit === 'L') {
                        return resource.weight
                    } else if (resource.weight_unit === 'mg') {
                        return resource.weight/1e+6
                    } else {
                        return resource.weight/35.274
                    }
                } else if (this.weight_dimension === 'ml') {
                    if (resource.weight_unit === 'lb') {
                        return resource.weight*453.592
                    } else if ((resource.weight_unit === 'kg') || (resource.weight_unit === 'L')) {
                        return resource.weight*1000
                    } else if (resource.weight_unit === 'mg') {
                        return resource.weight/1000
                    } else {
                        return resource.weight*28.413
                    }
                } else if (this.weight_dimension === 'L') {
                    if (resource.weight_unit === 'lb') {
                        return resource.weight/2.205
                    } else if ((resource.weight_unit === 'ml') || (resource.weight_unit === 'mg')) {
                        return resource.weight/1000
                    } else if (resource.weight_unit === 'kg') {
                        return resource.weight
                    } else {
                        return resource.weight/35.195
                    }
                } else if (this.weight_dimension === 'mg') {
                    if (resource.weight_unit === 'lb') {
                        return resource.weight*453600
                    } else if (resource.weight_unit === 'ml') {
                        return resource.weight*1000
                    } else if (resource.weight_unit === 'L') {
                        return resource.weight*1000000
                    } else if (resource.weight_unit === 'kg') {
                        return resource.weight*1e+6
                    } else {
                        return resource.weight*28350
                    }
                } else {
                    if (resource.weight_unit === 'lb') {
                        return resource.weight*16
                    } else if (resource.weight_unit === 'ml') {
                        return resource.weight/28.413
                    } else if (resource.weight_unit === 'L') {
                        return resource.weight*33.814
                    } else if (resource.weight_unit === 'mg') {
                        return resource.weight/28350
                    } else {
                        return resource.weight*35.274
                    }
                }                 
            },
            converted_dimension(resource: Resource, dimension: string): number {
                // convert dimension 
                if ((resource.height_unit === 'm' && this.dimension_unit === 'm') 
                    || (resource.height_unit === 'cm' && this.dimension_unit === 'cm')
                    || (resource.height_unit === 'in' && this.dimension_unit === 'in')) {
                        return dimension === 'height' ? resource.height : resource.width
                    }
                if (this.dimension_unit === 'm') {
                    if (resource.height_unit === 'in') {
                        return (dimension === 'height' ? resource.height : resource.width)/39.37
                    } else {
                        return (dimension === 'height' ? resource.height : resource.width)/100
                    }
                } else if (this.dimension_unit === 'cm') {
                    if (resource.height_unit === 'in') {
                        return (dimension === 'height' ? resource.height : resource.width)*2.54
                    } else {
                        return (dimension === 'height' ? resource.height : resource.width)*100
                    }
                } else {
                    if (resource.height_unit === 'm') {
                        return (dimension === 'height' ? resource.height : resource.width)*39.37
                    } else {
                        return (dimension === 'height' ? resource.height : resource.width)/2.54
                    }
                }
            },
            check_all(): void {
                if (this.zero && this.one && this.two && this.three && this.four && this.five) {
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
            maximum_price(): void {
                let max = 0
                for (let resource of this.resources) {
                    if ((parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))) > max) {
                        max = parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))
                    }
                }
                this.max_price = max
            },
            minimum_price(): void {
                let min = 0
                for (let resource of this.resources) {
                    if ((parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))) < min) {
                        min = parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))
                    }
                }
                this.min_price = min
            }
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
                        (this.all_price || ((parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€','')) >= this.min_price)
                        && (parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€','')) <= this.max_price)))
                        && ((this.converted_dimension(resource, 'height') <= this.max_height) && (this.converted_dimension(resource, 'height') >= this.min_height))
                        && ((this.converted_dimension(resource, 'width') <= this.max_width) && (this.converted_dimension(resource, 'width') >= this.min_width))
                        && ((this.converted_weight(resource) <= this.max_weight) && (this.converted_weight(resource) >= this.min_weight))
                        && ((this.condition_new && resource.condition === 'New') || (this.condition_used && resource.condition === 'Used'))
                        && ((this.textbook && resource.type === 'Textbook') || (this.stationery && resource.type === 'Stationery') || (this.notes && resource.type === 'Notes'))
                        && (this.rating_all
                        || (this.zero && resource.rating >= 0)
                        || (this.one && resource.rating >= 1)
                        || (this.two && resource.rating >= 2)
                        || (this.three && resource.rating >= 3)
                        || (this.four && resource.rating >= 4)
                        || (this.five && resource.rating >= 5))
                    ) {
                        return true
                    }  
                    return false
                })
            }
        },
        watch: {
            all_price(): void {
                this.maximum_price()
                this.minimum_price()
                this.all_price = true
            },
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
                this.maximum_price()
                this.minimum_price()
                this.all_price = true
            },
            sort_by(): void {
                this.sort_resources()
            },
            min_price(): void {
                if (this.min_price.toString() === '' || this.min_price < 0) this.min_price = 0
                if (this.min_price > this.max_price) {
                    this.max_price = this.min_price
                } 
                this.all_price = false
            },
            max_price(): void {
                if (this.max_price.toString() === '' || this.max_price < 0) this.max_price = 0
                if (this.min_price > this.max_price) {
                    this.min_price = this.max_price
                }
                this.all_price = false
            },
            min_height(): void {
                if (this.min_height.toString() === '' || this.min_height < 0) this.min_height = 0
                if (this.min_height > this.max_height) {
                    this.max_height = this.min_height
                } 
            },
            max_height(): void {
                if (this.max_height.toString() === '' || this.max_height < 0) this.max_height = 0
                if (this.min_height > this.max_height) {
                    this.min_height = this.max_height
                }
            },
            min_width(): void {
                if (this.min_width.toString() === '' || this.min_width < 0) this.min_width = 0
                if (this.min_width > this.max_width) {
                    this.max_width = this.min_width
                } 
            },
            max_width(): void {
                if (this.max_width.toString() === '' || this.max_width < 0) this.max_width = 0
                if (this.min_width > this.max_width) {
                    this.min_width = this.max_width
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

    .number-filter {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .number-filter input {
        text-align: center;
        width: 5rem !important;
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

    #filter i:hover, .new:hover, .all:hover, .used:hover, .not:hover {
        cursor: pointer;
    }

    .all, .new, .not {
        border: none;
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

    .new, .used, .all {
        background-color: green;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    #dark .new, #dark .used, #dark .all {
        background-color: #d9d9d9;
        color: black;
    }

    .new:hover, .used:hover, .all:hover, .all:hover {
        background-color: rgb(97, 205, 97);
    }

    #dark .new:hover, #dark .used:hover, #dark .all:hover {
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
