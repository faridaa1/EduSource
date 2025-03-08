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
                    <div id="filter-area-parent" v-if="filtering">
                        <div id="filter-area" >
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
                            <div id="type">
                                <label>Colour</label>
                                <div>
                                    <p :class="colour_all ? 'new' : 'not'" @click="colour_all=!colour_all">All</p>
                                    <p :class="black ? 'used' : 'not'" @click="black=!black">Black</p>
                                    <p :class="red ? 'used' : 'not'" @click="red=!red">Red</p>
                                    <p :class="yellow ? 'used' : 'not'" @click="yellow=!yellow">Yellow</p>
                                    <p :class="pink ? 'used' : 'not'" @click="pink=!pink">Pink</p>
                                    <p :class="purple ? 'used' : 'not'" @click="purple=!purple">Purple</p>
                                    <p :class="green ? 'used' : 'not'" @click="green=!green">Green</p>
                                    <p :class="blue ? 'used' : 'not'" @click="blue=!blue">Blue</p>
                                    <p :class="white ? 'used' : 'not'" @click="white=!white">White</p>
                                    <p :class="orange ? 'used' : 'not'" @click="orange=!orange">Orange</p>
                                    <p :class="brown ? 'used' : 'not'" @click="brown=!brown">Brown</p>
                                    <p :class="grey ? 'used' : 'not'" @click="grey=!grey">Grey</p>
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
                                    <button :class="all_height ? 'all' : 'not'" @click="all_height=!all_height">All</button>
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
                                    <button :class="all_width ? 'all' : 'not'" @click="all_width=!all_width">All</button>
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
                                    <button :class="all_weight ? 'all' : 'not'" @click="all_weight=!all_weight">All</button>
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
                                    <button :class="all_pages ? 'all' : 'not'" @click="all_pages=!all_pages">All</button>
                                    <input type="number" min="1" step="1" v-model="min_pages">
                                    <p>to</p>
                                    <input type="number" :min="min_price" step="1" v-model="max_pages">
                                </div>
                            </div>
                            <div id="type" v-if="(textbook || notes) && (some_unique())">
                                <label>Source</label>
                                <div>
                                    <p :class="source_all ? 'new' : 'not'" @click="source_all=!source_all">All</p>
                                    <p :class="source_self ? 'used' : 'not'" @click="source_self=!source_self">Self Made</p>
                                    <p :class="source_ai ? 'used' : 'not'" @click="source_ai=!source_ai">AI</p>
                                    <p :class="source_internet ? 'used' : 'not'" @click="source_internet=!source_internet">Internet</p>
                                </div>
                            </div>
                            <div id="type" v-if="(textbook || notes)">
                                <label>Media</label>
                                <div>
                                    <p :class="media_all ? 'new' : 'not'" @click="media_all=!media_all">All</p>
                                    <p :class="paper ? 'used' : 'not'" @click="paper=!paper">Paper</p>
                                    <p :class="online ? 'used' : 'not'" @click="online=!online">Online</p>
                                </div>
                            </div>
                             <!-- 
                'subject': self.subjects
                'author': self.author,
                -->
                            <div class="filter-row">
                                <label>Estimated Delivery</label>
                                <div class="number-filter">
                                    <button :class="all_delivery ? 'all' : 'not'" @click="all_delivery=!all_delivery">All</button>
                                    <input type="number" min="1" max="9999" step="1" v-model="min_delivery">
                                    <select v-model="min_delivery_option">
                                        <option value="minute">{{ min_delivery === 1 ? 'minute' : 'minutes'}}</option>
                                        <option value="hour">{{ min_delivery === 1 ? 'hour' : 'hours'}}</option>
                                        <option value="day">{{ min_delivery === 1 ? 'day' : 'days'}}</option>
                                        <option value="week">{{ min_delivery === 1 ? 'week' : 'weeks'}}</option>
                                        <option value="month">{{ min_delivery === 1 ? 'month' : 'months'}}</option>
                                    </select>
                                    <p>to</p>
                                    <input type="number" min="1" max="9999" step="1" v-model="max_delivery">
                                    <select v-model="max_delivery_option">
                                        <option v-if="min_delivery_option === 'minute'" value="minute">{{ max_delivery === 1 ? 'minute' : 'minutes'}}</option>
                                        <option v-if="(min_delivery_option === 'minute') || (min_delivery_option === 'hour')" value="hour">{{ max_delivery === 1 ? 'hour' : 'hours'}}</option>
                                        <option v-if="(min_delivery_option === 'minute') || (min_delivery_option === 'hour') || (min_delivery_option === 'day')" value="day">{{ max_delivery === 1 ? 'day' : 'days'}}</option>
                                        <option v-if="(min_delivery_option === 'minute') || (min_delivery_option === 'day') || (min_delivery_option === 'hour') || (min_delivery_option === 'week')" value="week">{{ max_delivery === 1 ? 'week' : 'weeks'}}</option>
                                        <option v-if="(min_delivery_option === 'minute') || (min_delivery_option === 'day') || (min_delivery_option === 'hour') || (min_delivery_option === 'week') || (min_delivery_option === 'month')" value="month">{{ max_delivery === 1 ? 'month' : 'months'}}</option>
                                    </select>
                                </div>
                            </div>
                            <div id="type">
                                <label>Delivery Options</label>
                                <div>
                                    <p :class="options_all ? 'new' : 'not'" @click="options_all=!options_all">All</p>
                                    <p :class="delivery ? 'used' : 'not'" @click="delivery=!delivery">Delivery</p>
                                    <p :class="collection ? 'used' : 'not'" @click="collection=!collection">Collection</p>
                                </div>
                            </div>
                            <div id="type">
                                <label>Return Options</label>
                                <div>
                                    <p :class="returns_all ? 'new' : 'not'" @click="returns_all=!returns_all">All</p>
                                    <p :class="returns ? 'used' : 'not'" @click="returns=!returns">Returns</p>
                                    <p :class="no_returns ? 'used' : 'not'" @click="no_returns=!no_returns">No Returns</p>
                                </div>
                            </div>
                        </div>
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
            colour_all: boolean, black: boolean, red: boolean, yellow: boolean, pink: boolean, purple: boolean, green: boolean, blue: boolean, white: boolean, orange: boolean, brown: boolean, grey: boolean,
            media_all: boolean, paper: boolean, online: boolean,
            source_all: boolean, source_self: boolean, source_ai: boolean, source_internet: boolean,
            all_delivery: boolean, max_delivery: number, min_delivery: number, min_delivery_option: 'day' | 'minute' | 'hour' | 'week' | 'month', max_delivery_option: 'day' | 'minute' | 'hour' | 'week' | 'month',
            options_all: boolean, delivery: boolean, collection: boolean,
            returns_all: boolean, returns: boolean, no_returns: boolean,
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
            colour_all: true, black: true, red: true, yellow: true, pink: true, purple: true, green: true, blue: true, white: true, orange: true, brown: true, grey: true,
            media_all: true, paper: true, online: true,
            options_all: true, delivery: true, collection: true,
            returns_all: true, returns: true, no_returns: true,
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
            all_delivery: true, max_delivery: 1, min_delivery: 1, min_delivery_option: 'day', max_delivery_option: 'day',
            source_all: true, source_self: true, source_ai: true, source_internet: true,
            max_width: 100,
            three: true,
            four: true,
            five: true,
            rating_all: true,
            type_all: true, textbook: true, stationery: true, notes: true,
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
            check_colours(): void {
                this.colour_all = this.black && this.red && this.yellow && this.pink && this.purple && this.green && this.blue && this.white && this.orange && this.brown && this.grey
            },
            check_media(): void {
                this.media_all = this.online && this.paper
            },
            check_options(): void {
                this.options_all = this.delivery && this.collection
            },
            check_returns(): void {
                this.returns_all = this.returns && this.no_returns
            },
            check_source(): void {
                this.source_all = this.source_ai && this.source_internet && this.source_self
            },
            some_unique(): boolean {
                for (let resource of this.resources) {
                    if (resource.unique) return true
                }
                return false
            },
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
            },
            maximum_height(): void {
                let max = 0
                for (let resource of this.resources) {
                    if (resource.height > max) {
                        max = resource.height
                    }
                }
                this.max_height = max
            },
            minimum_height(): void {
                let min = 0
                for (let resource of this.resources) {
                    if (resource.height < min) {
                        min = resource.height
                    }
                }
                this.min_height = min
            },
            maximum_width(): void {
                let max = 0
                for (let resource of this.resources) {
                    if (resource.width > max) {
                        max = resource.width
                    }
                }
                this.max_width = max
            },
            minimum_width(): void {
                let min = 0
                for (let resource of this.resources) {
                    if (resource.width < min) {
                        min = resource.width
                    }
                }
                this.min_width = min
            },
            maximum_weight(): void {
                let max = 0
                for (let resource of this.resources) {
                    if (resource.weight > max) {
                        max = resource.weight
                    }
                }
                this.max_weight = max
            },
            minimum_weight(): void {
                let min = 0
                for (let resource of this.resources) {
                    if (resource.weight < min) {
                        min = resource.weight
                    }
                }
                this.min_weight = min
            },
            maximum_pages(): void {
                let max = 0
                for (let resource of this.resources) {
                    if ((resource.type !== 'Stationery') && (resource.page_end > max)) {
                        max = resource.page_end
                    }
                }
                this.max_pages = max
            },
            minimum_pages(): void {
                let min = 1
                for (let resource of this.resources) {
                    if ((resource.type !== 'Stationery') && (resource.page_start < min)) {
                        min = resource.page_start
                    }
                }
                this.min_pages = min
            },
            valid_date(resource: Resource): boolean {
                if (this.all_delivery) {
                        // return true if all deliveries are allowed or the units are the same and the value is within the upper and lower bounds
                        return true
                }
                if (resource.estimated_delivery_units === this.min_delivery_option) {
                    if (this.min_delivery_option === this.max_delivery_option) {
                        return ((resource.estimated_delivery_time >= this.min_delivery) && (resource.estimated_delivery_time <= this.max_delivery)) 
                    }
                    return (resource.estimated_delivery_time >= this.min_delivery)
                }
                if (!((this.min_delivery_option === 'minute')
                    || ((this.min_delivery_option === 'hour' && resource.estimated_delivery_units !== 'minute'))
                    || ((this.min_delivery_option === 'day') && (resource.estimated_delivery_units !== 'hour') && (resource.estimated_delivery_units !== 'minute'))
                    || ((this.min_delivery_option === 'week') && ((resource.estimated_delivery_units === 'week') || (resource.estimated_delivery_units === 'month')))
                    || ((this.min_delivery_option === 'month') && (resource.estimated_delivery_units === 'month')))) {
                    // return false if units are below the minimum
                        return false
                } else if (!((this.max_delivery_option === 'minute' && resource.estimated_delivery_units === 'minute')
                    || ((this.max_delivery_option === 'hour') && (resource.estimated_delivery_units !== 'day') && (resource.estimated_delivery_units !== 'week') && (resource.estimated_delivery_units !== 'month'))
                    || ((this.max_delivery_option === 'day') && (resource.estimated_delivery_units !== 'week') && (resource.estimated_delivery_units !== 'month'))
                    || ((this.max_delivery_option === 'week') && (resource.estimated_delivery_units !== 'month'))
                    || (this.max_delivery_option === 'month'))) {
                        // return false if units are below the minimum
                        return false
                }
                
                // dealing with cases where min and max units are not the same, already assumed to meet the minimum based on tests above
                if ((this.max_delivery_option === 'hour') && (resource.estimated_delivery_units === 'hour')
                    || (this.max_delivery_option === 'day') && (resource.estimated_delivery_units === 'day')
                    || (this.max_delivery_option === 'week') && (resource.estimated_delivery_units === 'week')
                    || (this.max_delivery_option === 'month') && (resource.estimated_delivery_units === 'month')
                ) {
                    return resource.estimated_delivery_time <= this.max_delivery
                }
                // resource is within max delivery option so if they are not the same then the max would cover it
                return true
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
                        && ((this.zero && resource.rating >= 0)
                        || (this.one && resource.rating >= 1)
                        || (this.two && resource.rating >= 2)
                        || (this.three && resource.rating >= 3)
                        || (this.four && resource.rating >= 4)
                        || (this.five && resource.rating >= 5))
                        && ((resource.type === 'Stationery') 
                        || (
                            (resource.page_end <= this.max_pages) 
                            && (resource.page_start >= this.min_pages)
                        ))
                        && this.valid_date(resource)
                        && (this.source_all || !resource.unique || (
                            // assume resource is unqiue and check attributes
                            (this.source_ai && resource.source === 'AI')  
                            || (this.source_internet && resource.source === 'Internet')  
                            || (this.source_self && resource.source === 'None')  
                        ))
                        && (this.options_all 
                            || (this.delivery && resource.allow_delivery)
                            || (this.collection && resource.allow_collection)
                        )
                        && (this.returns_all 
                            || (this.returns && resource.allow_return)
                            || (this.no_returns && !resource.allow_return)
                        )
                        && (this.media_all 
                            || (this.paper && resource.media === 'Paper')
                            || (this.online && resource.media === 'Online')
                        )
                        && (this.colour_all 
                            || (this.black && resource.colour === 'Black')
                            || (this.red && resource.colour === 'Red')
                            || (this.yellow && resource.colour === 'Yellow')
                            || (this.pink && resource.colour === 'Pink')
                            || (this.purple && resource.colour === 'Purple')
                            || (this.green && resource.colour === 'Green')
                            || (this.blue && resource.colour === 'Blue')
                            || (this.white && resource.colour === 'White')
                            || (this.orange && resource.colour === 'Orange')
                            || (this.brown && resource.colour === 'Brown')
                            || (this.grey && resource.colour === 'Grey')
                        )
                    ) {
                        return true
                    }  
                    return false
                })
            }
        },
        watch: {
            red(): void {
                this.check_colours()
            },
            yellow(): void {
                this.check_colours()
            },
            pink(): void {
                this.check_colours()
            },
            purple(): void {
                this.check_colours()
            },
            green(): void {
                this.check_colours()
            },
            blue(): void {
                this.check_colours()
            },
            white(): void {
                this.check_colours()
            },
            brown(): void {
                this.check_colours()
            },
            orange(): void {
                this.check_colours()
            },
            grey(): void {
                this.check_colours()
            },
            black(): void {
                this.check_colours()
            },
            colour_all(): void {
                if (this.colour_all) {
                    this.black = true
                    this.red = true
                    this.yellow = true
                    this.pink = true
                    this.purple = true
                    this.green = true
                    this.blue = true
                    this.white = true
                    this.orange = true
                    this.brown = true
                    this.grey = true
                }
            },
            paper(): void {
                this.check_media()
            },
            online(): void {
                this.check_media()
            },
            media_all(): void {
                if (this.media_all) {
                    this.paper = true
                    this.delivery = true
                }
            },
            delivery(): void {
                this.check_options()
            },
            collection(): void {
                this.check_options()
            },
            options_all(): void {
                if (this.options_all) {
                    this.collection = true
                    this.delivery = true
                }
            },
            returns_all(): void {
                if (this.returns_all) {
                    this.returns = true
                    this.no_returns = true
                }
            },
            returns(): void {
                this.check_returns()
            },
            no_returns(): void {
                this.check_returns()
            },
            source_all(): void {
                if (this.source_all) {
                    this.source_ai = true
                    this.source_internet = true
                    this.source_self = true
                }
            },
            source_self(): void {
                this.check_source()
            },
            source_ai(): void {
                this.check_source()
            },
            source_internet(): void {
                this.check_source()
            },
            all_pages(): void {
                this.maximum_pages()
                this.minimum_pages()
                this.all_pages = true
            },
            all_price(): void {
                this.maximum_price()
                this.minimum_price()
                this.all_price = true
            },
            all_height(): void {
                this.maximum_height()
                this.minimum_height()
                this.all_height = true
            },
            all_width(): void {
                this.maximum_width()
                this.minimum_width()
                this.all_width = true
            },
            all_weight(): void {
                this.maximum_weight()
                this.minimum_weight()
                this.all_weight = true
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
                this.maximum_height()
                this.minimum_height()
                this.maximum_width()
                this.minimum_width()
                this.maximum_weight()
                this.minimum_weight()
                this.maximum_pages()
                this.minimum_pages()
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
                this.all_height = false
            },
            max_height(): void {
                if (this.max_height.toString() === '' || this.max_height < 0) this.max_height = 0
                if (this.min_height > this.max_height) {
                    this.min_height = this.max_height
                }
                this.all_height = false
            },
            min_width(): void {
                if (this.min_width.toString() === '' || this.min_width < 0) this.min_width = 0
                if (this.min_width > this.max_width) {
                    this.max_width = this.min_width
                } 
                this.all_width = false
            },
            max_width(): void {
                if (this.max_width.toString() === '' || this.max_width < 0) this.max_width = 0
                if (this.min_width > this.max_width) {
                    this.min_width = this.max_width
                }
                this.all_width = false
            },
            min_pages(): void {
                if (this.min_pages.toString() === '' || this.min_pages < 1) this.min_pages = 1
                if (this.min_pages > this.max_pages) {
                    this.max_pages = this.min_pages
                } 
                this.all_pages = false
            },
            max_pages(): void {
                if (this.max_pages.toString() === '' || this.max_pages < 1) this.max_pages = 1
                if (this.min_pages > this.max_pages) {
                    this.min_pages = this.max_pages
                }
                this.all_pages = false
            },
            min_delivery_option(): void {
                if (this.min_delivery_option === 'month') {
                    this.max_delivery_option = 'month'
                } else if (this.min_delivery_option === 'week') {
                    if ((this.max_delivery_option === 'day') || (this.max_delivery_option === 'hour') || (this.max_delivery_option === 'minute')) {
                        this.max_delivery_option = 'week'
                    }
                } else if (this.min_delivery_option === 'day') {
                    if ((this.max_delivery_option === 'hour') || (this.max_delivery_option === 'minute')) {
                        this.max_delivery_option = 'day'
                    }
                } else if (this.min_delivery_option === 'hour') {
                    if ((this.max_delivery_option === 'minute')) {
                        this.max_delivery_option = 'hour'
                    }
                } 
                this.all_delivery = false
            },
            max_delivery_option(): void {
                if ((this.min_delivery > this.max_delivery) && (
                    (this.min_delivery_option === 'day' && this.max_delivery_option === 'day')
                    || (this.min_delivery_option === 'minute' && this.max_delivery_option === 'minute')
                    || (this.min_delivery_option === 'hour' && this.max_delivery_option === 'hour')
                    || (this.min_delivery_option === 'week' && this.max_delivery_option === 'week')
                    || (this.min_delivery_option === 'month' && this.max_delivery_option === 'month')
                )) {
                    this.min_delivery = this.max_delivery
                }
                this.all_delivery = false
            },
            min_delivery(): void {
                if (this.min_delivery.toString() === '' || this.min_delivery < 1) this.min_delivery = 1
                if (this.min_delivery > 9999) this.min_delivery = 9999
                if ((this.min_delivery > this.max_delivery) && (
                    (this.min_delivery_option === 'day' && this.max_delivery_option === 'day')
                    || (this.min_delivery_option === 'minute' && this.max_delivery_option === 'minute')
                    || (this.min_delivery_option === 'hour' && this.max_delivery_option === 'hour')
                    || (this.min_delivery_option === 'week' && this.max_delivery_option === 'week')
                    || (this.min_delivery_option === 'month' && this.max_delivery_option === 'month')
                )) {
                    this.max_delivery = this.min_delivery
                } 
                this.all_delivery = false
            },
            max_delivery(): void {
                if (this.max_delivery.toString() === '' || this.max_delivery < 1) this.max_delivery = 1
                if (this.max_delivery > 9999) this.max_delivery = 9999
                if ((this.min_delivery > this.max_delivery) && (
                    (this.min_delivery_option === 'day' && this.max_delivery_option === 'day')
                    || (this.min_delivery_option === 'minute' && this.max_delivery_option === 'minute')
                    || (this.min_delivery_option === 'hour' && this.max_delivery_option === 'hour')
                    || (this.min_delivery_option === 'week' && this.max_delivery_option === 'week')
                    || (this.min_delivery_option === 'month' && this.max_delivery_option === 'month')
                )) {
                    this.min_delivery = this.max_delivery
                }
                this.all_delivery = false
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
        overflow-y: auto;
        height: 70vh;
        padding-right: 0.5rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #filter-area-parent {
        position: absolute;
        border-radius: 0.8rem;
        border: 0.1rem solid black;
        right: 3rem;
        background-color: white;
        padding: 0.7rem;
        height: 73vh;
    }


    #dark #filter-area-parent {
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
