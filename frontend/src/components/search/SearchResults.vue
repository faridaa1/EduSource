<template>
    <div id="search-container">
        <div id="search-heading">
            <div id="heading1">
                <p>Search Results</p>
            </div>
            <div id="heading2">
                <div id="first_row">
                    <div id="sort_by" v-if="filtered_resources.length > 0">
                        <label id="label">Sort</label>
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
                        <label id="label">Filter</label>
                        <i class="bi bi-sliders" @click="filtering=!filtering"></i>
                        <div id="backdrop" v-if="filtering">
                            <div id="filter-area-parent">
                                <div id="filter-area">
                                    <i class="bi bi-x" id="x" @click="filtering=false"></i>
                                    <div class="item">
                                        <label>Condition</label>
                                        <div>
                                            <p :class="condition_new ? 'new' : 'not'" @click="condition_new=!condition_new">New</p>
                                            <p :class="condition_used ? 'used' : 'not'" @click="condition_used=!condition_used">Used</p>
                                        </div>
                                    </div>
                                    <div class="item">
                                        <label>Rating</label>
                                        <div>
                                            <p :class="rating_all ? 'new' : 'not'" @click="() => { rating_all=!rating_all, zero=true; one=true; two=true; three=true; four=true; five=true } ">All</p>
                                            <p :class="zero ? 'new' : 'not'" @click="() => {zero=!zero; check_all()}">0</p>
                                            <p :class="one ? 'new' : 'not'" @click="() => {one=!one; check_all()}">1</p>
                                            <p :class="two ? 'used' : 'not'" @click="() => {two=!two; check_all()}">2</p>
                                            <p :class="three ? 'used' : 'not'" @click="() => {three=!three; check_all()}">3</p>
                                            <p :class="four ? 'used' : 'not'" @click="() => {four=!four; check_all()}">4</p>
                                            <p :class="five ? 'used' : 'not'" @click="() => {five=!five; check_all()}">5</p>
                                        </div>
                                    </div>
                                    <div class="item">
                                        <label>Type</label>
                                        <div>
                                            <p :class="type_all ? 'new' : 'not'" @click="() => { type_all=!type_all, textbook=true; notes=true; stationery=true } ">All</p>
                                            <p :class="textbook ? 'new' : 'not'" @click="() => {textbook=!textbook; check_type_all()}">Textbook</p>
                                            <p :class="notes ? 'used' : 'not'" @click="() => {notes=!notes; check_type_all()}">Notes</p>
                                            <p :class="stationery ? 'used' : 'not'" @click="() => {stationery=!stationery; check_type_all()}">Stationery</p>
                                        </div>
                                    </div>
                                    <div class="item new-line-item">
                                        <label>Subject</label>
                                        <div>
                                            <p :class="subject_all ? 'new' : 'not'" @click="subject_all=!subject_all">All</p>
                                            <p :class="subject_one ? 'used' : 'not'" @click="subject_one=!subject_one">{{ subjects[0] }}</p>
                                            <p v-if="subjects[1]" :class="subject_two ? 'used' : 'not'" @click="subject_two=!subject_two">{{ subjects[1] }}</p>
                                            <p v-if="subjects[2]" :class="subject_three ? 'used' : 'not'" @click="subject_three=!subject_three">{{ subjects[2] }}</p>
                                            <p v-if="subjects[3]" :class="subject_four ? 'used' : 'not'" @click="subject_four=!subject_four">{{ subjects[3] }}</p>
                                            <p v-if="subjects[4]" :class="subject_five ? 'used' : 'not'" @click="subject_five=!subject_five">{{ subjects[4] }}</p>
                                        </div>
                                    </div>
                                    <div class="item new-line-item">
                                        <label>Author</label>
                                        <div>
                                            <p :class="author_all ? 'new' : 'not'" @click="author_all=!author_all">All</p>
                                            <p :class="author_one ? 'used' : 'not'" @click="author_one=!author_one">{{ authors[0] }}</p>
                                            <p v-if="authors[1]" :class="author_two ? 'used' : 'not'" @click="author_two=!author_two">{{ authors[1] }}</p>
                                            <p v-if="authors[2]" :class="author_three ? 'used' : 'not'" @click="author_three=!author_three">{{ authors[2] }}</p>
                                            <p v-if="authors[3]" :class="author_four ? 'used' : 'not'" @click="author_four=!author_four">{{ authors[3] }}</p>
                                            <p v-if="authors[4]" :class="author_five ? 'used' : 'not'" @click="author_five=!author_five">{{ authors[4] }}</p>
                                        </div>
                                    </div>
                                    <div class="item new-line-item">
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
                                    <div id="price">
                                        <label>Price ({{ currency }})</label>
                                        <div class="number-filter">
                                            <button :class="all_price ? 'all' : 'not'" @click="all_price=!all_price">All</button>
                                            <input type="number" min="0" step="0.01" v-model="min_price">
                                            <p>to</p>
                                            <input type="number" :min="min_price" step="0.01" v-model="max_price">
                                        </div>
                                    </div>
                                    <div class="new-line-item dimension">
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
                                    <div class="new-line-item dimension">
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
                                    <div class="new-line-item dimension">
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
                                    <div v-if="notes || textbook" class="new-line-item item">
                                        <label>Pages</label>
                                        <div class="number-filter">
                                            <button :class="all_pages ? 'all' : 'not'" @click="all_pages=!all_pages">All</button>
                                            <input type="number" min="1" step="1" v-model="min_pages">
                                            <p>to</p>
                                            <input type="number" :min="min_price" step="1" v-model="max_pages">
                                        </div>
                                    </div>
                                    <div class="item new-line-item" v-if="(textbook || notes) && (some_unique())">
                                        <label>Source</label>
                                        <div>
                                            <p :class="source_all ? 'new' : 'not'" @click="source_all=!source_all">All</p>
                                            <p :class="source_self ? 'used' : 'not'" @click="source_self=!source_self">Self Made</p>
                                            <p :class="source_ai ? 'used' : 'not'" @click="source_ai=!source_ai">AI</p>
                                            <p :class="source_internet ? 'used' : 'not'" @click="source_internet=!source_internet">Internet</p>
                                        </div>
                                    </div>
                                    <div class="item new-line-item" v-if="(textbook || notes)">
                                        <label>Media</label>
                                        <div>
                                            <p :class="media_all ? 'new' : 'not'" @click="media_all=!media_all">All</p>
                                            <p :class="paper ? 'used' : 'not'" @click="paper=!paper">Paper</p>
                                            <p :class="online ? 'used' : 'not'" @click="online=!online">Online</p>
                                        </div>
                                    </div>
                                    <div id="estimated_delivery" class="new-line-item item">
                                        <label>Estimated Delivery</label>
                                        <div class="number-filter">
                                            <div>
                                                <button :class="all_delivery ? 'all' : 'not'" @click="all_delivery=!all_delivery">All</button>
                                            </div>
                                            <div>
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
                                    </div>
                                    <div class="item new-line-item">
                                        <label>Delivery Options</label>
                                        <div>
                                            <p :class="options_all ? 'new' : 'not'" @click="options_all=!options_all">All</p>
                                            <p :class="delivery ? 'used' : 'not'" @click="delivery=!delivery">Delivery</p>
                                            <p :class="collection ? 'used' : 'not'" @click="collection=!collection">Collection</p>
                                        </div>
                                    </div>
                                    <div class="item new-line-item">
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
                <div id="compare_resources" v-if="filtered_resources.length > 0">
                    <button @click="compare_resources" id="compres">Compare Resources</button>
                </div>
            </div>
        </div>
        <div id="search-content">
            <div id="loading" v-if="filtered_resources.length === 0 && searching"><Loading /></div>
            <div id="noresources" v-if="filtered_resources.length === 0 && !searching">No resources found</div>
            <div class="search-item" v-for="resource in filtered_resources">
                <div id="row1">
                    <div id="col1" @click="showResourcePage(resource.id)">
                        <div id="search-picture">
                            <img :src="`${url}${resource.image1}`">
                        </div>
                        <div id="search-data">
                            <p id="resource-name">{{ resource.name }}</p>
                            <p>{{ currency }}{{ parseFloat(resource.price.toString().replace('€','').replace('£','').replace('$','')).toFixed(2) }}</p>
                            <div id="stars">
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
                                <p>{{ resource.rating }}</p>
                            </div>
                            <p id="view-details" @click="showResourcePage(resource.id)">View Details</p>
                        </div>
                    </div>
                    <div id="col2">
                        <div v-if="Object.keys(user).length > 0" id="cart-filter">
                            <div id="toggle">
                                <div id="resnum">{{ Object.keys(cart_resource(resource)).length > 0 ? cart_resource(resource).number : 0 }}</div>
                                <div id=controls>
                                    <div id="plus" :class="(Object.keys(cart_resource(resource)).length > 0) ? '' : 'round-hover'" v-if="(Object.keys(cart_resource(resource)).length === 0) || (cart_resource(resource).number < resource.stock)" @click="add_to_cart(resource)">+</div>
                                    <hr v-if="((Object.keys(cart_resource(resource)).length > 0) && (cart_resource(resource).number > 0)) && (cart_resource(resource).number < resource.stock)">
                                    <div v-if="(Object.keys(cart_resource(resource)).length > 0) && (cart_resource(resource).number > 0)" id="minus" :class="(cart_resource(resource).number < resource.stock) ? '' : 'round-border'" @click="remove_from_cart(resource)">-</div>
                                </div>
                            </div>
                            <div>{{ currency }}{{ (Object.keys(cart_resource(resource)).length === 0) ? parseInt((0).toString()).toFixed(2) : (cart_resource(resource).number*parseFloat(get_resource(cart_resource(resource).resource).price.toString().replace('$','').replace('£','').replace('€',''))).toFixed(2) }}</div>
                        </div>
                        <div v-if="Object.keys(user).length > 0">
                            <button v-if="!in_wishlist(resource)" @click="add_to_wishlist(resource)">Add to Wishlist</button>
                            <button v-if="in_wishlist(resource)" @click="remove_from_wishlist(resource)">Remove from Wishlist</button>
                        </div>      
                    </div>
                </div>
                <hr id="search-separator" v-if="resource!==filtered_resources[filtered_resources.length-1]">
            </div>
        </div>
        <div id="pagination" v-if="filtered_resources.length > 0">
            <div>
                <p>Page</p>
            </div>
            <div id="of">
                <select v-model="current_page">
                    <option :value="page" v-for="page in total_pages">{{ page }}</option>
                </select>
                <p>of {{ total_pages }}</p>
            </div>
            <div id="pagination-buttons">
                <button :disabled="current_page===1" @click="update_page(-1)"><i class="bi bi-arrow-left"></i></button>
                <button :disabled="current_page===total_pages" @click="update_page(1)"><i class="bi bi-arrow-right"></i></button>
            </div>
        </div>
        <div v-if="error!==''">
            <Error :message="error" @close-error="error=''" />
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { Cart, CartResource, Resource, User, Wishlist } from '@/types';
    import { useUsersStore } from '@/stores/users';
    import Error from '../user experience/error/Error.vue';
    import { useURLStore } from '@/stores/url';
    import Loading from '../user experience/loading/Loading.vue';
    export default defineComponent({
        components: { Error, Loading },
        data(): {
            searching: boolean,
            current_page: number,
            error: string,
            subject_all: boolean, subject_one: boolean, subject_two: boolean, subject_three: boolean, subject_four: boolean, subject_five: boolean,
            author_all: boolean, author_one: boolean, author_two: boolean, author_three: boolean, author_four: boolean, author_five: boolean,
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
            total_pages: number,
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
            subject_all: true, subject_one: true, subject_two: true, subject_three: true, subject_four: true, subject_five: true,
            author_all: true, author_one: true, author_two: true, author_three: true, author_four: true, author_five: true,
            colour_all: true, black: true, red: true, yellow: true, pink: true, purple: true, green: true, blue: true, white: true, orange: true, brown: true, grey: true,
            media_all: true, paper: true, online: true,
            options_all: true, delivery: true, collection: true,
            returns_all: true, returns: true, no_returns: true,
            search_value: '',
            searching: false,
            one: true,
            dimension_unit: 'm',
            two: true,
            min_price: 0,
            error: '',
            zero: true,
            max_price: 100,
            current_page: 1,
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
            total_pages: 1,
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
            sort_by: 'rating-high'
        }},
        async mounted(): Promise<void> {
            const search: HTMLInputElement = document.getElementById('main-header-search') as HTMLInputElement
            if (search) {
                // Store search result
                const window_location: string[] = window.location.href.split('/')
                const search_query: string = window_location[window_location.length-1]
                search.value = search_query.replaceAll('%20', ' ');
                this.search_value = search.value
            }
            if (!useUserStore().csrf) {
                // Generate CSRF token of unauthenticated user
                for (let cookie of document.cookie.split(';')) {
                    const cookie_pair = cookie.split('=')
                    if (cookie_pair[0].trim() === 'csrftoken') {
                        useUserStore().saveCsrf(cookie_pair[1])
                    }
                }
            }
            // Find resources matching search result
            this.searching = true
            const searchResponse = await fetch(`${useURLStore().url}/api/semantic-search/${Object.keys(this.user).length > 0 ? this.user.id : -1}/`, {
                method: 'PUT',
                credentials: 'include',
                headers: {
                    'Content-Type' : 'application/json',
                    'X-CSRFToken' : useUserStore().csrf
                },
                body: JSON.stringify(this.search_value)
            })
            this.searching = false
            if (searchResponse.ok) {
                const searchResults: Resource[] = await searchResponse.json()
                this.resources = searchResults.filter(resource => resource.stock > 0 && !resource.is_draft)
                this.sort_resources()
            }
            document.addEventListener('click', (event) => {
                if (this.filtering) {
                    // Closing filtering panel when click occurs outside of it
                    if (event.target && (((event.target as HTMLDivElement).id === 'backdrop')) || ((event.target as HTMLDivElement).id === 'profile-header') || ((event.target as HTMLDivElement).id === 'search')) {
                        this.filtering = false
                    }
                }
            })
        },
        methods: {
            compare_resources(): void {
                // Take users to page to compare resources
                window.location.href = `/compare/${this.search_value}`
            },
            update_page(new_page: number): void {
                // Update page
                this.current_page = this.current_page + new_page
            },
            async add_to_wishlist(resource: Resource): Promise<void> {
                if (Object.keys(this.cart_resource(resource)).length > 0) {
                    // Move from cart to wishlist
                    const moveToWishlist: Response = await fetch(`${useURLStore().url}/api/user/${this.user.id}/cart-to-wishlist/`, {
                        method: 'PUT',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                            'Content-Type' : 'application/json',
                        },
                        body: JSON.stringify(this.cart_resource(resource).id)
                    })
                    if (!moveToWishlist.ok) {
                        this.error = 'Error moving to wishlist. Please try again.'
                        return
                    }
                    const data: {wishlist: Wishlist, cart: Cart} = await moveToWishlist.json()
                    useUserStore().updateCart(data.cart)
                    useUserStore().updateWishlist(data.wishlist)
                    useUsersStore().updateUser(this.user)
                } else {
                    // Add to wishlist
                    const editWishlistResponse: Response = await fetch(`${useURLStore().url}/api/user/${this.user.id}/wishlist/`, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                            'Content-Type' : 'application/json',
                        },
                        body: JSON.stringify(resource.id)
                    })
                    if (!editWishlistResponse.ok) { this.error = 'Error editing wishlist. Please try again' }
                    else { 
                        const data: { wishlist: Wishlist } = await editWishlistResponse.json()
                        useUserStore().updateWishlist(data.wishlist)
                    }
                }
            },
            async remove_from_wishlist(resource: Resource): Promise<void> {
                // Remove resource from wishlist
                const editWishlistResponse: Response = await fetch(`${useURLStore().url}/api/user/${this.user.id}/wishlist/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(resource.id)
                })
                if (!editWishlistResponse.ok) { this.error = 'Error editing wishlist. Please try again' }
                else { 
                    const data: { wishlist: Wishlist } = await editWishlistResponse.json()
                    useUserStore().updateWishlist(data.wishlist)
                }
            },
            in_wishlist(resource: Resource): boolean {
                // Returning whether resource is in wishlist
                return this.user.wishlist.resources.find(wishlist_resource => wishlist_resource.resource === resource.id) ? true : false
            },
            async remove_from_cart(resource: Resource): Promise<void> {
                // Editing number of resource in cart
                const del: boolean = (this.cart_resource(resource).number === 1) ? true : false
                const putCartItem: Response = await fetch(`${useURLStore().url}/api/update-cart/user/${this.user.id}/cart/${this.cart_resource(resource).id}/resource/${resource.id}/`, {
                    method: del ? 'DELETE' : 'PUT',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(this.cart_resource(resource).number-1)
                })
                if (!putCartItem.ok) {
                    this.error = 'Error editing cart. Please try again'
                    return
                }
                const data: {resource: CartResource, cart: Cart, wishlist: Wishlist} = await putCartItem.json()
                useUserStore().updateCart(data.cart)
                useUsersStore().updateUser(this.user)
            },
            async add_to_cart(resource: Resource): Promise<void> {
                // Adding resource to cart
                if (this.in_wishlist(resource)) this.remove_from_wishlist(resource)
                let putCartItem: Response
                if (Object.keys(this.cart_resource(resource)).length === 0) {
                    // create cart resource
                    putCartItem = await fetch(`${useURLStore().url}/api/update-cart/user/${this.user.id}/cart/-1/resource/${resource.id}/`, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                        },
                    })
                } else {
                    putCartItem = await fetch(`${useURLStore().url}/api/update-cart/user/${this.user.id}/cart/${this.cart_resource(resource).id}/resource/${resource.id}/`, {
                        method: 'PUT',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                            'Content-Type' : 'application/json',
                        },
                        body: JSON.stringify(this.cart_resource(resource).number+1)
                    })
                }
                if (!putCartItem.ok) {
                    this.error = 'Error editing cart. Please try again'
                    return
                }
                const data: {resource: CartResource, cart: Cart, wishlist: Wishlist} = await putCartItem.json()
                useUserStore().updateCart(data.cart)
                useUsersStore().updateUser(this.user)
            },
            get_resource(resource_id: number): Resource {
                // Retrieve resource given an ID
                return this.resources.find(resource => resource.id === resource_id) as Resource
            },
            cart_resource(resource: Resource): CartResource {
                // Returning cart resource related to given resource
                let cart_resource = this.user.cart.resources.find(cart_resource => cart_resource.resource === resource.id)
                if (cart_resource === undefined) {
                    for (let resource of this.resources) {
                        const potential_cart_resource = this.resources.find(res => res.id !== resource.id && res.name === resource.name && resource.author === res.author && !resource.unique)
                        if (potential_cart_resource) {
                            return this.user.cart.resources.find(cart_resource => cart_resource.resource === potential_cart_resource.id) || {} as CartResource
                        } 
                    }
                }
                return cart_resource || {} as CartResource
            },
            check_authors(): void {
                // Determining whether 'All' is selected based on values of other filters
                this.author_all = this.author_one && this.author_two && this.author_three && this.author_four && this.author_five
            },
            check_subjects(): void {
                // Determining whether 'All' is selected based on values of other filters
                this.subject_all = this.subject_one && this.subject_two && this.subject_three && this.subject_four && this.subject_five
            },
            check_colours(): void {
                // Determining whether 'All' is selected based on values of other filters
                this.colour_all = this.black && this.red && this.yellow && this.pink && this.purple && this.green && this.blue && this.white && this.orange && this.brown && this.grey
            },
            check_media(): void {
                // Determining whether 'All' is selected based on values of other filters
                this.media_all = this.online && this.paper
            },
            check_options(): void {
                // Determining whether 'All' is selected based on values of other filters
                this.options_all = this.delivery && this.collection
            },
            check_returns(): void {
                // Determining whether 'All' is selected based on values of other filters
                this.returns_all = this.returns && this.no_returns
            },
            check_source(): void {
                // Determining whether 'All' is selected based on values of other filters
                this.source_all = this.source_ai && this.source_internet && this.source_self
            },
            some_unique(): boolean {
                // Return whether any resources are unique
                for (let resource of this.resources) {
                    if (resource.unique) return true
                }
                return false
            },
            converted_weight(resource: Resource): number {
                // Convert weight
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
                // Convert dimension (height or width)
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
                // Determining whether 'All' is selected based on values of other filters
                if (this.zero && this.one && this.two && this.three && this.four && this.five) {
                    this.rating_all = true
                } else {
                    this.rating_all = false
                }
            },
            check_type_all(): void {
                // Determining whether 'All' is selected based on values of other filters
                if (this.textbook && this.notes && this.stationery) {
                    this.type_all = true
                } else {
                    this.type_all = false
                }
            },
            message(userID: number): void {
                // Taking user to page where they can message the seller
                window.location.href = `/message/${this.user.id}/${userID}`
            },
            showResourcePage(resourceId: number): void {
                window.location.href = `/view/${resourceId}` 
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
            sort_resources(): void {
                // Sorting resources
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
                        return parseFloat(b.price.toString().replace('$','').replace('£','').replace('€','')) - parseFloat(a.price.toString().replace('$','').replace('£','').replace('€',''))
                    }
                    return parseFloat(a.price.toString().replace('$','').replace('£','').replace('€','')) - parseFloat(b.price.toString().replace('$','').replace('£','').replace('€',''))
                })
            },
            maximum_price(): void {
                // Updating values to make sure they are valid
                let max = 0
                for (let resource of this.resources) {
                    if ((parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))) > max) {
                        max = parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))
                    }
                }
                this.max_price = max
            },
            minimum_price(): void {
                // Updating values to make sure they are valid
                let min = 0
                for (let resource of this.resources) {
                    if ((parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))) < min) {
                        min = parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€',''))
                    }
                }
                this.min_price = min
            },
            maximum_height(): void {
                // Updating values to make sure they are valid
                let max = 0
                for (let resource of this.resources) {
                    if (resource.height > max) {
                        max = resource.height
                    }
                }
                this.max_height = max
                this.dimension_unit = 'm'
            },
            minimum_height(): void {
                // Updating values to make sure they are valid
                let min = 0
                for (let resource of this.resources) {
                    if (resource.height < min) {
                        min = resource.height
                    }
                }
                this.min_height = min
                this.dimension_unit = 'm'
            },
            maximum_width(): void {
                // Updating values to make sure they are valid
                let max = 0
                for (let resource of this.resources) {
                    if (resource.width > max) {
                        max = resource.width
                    }
                }
                this.max_width = max
                this.weight_dimension = 'kg'
            },
            minimum_width(): void {
                // Updating values to make sure they are valid
                let min = 0
                for (let resource of this.resources) {
                    if (resource.width < min) {
                        min = resource.width
                    }
                }
                this.min_width = min
            },
            maximum_weight(): void {
                // Updating values to make sure they are valid
                let max = 0
                for (let resource of this.resources) {
                    if (resource.weight > max) {
                        max = resource.weight
                    }
                }
                this.max_weight = max
            },
            minimum_weight(): void {
                // Updating values to make sure they are valid
                let min = 0
                for (let resource of this.resources) {
                    if (resource.weight < min) {
                        min = resource.weight
                    }
                }
                this.min_weight = min
            },
            maximum_pages(): void {
                // Updating values to make sure they are valid
                let max = 0
                for (let resource of this.resources) {
                    if ((resource.type !== 'Stationery') && (resource.page_end > max)) {
                        max = resource.page_end
                    }
                }
                this.max_pages = max
            },
            minimum_pages(): void {
                // Updating values to make sure they are valid
                let min = 1
                for (let resource of this.resources) {
                    if ((resource.type !== 'Stationery') && (resource.page_start < min)) {
                        min = resource.page_start
                    }
                }
                this.min_pages = min
            },
            valid_date(resource: Resource): boolean {
                // Updating values to make sure they are valid
                if (this.all_delivery) {
                    // Return true if all deliveries are allowed or the units are the same and the value is within the upper and lower bounds
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
                    // Return false if units are below the minimum
                        return false
                } else if (!((this.max_delivery_option === 'minute' && resource.estimated_delivery_units === 'minute')
                    || ((this.max_delivery_option === 'hour') && (resource.estimated_delivery_units !== 'day') && (resource.estimated_delivery_units !== 'week') && (resource.estimated_delivery_units !== 'month'))
                    || ((this.max_delivery_option === 'day') && (resource.estimated_delivery_units !== 'week') && (resource.estimated_delivery_units !== 'month'))
                    || ((this.max_delivery_option === 'week') && (resource.estimated_delivery_units !== 'month'))
                    || (this.max_delivery_option === 'month'))) {
                        // Return false if units are below the minimum
                        return false
                }
                
                // Dealing with cases where min and max units are not the same, already assumed to meet the minimum based on tests above
                if ((this.max_delivery_option === 'hour') && (resource.estimated_delivery_units === 'hour')
                    || (this.max_delivery_option === 'day') && (resource.estimated_delivery_units === 'day')
                    || (this.max_delivery_option === 'week') && (resource.estimated_delivery_units === 'week')
                    || (this.max_delivery_option === 'month') && (resource.estimated_delivery_units === 'month')
                ) {
                    return resource.estimated_delivery_time <= this.max_delivery
                }
                // Resource is within max delivery option so if they are not the same then the max would cover it
                return true
            }
        },
        computed: {
            url(): string {
                return useURLStore().url
            },
            subjects(): string[] {
                // Return top 5 most common subjects for filtering
                let subjects_map: {[key: string] : number} = {}
                for (let resource of this.resources) {
                    if (!subjects_map[resource.subject]) {
                        subjects_map[resource.subject] = 1
                    } else {
                        subjects_map[resource.subject] += 1
                    }
                }
                return Object.keys(subjects_map).sort((a,b) => subjects_map[b]-subjects_map[a]).slice(0,6)
            },
            authors(): string[] {
                // Return top 5 most common authors for filtering
                let authors_map: {[key: string] : number} = {}
                for (let resource of this.resources) {
                    if (!authors_map[resource.author]) {
                        authors_map[resource.author] = 1
                    } else {
                        authors_map[resource.author] += 1
                    }
                }
                return Object.keys(authors_map).sort((a,b) => authors_map[b]-authors_map[a]).slice(0,6)
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
            filtered_resources(): Resource[] {
                // Filter resources
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
                temp_resources=temp_resources.filter(resource => {
                    if (
                        (this.all_price || ((parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€','')) >= this.min_price)
                        && (parseFloat(resource.price.toString().replace('$','').replace('£','').replace('€','')) <= this.max_price)))
                        && (this.all_height || ((this.converted_dimension(resource, 'height') <= this.max_height) && (this.converted_dimension(resource, 'height') >= this.min_height)))
                        && (this.all_width || ((this.converted_dimension(resource, 'width') <= this.max_width) && (this.converted_dimension(resource, 'width') >= this.min_width)))
                        && (this.all_weight || ((this.converted_weight(resource) <= this.max_weight) && (this.converted_weight(resource) >= this.min_weight)))
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
                            // Assume resource is unqiue and check attributes
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
                        && (
                            this.subject_all || (
                                (this.subject_one && resource.subject === this.subjects[0])
                                || (this.subject_two && resource.subject === this.subjects[1])
                                || (this.subject_three && resource.subject === this.subjects[2])
                                || (this.subject_four && resource.subject === this.subjects[3])
                                || (this.subject_five && resource.subject === this.subjects[4])
                            )
                        )
                        && (
                            this.author_all || (
                                (this.author_one && resource.author === this.authors[0])
                                || (this.author_two && resource.author === this.authors[1])
                                || (this.author_three && resource.author === this.authors[2])
                                || (this.author_four && resource.author === this.authors[3])
                                || (this.author_five && resource.author === this.authors[4])
                            )
                        )
                    ) {
                        return true
                    }  
                    return false
                })
                this.total_pages = Math.ceil(temp_resources.length/10)
                return temp_resources.filter((_, index) => ((index) < (this.current_page*10)) && ((index+1) > ((this.current_page-1)*10)))
            }
        },
        watch: {
            subject_one(): void {
                // Update 'All' filter
                this.check_subjects()
            },
            subject_two(): void {
                // Update 'All' filter
                this.check_subjects()
            },
            subject_three(): void {
                // Update 'All' filter
                this.check_subjects()
            },
            subject_four(): void {
                // Update 'All' filter
                this.check_subjects()
            },
            subject_five(): void {
                // Update 'All' filter
                this.check_subjects()
            },
            subject_all(): void {
                // Update filters based on whether 'All' is true
                if (this.subject_all) {
                    this.subject_one = true
                    this.subject_two = true
                    this.subject_three = true
                    this.subject_four = true
                    this.subject_five = true
                }
            },
            author_one(): void {
                // Update 'All' filter
                this.check_authors()
            },
            author_two(): void {
                // Update 'All' filter
                this.check_authors()
            },
            author_three(): void {
                // Update 'All' filter
                this.check_authors()
            },
            author_four(): void {
                // Update 'All' filter
                this.check_authors()
            },
            author_five(): void {
                // Update 'All' filter
                this.check_authors()
            },
            author_all(): void {
                // Update filters based on whether 'All' is true
                if (this.author_all) {
                    this.author_one = true
                    this.author_two = true
                    this.author_three = true
                    this.author_four = true
                    this.author_five = true
                }
            },
            red(): void {
                // Update 'All' filter
                this.check_colours()
            },
            yellow(): void {
                // Update 'All' filter
                this.check_colours()
            },
            pink(): void {
                // Update 'All' filter
                this.check_colours()
            },
            purple(): void {
                // Update 'All' filter
                this.check_colours()
            },
            green(): void {
                // Update 'All' filter
                this.check_colours()
            },
            blue(): void {
                // Update 'All' filter
                this.check_colours()
            },
            white(): void {
                // Update 'All' filter
                this.check_colours()
            },
            brown(): void {
                // Update 'All' filter
                this.check_colours()
            },
            orange(): void {
                // Update 'All' filter
                this.check_colours()
            },
            grey(): void {
                // Update 'All' filter
                this.check_colours()
            },
            black(): void {
                // Update 'All' filter
                this.check_colours()
            },
            colour_all(): void {
                // Update filters based on whether 'All' is true
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
                // Update 'All' filter
                this.check_media()
            },
            online(): void {
                // Update 'All' filter
                this.check_media()
            },
            media_all(): void {
                // Update filters based on whether 'All' is true
                if (this.media_all) {
                    this.paper = true
                    this.delivery = true
                }
            },
            delivery(): void {
                // Update 'All' filter
                this.check_options()
            },
            collection(): void {
                // Update 'All' filter
                this.check_options()
            },
            options_all(): void {
                // Update filters based on whether 'All' is true
                if (this.options_all) {
                    this.collection = true
                    this.delivery = true
                }
            },
            returns_all(): void {
                // Update filters based on whether 'All' is true
                if (this.returns_all) {
                    this.returns = true
                    this.no_returns = true
                }
            },
            returns(): void {
                // Update 'All' filter
                this.check_returns()
            },
            no_returns(): void {
                // Update 'All' filter
                this.check_returns()
            },
            source_all(): void {
                // Update filters based on whether 'All' is true
                if (this.source_all) {
                    this.source_ai = true
                    this.source_internet = true
                    this.source_self = true
                }
            },
            source_self(): void {
                // Update 'All' filter
                this.check_source()
            },
            source_ai(): void {
                // Update 'All' filter
                this.check_source()
            },
            source_internet(): void {
                // Update 'All' filter
                this.check_source()
            },
            all_pages(): void {
                if (this.all_pages) {
                    this.maximum_pages()
                    this.minimum_pages()
                }
            },
            all_price(): void {
                if (this.all_price) {
                    this.maximum_price()
                    this.minimum_price()
                }
            },
            all_height(): void {
                if (this.all_height) {
                    this.maximum_height()
                    this.minimum_height()
                }
            },
            all_width(): void {
                if (this.all_width) {
                    this.maximum_width()
                    this.minimum_width()
                }
            },
            all_weight(): void {
                if (this.all_weight) {
                    this.maximum_weight()
                    this.minimum_weight()
                }
            },
            async user(new_user: User): Promise<void> {
                for (const resource of this.user.listings) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resources(resources: Resource[]): Promise<void> {
                // Resetting values
                if (Object.keys(resources).length < 1) return
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
                // Finding minimum price based on all resources
                if (this.min_price.toString() === '' || this.min_price < 0) this.min_price = 0
                if (this.min_price > this.max_price) {
                    this.max_price = this.min_price
                } 
                this.all_price = false
            },
            max_price(): void {
                // Finding maximum price based on all resources
                if (this.max_price.toString() === '' || this.max_price < 0) this.max_price = 0
                if (this.min_price > this.max_price) {
                    this.min_price = this.max_price
                }
                this.all_price = false
            },
            min_height(): void {
                // Finding minimum height based on all resources
                if (this.min_height.toString() === '' || this.min_height < 0) this.min_height = 0
                if (this.min_height > this.max_height) {
                    this.max_height = this.min_height
                } 
                this.all_height = false
            },
            max_height(): void {
                // Finding maximum height based on all resources
                if (this.max_height.toString() === '' || this.max_height < 0) this.max_height = 0
                if (this.min_height > this.max_height) {
                    this.min_height = this.max_height
                }
                this.all_height = false
            },
            min_width(): void {
                // Finding minimum width based on all resources
                if (this.min_width.toString() === '' || this.min_width < 0) this.min_width = 0
                if (this.min_width > this.max_width) {
                    this.max_width = this.min_width
                } 
                this.all_width = false
            },
            max_width(): void {
                // Finding maximum width based on all resources
                if (this.max_width.toString() === '' || this.max_width < 0) this.max_width = 0
                if (this.min_width > this.max_width) {
                    this.min_width = this.max_width
                }
                this.all_width = false
            },
            min_pages(): void {
                // Finding minimum pages based on all resources
                if (this.min_pages.toString() === '' || this.min_pages < 1) this.min_pages = 1
                if (this.min_pages > this.max_pages) {
                    this.max_pages = this.min_pages
                } 
                this.all_pages = false
            },
            max_pages(): void {
                // Finding maximum pages based on all resources
                if (this.max_pages.toString() === '' || this.max_pages < 1) this.max_pages = 1
                if (this.min_pages > this.max_pages) {
                    this.min_pages = this.max_pages
                }
                this.all_pages = false
            },
            min_delivery_option(): void {
                // Finding minimum delivery option unit based on all resources
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
                // Finding maximum delivery option unit based on all resources
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
                // Finding minimum delivery option value based on all resources
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
                // Finding maximum delivery option value based on all resources
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
            },
        },
    })
</script>

<style scoped>
    img {
        width: 10rem;
        height: 10rem;
        object-fit: contain;
    }

    #stars {
        display: flex;
        gap: 0.3rem;
    }

    #stars p {
        margin-left: 0.5rem;
    }

    #estimated_delivery div {
        flex-direction: row;
    }

    #estimated_delivery input, #estimated_delivery select {
        width: 3.8rem !important;
        padding: 0rem;
        padding-top: 0.4rem;
        padding-bottom: 0.4rem;
        padding-left: 0.1rem;
    }

    .number-filter input {
        text-align: center;
        width: 4rem !important;
    }

    input {
        border-radius: 0.5rem;
    }

    #search-data {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    #search-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        padding: 1.5rem;
        position: relative;
    }

    #dark #search-container {
        color: white;
    }

    #search-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    #heading1 p, #heading2 #first_row #label, #filter i {
        font-size: 1.2rem;
    }

    #heading1 {
        align-self: flex-start;
    }

    #compare_resources button {
        border: none;
        background-color: #0DCAF0;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    #dark #compare_resources button {
        background-color: white;
    }

    #compare_resources button:hover {
        cursor: pointer;
        background-color: #2d8da0 !important;
    }

    #dark #compare_resources button:hover {
        background-color: darkgray !important;
    }

    #label {
        width: 2rem;
    }

    #heading2 #first_row {
        display: flex;
        align-items: center;
        gap: 2rem;
    }

    #heading2 {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    select {
        padding: 0.4rem;
        border-radius: 0.5rem;
        border: none;
        background-color: #0DCAF0;
    }

    select, #compres {
        color: black;
    }

    #dark select {
        background-color: white;
    }

    #sort_by {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    #search-content {
        height: 80vh;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 1rem;
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
        gap: 1.5rem;
        position: relative;
    }

    #filter-area-parent {
        width: 75vw;
        margin-left: auto;
        margin-right: 2rem;
        margin-top: 1rem;
        border-radius: 0.8rem;
        background-color: white;
        border: 0.1rem solid black;
        right: 3rem;
        padding: 0.7rem;
        height: 73vh;
    }


    #dark #filter-area-parent {
        background-color: rgb(41, 41, 41);
        border: 0.1rem solid white;
    }

    .new, .used, .all {
        background-color: #0DCAF0;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    #dark .new, #dark .used, #dark .all {
        background-color: #d9d9d9;
        color: black;
    }

    .new:hover, .used:hover, .all:hover, .all:hover {
        background-color: #2d8da0;
    }

    #dark .new:hover, #dark .used:hover, #dark .all:hover {
        background-color: rgb(96, 96, 96);
    }

    .not {
        background-color: #d9d9d9;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    #dark .not {
        background-color: rgb(96, 96, 96);
        color: black;
    }

    .not:hover {
        background-color: #2d8da0;
    }

    #dark .not:hover {
        background-color: #d9d9d9;
        color: black;
    }

    #noresources {
        font-size: 1.3rem;
        text-align: center;
    }

    .item, #price, .dimension {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .item div, .number-filter {
        align-items: center;
        display: flex;
        gap: 0.8rem;
    }

    .new-line-item div {
        flex-wrap: wrap;
        width: 100%;
    }

    #rating div p {
        width: 1rem;
        text-align: center;
    }

    #col1:hover {
        cursor: pointer;
    }

    #view-details {
        color: rgb(121, 189, 218);
    }

    #view-details:hover {
        text-decoration: underline;
    }

    #dark #view-details {
        color: rgb(206, 206, 206);
    }

    #toggle {
        background-color: #D9D9D9;
        display: flex;
        width: 6rem;
        padding-left: 0.4rem;
        padding-right: 0.4rem;
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        border-radius: 0.5rem;
        align-items: center;
    }

    #toggle:hover {
        background-color: #D9D9D9;
    }

    #controls {
        display: flex;
        background-color: white;
        margin-left: auto;
        border-radius: 0.2rem;
        text-align: center;
    }

    #controls div {
        width: 1rem;
    }

    #controls div:hover {
        background-color: darkgray;
        cursor: pointer;
    }

    hr { 
        border: none;
        background-color: black;
        width: 0.01rem;
    }

    #plus:hover {
        border-top-left-radius: 0.2rem;
        border-bottom-left-radius: 0.2rem;
    }

    #minus {
        border-top-right-radius: 0.2rem;
        border-bottom-right-radius: 0.2rem;
    }

    #loading {
        overflow-y: hidden;
        overflow-x: hidden;
    }

    .round-border {
        border-top-left-radius: 0.2rem;
        border-bottom-left-radius: 0.2rem;
    }

    #minus i {
        color: red !important;
        font-size: 0.8rem;
    }

    #resnum {
        margin: auto;
    }

    .round-hover {
        border-radius: 0.2rem;
    }

    #cart-filter {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem
    }

    .search-item {
        display: flex;
        flex-direction: column;
    }

    .search-item #row1 {
        display: flex;
        align-items: center;
        gap: 2rem;
        justify-content: space-between;
        padding: 0.5rem;
    }

    #search-separator {
        height: 0.01rem;
        background-color: #d9d9d9;
        border-radius: 0.5rem;
        width: 95%;
        margin-top: 0.8rem;
    }

    #backdrop {
        position: absolute;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: 4;
        background-color: rgba(140, 140, 140, 0.5);
        margin: 0;
    }

    #col1, #col2 {
        display: flex;
        gap: 4rem;
        align-items: center;
    }

    #col2 button {
        border: none;
        padding: 0.5rem;
        background-color: #0DCAF0;
        width: 10rem;
        border-radius: 0.5rem;
    }

    #col2 {
        margin-right: 1rem;
    }

    #dark #toggle {
        color: black;
    }

    #col2 button:hover {
        background-color: #2d8da0;
        cursor: pointer;
    }

    #dark #col2 button {
        background-color: white;
    }

    #dark #col2 button:hover {
        background-color: darkgray;
    }

    #resource-name {
        width: 40vw;
        word-wrap: break-word;
    }

    #pagination {
        display: flex;
        align-items: center;
        gap: 1rem;
        justify-content: center;
    }

    #pagination p {
        font-size: 1.3rem;
    }

    #pagination select, #pagination i {
        font-size: 1rem;
    }

    #pagination #pagination-buttons {
        display: flex;
        gap: 1.5rem;
        margin-left: 1rem;
    }

    #pagination #pagination-buttons button {
        border-radius: 0.5rem;
        border: none;
        padding: 0.45rem;
        background-color: #0DCAF0;
        color: white;
    }

    #dark #pagination #pagination-buttons button {
        background-color: white;
        color: black;
    }

    #dark #pagination #pagination-buttons button:hover {
        background-color: darkgray;
    }

    #pagination #pagination-buttons button:hover {
        cursor: pointer;
        background-color: #15acca;
    }

    #pagination #pagination-buttons button:disabled, #dark #pagination #pagination-buttons button:disabled {
        background-color: lightgrey;
        color: darkgray;
    }

    #pagination #pagination-buttons button:disabled:hover {
        cursor: not-allowed;
    }

    #of {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .search-item #row1 img {
        background-color: #d9d9d9;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    #sort_by, #filter {
        display: flex;
        gap: 1.5rem;
    }

    #x {
        color: red;
        position: absolute;
        right: 0;
        top: -0.5rem;
        font-size: 2rem !important;
    }

    #x:hover {
        color: darkred;
    }

    #dark #x {
        color: rgb(250, 141, 141);
    }

    #dark #x:hover {
        color: rgb(245, 116, 116);
    }

    /* Responsive Design */
    @media (max-width: 1156px) {
        #col2 {
            flex-direction: column;
            gap: 1rem;
        }

        #cart-filter {
            flex-direction: row;
            gap: 1rem;
        }
    }

    @media (max-width: 852px) {
        .search-item #row1 {
            flex-direction: column;
            gap: 0.5rem;
            align-items: flex-start;
        }

        #col2 {
            align-items: flex-start;
            flex-direction: row;
            gap: 2rem;
            margin-right: 0;
            margin-top: 1rem;
        }

        #cart-filter {
            flex-direction: column;
            gap: 1rem;
        }
    }

    @media (max-width: 559px) {
        .search-item #row1 p, button, .search-item #row1 div, p {
            font-size: 1rem !important;
        }

        .search-item #row1 img {
            height: 6rem;
            width: 6rem;
            object-fit: contain;
        }

        #col1 {
            gap: 1rem;
        }

        #heading1 p {
            font-size: 1.2rem !important;
        }
    }

    @media (max-width: 542px) {
        #heading2 #first_row {
            flex-direction: column;
            gap: 1rem;
            align-items: start;
        }

        #sort_by, #filter {
            font-size: 1rem;
        }

        #search-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }

    @media (max-height: 1360px), (max-width: 559px) {
        #search-content {
            height: 77vh;
        }
    }

    @media (max-height: 1100px) {
        #search-content {
            height: 74vh;
        }
    }

    @media (max-height: 1240px) {
        #search-content {
            height: 73vh;
        }
    }

    @media (max-height: 1036px) {
        #search-content {
            height: 70vh;
        }
    }

    @media (max-height: 935px) {
        #search-content {
            height: 66vh;
        }
    }

    @media (max-height: 889px) {
        #search-content {
            height: 67vh;
        }
    }

    @media (max-height: 816px) {
        #search-content {
            height: 65vh;
        }
    }

    @media (max-height: 794px) {
        #search-content {
            height: 60vh;
        }
    }

    @media (max-height: 672px) {
        #search-content {
            height: 54vh;
        }
    }

</style>
