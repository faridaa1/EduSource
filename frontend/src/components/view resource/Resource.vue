<template>
    <div id="resource-view" v-if="resource && Object.keys(resource).length > 0">
        <div id="header">
            <p>{{ (resource as Resource).name }}</p>
        </div>
        <div id="resource">
            <img id="resource-image" :src="`${url}/${(resource as Resource).image1}`" :alt="`${(resource as Resource).type}`">
            <div id="resource-price-and-rating">
                <div>{{ Object.keys(user).length === 0 ? unauth_currency(resource as Resource) : '' }}{{ (resource as Resource).price }}</div>
                <div id="rating" @click="scrollReviewsIntoView()">
                    <i id="one" class="bi bi-star-fill"></i>
                    <i id="two" class="bi bi-star-fill"></i>
                    <i id="three" class="bi bi-star-fill"></i>
                    <i id="four" class="bi bi-star-fill"></i>
                    <i id="five" class="bi bi-star-fill"></i>
                    <p>{{ average_rating }}</p>
                    <span class="rating-text" v-if="total_ratings === 1">({{total_ratings}} rating)</span>
                    <span class="rating-text" v-if="total_ratings !== 1">({{total_ratings}} ratings)</span>
                </div>
                <span v-if="total_ratings === 0">0 ratings</span>
                <div id="add-review" v-if="!written_review && total_ratings === 0" @click="add_review">Be the first to write a review</div>
                <div id="add-review" v-if="Object.keys(user).length > 0 && total_ratings > 0 && possible_sellers(false).length > 0" @click="add_review">Add Review</div>
                <div id="est-del">Estimated Delivery: {{ parseFloat((resource as Resource).estimated_delivery_time.toString()) }} {{ (resource as Resource).estimated_delivery_units }}{{ parseFloat((resource as Resource).estimated_delivery_time.toString()) !== 1 ? 's' : '' }}</div>
            </div>
        </div>
        <div id="resource-description">
            <div>Description</div>
            <div id="desc">{{ (resource as Resource).description }}</div>
        </div>
        <div id="resource-cart">
            <div id="cart-total-section" v-if="Object.keys(user).length > 0">
                <div id="cart">
                    <p id="cart-total">{{ cart_resource.number }}</p>
                    <div id="cart-toggle">
                        <p v-if="(Object.keys(currentResource).length === 0) || cart_resource.number < currentResource.stock" id="plus" :class="cart_resource.number === 0 || (Object.keys(currentResource).length === 0) ? 'round-plus' : ''" @click="update_cart(1)">+</p>
                        <hr v-if="cart_resource.number > 0 && ((Object.keys(currentResource).length === 0) || (cart_resource.number < currentResource.stock))">
                        <p v-if="cart_resource.number > 0" id="minus" :class="(Object.keys(currentResource).length === 0) || (cart_resource.number < currentResource.stock) ? '' : 'round-border'" @click="update_cart(-1)"><i :class="cart_resource.number === 1 ? 'bi bi-trash3-fill' : ''"></i>{{ cart_resource.number === 1 ? '' : '-' }}</p>
                    </div>
                </div>
                <div id="total" v-if="cart_resource.number > 0"> Total: {{ user.currency === 'GBP' ? '£' : user.currency === 'USD' ? '$' : '€' }}{{ (cart_resource.number * cart_price).toFixed(2) }} </div>
            </div>
            <div v-if="Object.keys(user).length > 0" @click="edit_wishlist()">{{ in_wishlist ? 'Remove from Wishlist' : 'Add to Wishlist' }}</div>
        </div>
        <div id="view-sellers">
            <p @click="show_sellers">View Sellers</p>
            <p id="buynow" @click=buy_now v-if="Object.keys(user).length > 0">Buy Now</p>
            <p id="exchange" @click=exchange() v-if="(Object.keys(user).length > 0) && has_resources()">Exchange</p>
        </div>
        <ViewSellers :resources="allResources" :seller="seller" v-if="viewing_sellers" @close-view="viewing_sellers = false" @update_seller="update_seller" />
        <div id="resource-details">
            <div>Product Details</div>
            <div id="details">
                <div class="detail">
                    <label>Height</label>
                    <div class="data">
                        <p>{{ parseFloat((resource as Resource).height.toString()) }}</p>
                        <p>{{ (resource as Resource).height_unit }}</p>
                    </div>
                </div>
                <div class="detail">
                    <label>Width</label>
                    <div class="data">
                        <p>{{ parseFloat((resource as Resource).width.toString()) }}</p>
                        <p>{{ (resource as Resource).width_unit }}</p>
                    </div>
                </div>
                <div class="detail">
                    <label>Weight</label>
                    <div class="data">
                        <p>{{ parseFloat((resource as Resource).weight.toString()) }}</p>
                        <p>{{ (resource as Resource).weight_unit }}</p>
                    </div>
                </div>
                <div class="detail">
                    <label>Colour</label>
                    <div class="data">
                        <p>{{ (resource as Resource).colour }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div id="stars">
            <div>
                <p id="reviews-p">Reviews</p>
            </div>
            <Stars />
        </div>
        <div id="my-review">
            <div id="filtering" v-if="!addingReview && !editing">
                <button id="add-review" v-if="Object.keys(user).length > 0 && !addingReview && possible_sellers(false).length > 0" @click="add_review">Click to add Review</button>
                <div id="sorting">
                    <div id="filter-right">
                        <div class="filtering">
                            <label>Sort</label>
                            <select v-model="sort_by">
                                <option value="earliest">Date: Earliest to Latest</option>
                                <option value="latest">Date: Latest to Earliest</option>
                                <option value="low">Rating: Low to High</option>
                                <option value="high">Rating: High to Low</option>
                                <option value="positive">Review: Positive to Negative</option>
                                <option value="negative">Review: Negative to Positive</option>
                            </select>
                        </div>
                        <div class="filtering" id="clickable">
                            <div id="filtering-section">
                                <div id="toggle-filter" @click="toggleFilter">
                                    <p id="clickable">Filter</p>
                                    <i id="clickable" v-if="!toggle_filter" class="bi bi-chevron-down"></i>
                                    <i id="clickable" v-if="toggle_filter" class="bi bi-chevron-up"></i>
                                </div>
                                <div id="filter-options" v-if="toggle_filter">
                                    <div class="filter-item border-top">
                                        <label>Review Type</label>
                                        <div class="row">
                                            <div :class="both_reviews ? '' : 'not'" class="datum" @click="both_reviews=!both_reviews">All</div>
                                            <div :class="my_reviews ? '' : 'not'" class="datum" @click="my_reviews=!my_reviews">My Reviews</div>
                                            <div :class="me_reviews ? '' : 'not'" class="datum" v-if="allResources.map(resource => resource.user).includes(user.id)" @click="me_reviews=!me_reviews">Reviews for Me</div>
                                        </div>
                                    </div>
                                    <div class="filter-item">
                                        <label>Stars</label>
                                        <div class="row">
                                            <div :class="all_stars ? '' : 'not'" class="datum" @click="all_stars=!all_stars">All</div>
                                            <div :class="filter_zero ? '' : 'not'" class="datum" @click="filter_zero=!filter_zero">0</div>
                                            <div :class="filter_one ? '' : 'not'" class="datum" @click="filter_one=!filter_one">1</div>
                                            <div :class="filter_two ? '' : 'not'" class="datum" @click="filter_two=!filter_two">2</div>
                                            <div :class="filter_three ? '' : 'not'" class="datum" @click="filter_three=!filter_three">3</div>
                                            <div :class="filter_four ? '' : 'not'" class="datum" @click="filter_four=!filter_four">4</div>
                                            <div :class="filter_five ? '' : 'not'" class="datum" @click="filter_five=!filter_five">5</div>
                                        </div>
                                    </div>
                                    <div class="filter-item">
                                        <label>Media</label>
                                        <div class="row">
                                            <div :class="all_media ? '' : 'not'" class="datum" @click="all_media=!all_media">All</div>
                                            <div :class="filter_images ? '' : 'not'" class="datum" @click="filter_images=!filter_images">Images</div>
                                            <div :class="filter_video ? '' : 'not'" class="datum" @click="filter_video=!filter_video">Video</div>
                                            <div :class="no_reviews ? '' : 'not'" class="datum" @click="no_reviews=!no_reviews">None</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="addingReview" class="item">
                <p id="stars-text">Stars</p>
                <div id="my-rating">
                    <i id="rating-one" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                    <i id="rating-two" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                    <i id="rating-three" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                    <i id="rating-four" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                    <i id="rating-five" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                    <span>{{ rating }}</span>
                </div>
                <p id="rating-error" v-if="rating_error">Select a rating</p>
            </div>
            <div v-if="addingReview" class="item">
                <p>Title</p>
                <input type="text" id="review-title" @input="reset_validity(0)">
            </div>
            <div v-if="addingReview" class="item">
                <p>Seller</p>
                <select id="resource-add-seller">
                    <option :value="resource.id" v-for="resource in possible_sellers(false)">
                        <p>{{ resource.author }}</p>
                    </option>
                </select>
            </div>
            <div v-if="addingReview" class="item">
                <p>Review</p>
                <textarea id="review-text" @input="reset_validity(0)"></textarea>
            </div>
            <div id="media" v-if="addingReview">
                <div id="image">
                    <p>Image</p>
                    <input :disabled="api" id="image1" type="file" accept=".png" @change="show_image">
                    <label for="image1" class="media-square">
                        <i v-if="image.name === ''" class="bi bi-plus-lg"></i>
                        <img id="img" alt="image1">
                        <button :disabled="api" v-if="!(image.name === '')" @click="remove_image"><i class="bi bi-x-lg delete"></i></button>
                    </label>
                </div>
                <div id="video">
                    <p>Video</p>
                    <input :disabled="api" id="video1" type="file" accept=".mp4" @change="(event: Event) => show_video(event, 0)">
                    <label for="video1" class="media-square">
                        <i v-if="video.name === ''" class="bi bi-plus-lg"></i>
                        <video controls id="vid"></video>
                        <button :disabled="api" v-if="!(video.name === '')" @click="(event: Event) => remove_video(event,0)"><i class="bi bi-x-lg delete"></i></button>
                    </label>
                </div>
            </div>
            <div id="buttons" v-if="addingReview">
                <button :disabled="api" id="save-review" @click="save_review">Save Review</button>
                <button :disabled="api" id="delete-review" @click="addingReview = false">Cancel</button>
            </div>
        </div>
        <div id="reviews">
            <p id="no-reviews-to-display" v-if="all_reviews.length === 0">No reviews to display</p>
            <div :name="review.id.toString()" v-if="get_all_reviews" id="showing-reviews" class="reviews-review" v-for="review in all_reviews">
                <div class="review-heading">
                    <div id="review-heading-one" class="review-heading-one-height">
                        <div v-if="!editing || editing && editing_review !== review.id">
                            <i class="bi bi-person-circle icon"></i>
                        </div>
                        <div class="title-area">
                            <p v-if="editing && editing_review === review.id" style="font-weight: normal;">Stars</p>
                            <div class="review-rating">
                                <i v-if="!editing || editing && editing_review !== review.id" class="bi bi-star-fill" style="color: orange;"></i>
                                <i v-if="editing && editing_review === review.id" class="bi bi-star-fill" id="rating-one" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="(!editing || editing && editing_review !== review.id) && review.rating >= 2" class="bi bi-star-fill" style="color: orange;" ></i>
                                <i v-if="editing && editing_review === review.id && review.rating >= 2" id="rating-two" class="bi bi-star-fill" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="(!editing || editing && editing_review !== review.id) && review.rating < 2"class="bi bi-star-fill"></i>
                                <i v-if="editing && editing_review === review.id && review.rating < 2" id="rating-two" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                                <i v-if="(!editing || editing && editing_review !== review.id) && review.rating >= 3" class="bi bi-star-fill" style="color: orange;"></i>
                                <i v-if="editing && editing_review === review.id && review.rating >= 3" id="rating-three" class="bi bi-star-fill" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="(!editing || editing && editing_review !== review.id) && review.rating < 3" class="bi bi-star-fill"></i>
                                <i v-if="editing && editing_review === review.id && review.rating < 3" id="rating-three" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                                <i v-if="(!editing || editing && editing_review !== review.id) && review.rating >= 4" class="bi bi-star-fill" style="color: orange;"></i>
                                <i v-if="editing && editing_review === review.id && review.rating >= 4" id="rating-four" class="bi bi-star-fill" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="(!editing || editing && editing_review !== review.id) && review.rating < 4" class="bi bi-star-fill"></i>
                                <i v-if="editing && editing_review === review.id && review.rating < 4" id="rating-four" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                                <i v-if="(!editing || editing && editing_review !== review.id) && review.rating == 5" class="bi bi-star-fill" style="color: orange;"></i>
                                <i v-if="editing && editing_review === review.id && review.rating == 5" id="rating-five" class="bi bi-star-fill" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="(!editing || editing && editing_review !== review.id) && review.rating < 5" class="bi bi-star-fill"></i>
                                <i v-if="editing && editing_review === review.id && review.rating < 5" id="rating-five" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                                <span v-if="editing && editing_review === review.id" id="stars-span">{{ parseFloat(rating.toString()) }}</span>
                            </div>
                            <p v-if="!editing || editing_review !== review.id" id="title">{{ review.title }} (Ordered from {{ users.find(user => user.id === allResources.find(resource => resource.id === review.resource)?.user)?.username }})</p>
                            <p v-if="!editing || editing && editing_review !== review.id" class="date">{{ to_date(review.upload_date) }}</p>
                        </div>
                    </div>
                    <div v-if="!editing || editing && editing_review !== review.id" class="review-media">
                        <img class="review-image" @click="image_full_url=`${url}${review.image}`, image_full=true" v-if="review.image" :src="`${url}${review.image}`" alt="image">
                        <video class="review-video" @click="video_full_url=`${url}${review.video}`; video_full=true" v-if="review.video" :src="`${url}${review.video}`"></video>
                    </div>
                </div>
                <div v-if="editing && editing_review === review.id">
                    <div class="item">
                        <p>Title</p>
                        <input type="text" id="specific-review-title" :value="review.title" @input="reset_validity(1, review.id)">
                    </div>
                    <div class="item top-marg">
                        <p>Seller</p>
                        <select :id="`${review.id}`" :value="review.resource">
                            <option :value="resource.id" v-for="resource in possible_sellers(true)">
                                <p>{{ users.find(user => user.id === resource.user)?.username }}</p>
                            </option>
                        </select>
                    </div>
                </div>
                <p class="top-marg text-desc" v-if="editing && editing_review === review.id">Review</p>
                <textarea :disabled="!editing || editing && editing_review !== review.id" :id="`${review.id}review-review`" :value="review.review" class="review-review" @input="reset_validity(1, review.id)">{{ review.review }}</textarea>
                <div id="media" v-if="editing && editing_review === review.id">
                    <div id="image">
                        <p>Image</p>
                        <input :disabled="api" id="image1" type="file" accept=".png" @change="show_image">
                        <label for="image1" class="media-square">
                            <i v-if="image.name === ''" class="bi bi-plus-lg"></i>
                            <img id="img" alt="image1" :src="`${url}${review.image}`">
                            <button :disabled="api" v-if="!(image.name === '')" @click="remove_image"><i class="bi bi-x-lg delete"></i></button>
                        </label>
                    </div>
                    <div id="video">
                        <p>Video</p>
                        <input :disabled="api" id="video1" type="file" accept=".mp4" @change="(event: Event) => show_video(event,1)">
                        <label for="video1" class="media-square">
                            <i v-if="video.name === ''" class="bi bi-plus-lg"></i>
                            <video controls id="vid1" :src="`${url}${review.video}`"></video>
                            <button :disabled="api" v-if="!(video.name === '')" @click="(event: Event) => remove_video(event,1)"><i class="bi bi-x-lg delete"></i></button>
                        </label>
                    </div>
                </div>
                <div v-if="review.user === user.id" id="edit-review">
                    <button :disabled="api" v-if="!editing || editing && editing_review !== review.id" class="edit" @click="edit_review(review)"><i class="bi bi-pencil-fill"></i></button>
                    <button :disabled="api" v-if="editing && editing_review === review.id" class="save" @click="save_edited_review(review)"><i class="bi bi-floppy-fill"></i></button>
                    <button :disabled="api" v-if="editing && editing_review === review.id" class="rewind" @click="close_review(review)"><i class="bi bi-arrow-counterclockwise"></i></button>
                    <button :disabled="api" class="trash" @click="delete_review(review)"><i class="bi bi-trash3-fill"></i></button>
                </div>
            </div>
            <div v-if="error!==''">
                <Error :message="error" @close-error="error=''" />
            </div>
            <div v-if="image_full || video_full" id="border" @click="image_full_url='',image_full=false,video_full=false,video_full_url=''">
                <div class="full_media" v-if="image_full && (image_full_url!=='')">
                    <i id="x" class="bi bi-x-lg big-x"></i>
                    <img :src="image_full_url">
                </div>
                <div class="full_media" v-if="video_full && (video_full_url!=='')">
                    <i id="x" class="bi bi-x-lg big-x"></i>
                    <video :src="video_full_url" controls></video>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import ViewSellers from './ViewSellers.vue';
    import type { Cart, CartResource, Exchange, Resource, Review, User, Wishlist } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import Stars from './Stars.vue';
    import { useUsersStore } from '@/stores/users';
    import Error from '../user experience/error/Error.vue';
    import { useURLStore } from '@/stores/url';
    export default defineComponent({
        components: { Stars, ViewSellers, Error },
        data(): {
            video_full: boolean,
            video_full_url: string,
            image_full: boolean,
            image_full_url: string,
            api: boolean,
            no_reviews: boolean,
            filter_zero: boolean,
            all_stars: boolean,
            all_media: boolean,
            error: string,
            exchanging: boolean,
            seen_review: boolean,
            buying_now: boolean,
            in_wishlist: boolean,
            currentResource: Resource,
            all_reviews: Review[],
            seller: number,
            cart_resource: CartResource,
            addingReview: boolean,
            rating_error: boolean,
            viewing_sellers: boolean,
            review: number,
            editing: boolean,
            rating: number,
            image: File,
            toggle_filter: boolean,
            video: File,
            editing_review: number,
            sort_by: 'earliest' | 'latest' | 'high' | 'low' | 'positive' | 'negative',
            my_reviews: boolean,
            me_reviews: boolean,
            filter_one: boolean,
            filter_two: boolean,
            filter_three: boolean,
            filter_four: boolean,
            filter_five: boolean,
            filter_images: boolean,
            both_reviews: boolean,
            filter_video: boolean,
            cart_price: number,
        } { return {
            all_stars: true,
            all_media: true,
            exchanging: false,
            video_full: false,
            video_full_url: '',
            image_full: false,
            image_full_url: '',
            seen_review: false,
            filter_zero: true,
            no_reviews: true,
            in_wishlist: false,
            currentResource: {} as Resource,
            cart_price: 0,
            api: false,
            seller: -1,
            cart_resource: {
                id: -1,
                resource: -1,
                number: 0
            },
            error: '',
            all_reviews: [],
            buying_now: true,
            toggle_filter: false,
            filter_one: true,
            filter_five: true,
            filter_four: true,
            filter_images: true,
            my_reviews: true,
            me_reviews: true,
            filter_three: true,
            filter_two: true,
            filter_video: true,
            sort_by: 'latest',
            editing_review: -1,
            addingReview: false,
            rating: 0,
            review: -1,
            viewing_sellers: false,
            both_reviews: true,
            editing: false,
            rating_error: false,
            video: new File([''], ''),
            image: new File([''], ''),
        }},
        methods: {
            has_resources(): boolean {
                // If resource sellers are only the current user, false will be returned as the user cannot exchange items with themself
                const resources = useResourcesStore().resources.filter(resource => (resource.user === this.user.id) && !resource.is_draft && (resource.stock > 0))
                const own_resource = this.allResources.find(resource => resource.user !== this.user.id) ? false : true
                return (resources.length > 0) && (!own_resource)
            },
            check_all_reviews(): void {
                this.both_reviews = this.me_reviews && this.my_reviews 
            },
            check_all_stars(): void {
                this.all_stars = this.filter_zero && this.filter_three && this.filter_one && this.filter_two && this.filter_five && this.filter_four 
            },
            check_all_media(): void {
                this.all_media = this.filter_images && this.filter_video && this.no_reviews
            },
            async exchange(): Promise<void> {
                // Taking users to paeg where they can exchange resources
                if (this.seller === -1) {
                    this.viewing_sellers = true
                    this.exchanging = true
                    return
                }
                if ((this.allResources.find(resource => resource.id === this.seller) as Resource).user === this.user.id) {
                    this.error = 'You cannot exchange resources with yourself. Change the seller if you can.'
                    this.viewing_sellers = true
                    return
                }
                if (Object.keys(this.resource).length > 0) {
                    const resource: Resource | undefined = this.allResources.find(resource => resource.id === this.seller)
                    if (!resource) {
                        this.error = 'Error finding resource. Please try again.'
                        return
                    }
                    const exchangeResponse: Response = await fetch(`${useURLStore().url}/api/exchange/user/${this.user.id}/seller/${resource.user}/resource/${this.seller}/`, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf,
                            'Content-Type' : 'application/json',
                        },
                    })
                    if (!exchangeResponse.ok) { this.error = 'Error editing wishlist. Please try again.' }
                    else { 
                        const data: {user: User, exchange: Exchange} = await exchangeResponse.json()
                        useUserStore().saveUser(data.user)
                        useUsersStore().updateUser(data.user)
                        window.location.href = `/exchange/${data.exchange.id}`
                    }
                } else {
                    this.error = 'Error finding resource. Please try again.'
                }
            },
            buy_now(): void {
                // Taking users to fast checkout where they do not have to re-enter their details
                this.buying_now = true
                if (this.seller === -1) {
                    this.viewing_sellers = true
                    return
                }
                nextTick(() => {
                    if (!this.buying_now || this.cart_resource.resource === -1) {
                        return
                    } else {
                        window.location.href = `/fast-checkout/${this.cart_resource.resource}`
                    }
                })
            },
            unauth_currency(resource: Resource): string {
                return resource.price_currency === 'GBP' ? '£' : resource.price_currency === 'USD' ? '$' : '€' 
            },
            async edit_wishlist(): Promise<void> {
                // User can add or remove resource from wishlist
                if (this.cart_resource.number !== 0) {
                    await this.update_cart_db('DELETE', this.cart_resource.id, -1)
                }
                const editWishlistResponse: Response = await fetch(`${useURLStore().url}/api/user/${this.user.id}/wishlist/`, {
                    method: this.in_wishlist ? 'DELETE' : 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(this.allResources[0].id)
                })
                if (!editWishlistResponse.ok) { this.error = 'Error editing wishlist. Please try again.' }
                else { 
                    const data: { wishlist: Wishlist } = await editWishlistResponse.json()
                    this.in_wishlist = !this.in_wishlist
                    useUserStore().updateWishlist(data.wishlist)
                }
            },
            show_sellers() {
                this.viewing_sellers = true
                nextTick(() => {
                    const view_sellers = document.getElementById('view-sellers-container')
                    view_sellers?.scrollIntoView()
                })
            },
            update_seller(resource: number): void {
                // Used to update the resource seller the user will be buying the resources from
                this.viewing_sellers = false
                this.seller = resource
                if (this.cart_resource.number === 0) {
                    this.cart_resource.number +=1
                    this.update_cart_db('POST', -1, this.seller)
                    this.get_cart()
                } else {
                    this.update_cart_db('PUT', this.cart_resource.id, resource)
                    this.get_cart()
                }
            },
            async get_cart(): Promise<void> {
                // Find cart resource associated with the curernt resource being viewed
                const cart: Response = await fetch(`${useURLStore().url}/api/cart/${this.user.id}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                })
                const data: Cart = await cart.json()
                data.resources.forEach(cartResource => {
                    this.allResources.forEach(resource => {
                        if (cartResource.resource === resource.id) {
                            this.cart_resource = cartResource
                            this.seller = cartResource.resource
                            return
                        } 
                    })
                })
                if (!(data.resources.find(cart_resoure => cart_resoure.resource === this.seller))) {
                    this.cart_resource = {
                        id: -1,
                        resource: -1,
                        number: 0
                    }
                }
                useUserStore().updateCart(data)
            },
            async update_cart_db(method: string, cart_number: number, resource: number): Promise<void> {
                // Update numebr of items in cart
                const updateCart: Response = await fetch(`${useURLStore().url}/api/update-cart/user/${this.user.id}/cart/${cart_number}/resource/${resource}/`, {
                    method: method,
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf,
                        'Content-Type' : 'application/json',
                    },
                    body: JSON.stringify(this.cart_resource.number)
                })
                if (!updateCart.ok) {
                    this.error = 'Error updating cart. Please try again.'
                    return
                }
                const data: {resource: CartResource, cart: Cart, wishlist: Wishlist} = await updateCart.json()
                useUserStore().updateCart(data.cart)
                useUserStore().updateWishlist(data.wishlist)
                useUsersStore().updateUser(this.user)
                this.get_cart()
            },
            update_cart(number: number): void {
                // Determining logic of cart updates
                if (this.cart_resource.number === 0 && number === -1) {
                    // User cannot reduce number of items in cart from 0
                    return
                }
                if (this.cart_resource.number === 0) {
                    // User chooses seller before adding item to cart
                    if (this.allResources.filter(resource => resource.user !== this.user.id).length === 1) {
                        this.update_seller((this.allResources.find(resource => resource.user !== this.user.id) as Resource).id)                      
                        return
                    }
                    this.viewing_sellers = true
                    return;
                }
                this.cart_resource.number += number
                if (this.cart_resource.number === 0) {
                    this.update_cart_db('DELETE', this.cart_resource.id, -1)
                    nextTick(() => {
                        this.currentResource = {} as Resource
                    })
                    return
                }
                this.update_cart_db('PUT', this.cart_resource.id, this.cart_resource.resource)
            },
            toggleFilter(): void {
                // Determines whether filter options show
                this.toggle_filter = !this.toggle_filter
                if (this.toggle_filter) {
                    document.addEventListener('click', (event: Event) => {
                        const target: HTMLElement = event.target as HTMLElement
                        if (!(target.id === 'filtering-section' || target.id === 'clickable' || target.id === 'toggle-filter')) {
                            this.toggle_filter=false
                        }
                    })
                } 
            },
            close_review(review: Review): void {
                // User stops editing review
                document.getElementById(`${review.id}review-review`)?.classList.remove('review-review-desc')
                document.getElementById('review-heading-one')?.classList.add('review-heading-one-height')
                document.getElementById('review-heading-one')?.classList.remove('review-heading-one-reviewing-height')
                this.editing = false
                this.review = -1
            },
            edit_review(review: Review): void {
                // Allow user to edit review
                this.editing_review = review.id
                this.editing = true
                this.addingReview = false
                nextTick(() => { 
                    this.review = review.id
                    const description: HTMLTextAreaElement = document.getElementById(`${review.id}review-review`) as HTMLTextAreaElement
                    description.scrollIntoView()
                    const reviews: HTMLDivElement = document.getElementById('reviews') as HTMLDivElement
                    const img: HTMLImageElement = reviews.querySelector('img') as HTMLImageElement
                    const vid: HTMLVideoElement = document.getElementById('vid1') as HTMLVideoElement
                    if (review.image) {
                        this.image = new File([], img.src)
                        img.style.display = 'block'
                    } else {
                        this.image = new File([], '')
                    }
                    if (review.video) {
                        this.video = new File([], vid.src)
                        vid.style.display = 'block'
                    } else {
                        this.video = new File([], '')
                    }
                    document.getElementById(`${review.id}review-review`)?.classList.add('review-review-desc')
                    document.getElementById('review-heading-one')?.classList.remove('review-heading-one-height')
                    document.getElementById('review-heading-one')?.classList.add('review-heading-one-reviewing-height')
                    this.rating = review.rating
                })
            },
            async delete_review(review: Review) {
                // Allows user to delete review
                this.api = true
                const response: Response = await fetch(`${useURLStore().url}/api/user/${this.user.id}/review/${review.id}/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                })
                if (!response.ok) {
                    this.error = 'Error deleting review. Please try again.'
                    return
                }
                const resource: {resource: Resource, users: User[]} = await response.json()
                useResourcesStore().updateResource(resource.resource)
                useUsersStore().updateUsers(resource.users)
                this.fill_stars()
                this.api = false
            },
            to_date(date: string): string {
                // Performing review date conversion
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
            remove_video(event:Event, num: number): void {
                // Remove uploaded video
                event.preventDefault()
                const vid: HTMLImageElement = document.getElementById(num === 0 ? 'vid' : 'vid1') as HTMLImageElement
                const video: HTMLInputElement = document.getElementById('video1') as HTMLInputElement
                if (vid && video) {
                    vid.src = ''
                    this.video = new File([''], '')
                    vid.style.display = 'none'
                    video.value = ''
                }
            },
            show_video(event: Event, num: number): void {
                // Upload video
                const inputElement: HTMLInputElement = event.target as HTMLInputElement
                if (!inputElement.files) return
                const video: File = inputElement.files[0]
                if (!video) return
                const vid: HTMLImageElement = document.getElementById(num === 0 ? 'vid' : 'vid1') as HTMLImageElement
                if (!vid) return
                vid.src = URL.createObjectURL(video)
                vid.style.display = 'block'
                this.video = video
            },
            remove_image(event: Event): void {
                // Remove uploaded image
                event.preventDefault()
                const img: HTMLImageElement = document.getElementById('img') as HTMLImageElement
                const image: HTMLInputElement = document.getElementById('image1') as HTMLInputElement
                if (img && image) {
                    img.src = ''
                    this.image = new File([''], '')
                    img.style.display = 'none'
                    image.value = ''
                }
            },
            show_image(event: Event): void {
                // Upload image
                const inputElement: HTMLInputElement = event.target as HTMLInputElement
                if (!inputElement.files) return
                const image: File = inputElement.files[0]
                if (!image) return
                const img: HTMLImageElement = document.getElementById('img') as HTMLImageElement
                if (!img) return
                img.src = URL.createObjectURL(image)
                img.style.display = 'block'
                this.image = image
            },
            add_review(): void {
                // Allow user to see input values to add review
                this.addingReview = true
                this.editing = false
                nextTick(() => {
                    document.getElementById('stars-text')?.scrollIntoView()
                    this.image = new File([''], '')
                    this.video = new File([''], '')
                    this.rating = 0
                })
            },
            reset_validity(number: number, review?: number): void {
                // Clear input error messages
                const title: HTMLInputElement = document.getElementById(number === 0 ? 'review-title' : 'specific-review-title') as HTMLInputElement
                const description: HTMLTextAreaElement = document.getElementById(number === 0 ? 'review-text' : `${review}review-review`) as HTMLTextAreaElement
                title.setCustomValidity('')
                title.reportValidity()
                description.setCustomValidity('')
                description.reportValidity()
            },
            async save_edited_review(review: Review): Promise<void> {
                // Validating review input and saving edited review
                const title: HTMLInputElement = document.getElementById('specific-review-title') as HTMLInputElement
                const description: HTMLTextAreaElement = document.getElementById(`${review.id}review-review`) as HTMLTextAreaElement

                if (!title && !description) return

                if (title.value === '') {
                    title.setCustomValidity('Cannot be empty')
                    title.reportValidity()
                    return
                } 

                if (description.value === '') {
                    description.setCustomValidity('Cannot be empty')
                    description.reportValidity()
                    return
                } 

                this.reset_validity(1, review.id)
                const seller_element: HTMLSelectElement = document.getElementById(`${review.id}`) as HTMLSelectElement
                const seller = seller_element.value
                const data: FormData = new FormData()
                data.append('stars', this.rating.toString())
                data.append('title', title.value)
                data.append('description', description.value)
                data.append('image', this.image)
                data.append('video', this.video)
                data.append('old_resource', review.resource.toString())
                this.api = true
                let savedReview: Response = await fetch(`${useURLStore().url}/api/user/${this.user.id}/edit-review/${review.id}/${seller}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: data
                })
                if(!savedReview.ok) {
                    this.error = 'Error editing review. Please try again.'
                    return
                }
                let reviewData: {old_resource: Resource, new_resource : Resource, users: User[]} = await savedReview.json()
                useResourcesStore().editResource(reviewData.old_resource, reviewData.new_resource)
                useUsersStore().updateUsers(reviewData.users)
                this.close_review(review)
                this.api = false
            },
            async save_review(): Promise<void> {
                // Validating review input and saving new review
                const title: HTMLInputElement = document.getElementById('review-title') as HTMLInputElement
                const description: HTMLTextAreaElement = document.getElementById('review-text') as HTMLTextAreaElement

                if (!title && !description) return

                if (title.value === '') {
                    title.setCustomValidity('Cannot be empty')
                    title.reportValidity()
                    return
                } 

                if (description.value === '') {
                    description.setCustomValidity('Cannot be empty')
                    description.reportValidity()
                    return
                } 
                
                if (this.rating === 0) {
                    this.rating_error = true
                    document.getElementById('my-rating')?.scrollIntoView()
                    return
                }

                this.rating_error = false
                this.reset_validity(0)
                const seller_element: HTMLSelectElement = document.getElementById('resource-add-seller') as HTMLSelectElement
                const seller = seller_element.value
                const data: FormData = new FormData()
                data.append('stars', this.rating.toString())
                data.append('title', title.value)
                data.append('description', description.value)
                data.append('image', this.image)
                data.append('video', this.video)
                this.api = true
                let savedReview: Response = await fetch(`${useURLStore().url}/api/user/${this.user.id}/review/${seller}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: data
                })
                let resource: { resource: Resource, users: User[]} = await savedReview.json()
                useResourcesStore().updateResource(resource.resource)
                useUsersStore().updateUsers(resource.users)
                this.addingReview = false
                this.api = false
            },
            show_potential_rating(event: Event): void {
                // Allow colours to change as user hovers over number of stars
                let star: HTMLElement = event.target as HTMLElement
                const star1: HTMLElement = document.getElementById('rating-one') as HTMLElement
                const star2: HTMLElement = document.getElementById('rating-two') as HTMLElement
                const star3: HTMLElement = document.getElementById('rating-three') as HTMLElement
                const star4: HTMLElement = document.getElementById('rating-four') as HTMLElement
                const star5: HTMLElement = document.getElementById('rating-five') as HTMLElement
                if (star1 && star2 && star3 && star4 && star5) {
                    star1.style.color = 'orange'
                    star2.style.color = star !== star1 ? 'orange' : ''
                    star3.style.color = star !== star1 && star !== star2 ? 'orange' : ''
                    star4.style.color = star === star4 || star === star5 ? 'orange' : ''
                    star5.style.color = star === star5 ? 'orange' : ''
                }
                this.rating = star === star1 ? 1 : star === star2 ? 2 : star === star3 ? 3 : star === star4 ? 4 : 5
            },
            async listedprice(resource: Resource): Promise<number> {
                // Performing currency conversion
                if (resource === undefined) return 0
                if (Object.keys(this.user).length === 0) return resource.price
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
            fill_stars(): void {
                nextTick(() => {
                    const star1: HTMLElement = document.getElementById('one') as HTMLElement
                    const star2: HTMLElement = document.getElementById('two') as HTMLElement
                    const star3: HTMLElement = document.getElementById('three') as HTMLElement
                    const star4: HTMLElement = document.getElementById('four') as HTMLElement
                    const star5: HTMLElement = document.getElementById('five') as HTMLElement
                    if (star1 && star2 && star3 && star4 && star5) {
                        star1.style.color = this.average_rating >= 1 ? 'orange' : ''
                        star2.style.color = this.average_rating >= 2 ? 'orange' : ''
                        star3.style.color = this.average_rating >= 3 ? 'orange' : ''
                        star4.style.color = this.average_rating >= 4 ? 'orange' : ''
                        star5.style.color = this.average_rating == 5 ? 'orange' : ''
                    }
                })
            },
            possible_sellers(editing: boolean): Resource[] {
                if (Object.keys(this.user).length === 0) return this.allResources
                // Filter so that user cannot review seller twice; check who they've reviewed and remove them
                let resources = this.allResources.filter(resource =>  resource.user !== this.user.id)
                if (editing) {
                    return resources.filter(resource => resource.reviews.length === 0 || resource.reviews.some(review => this.review === review.id || review.user !== this.user.id))
                }
                return resources.filter(resource => resource.reviews.length === 0 || resource.reviews.some(review => review.user !== this.user.id))
            },
            scrollReviewsIntoView(): void {
                const allReviews: HTMLDivElement = document.getElementById('showing-reviews') as HTMLDivElement
                if (allReviews) {
                    allReviews.scrollIntoView()
                }
            },
            async reviews_ordered(reviews: Review[]): Promise<void> {
                // Sorting reviews
                const sentiment = await this.resource_sentiment
                this.all_reviews = reviews.sort((review1, review2) => 
                    this.sort_by === 'positive' ?
                        sentiment[review2.id] - sentiment[review1.id]
                        : sentiment[review1.id] - sentiment[review2.id]
                )
            },
            async get_all_reviews(): Promise<void> {
                // Retrieving all reviews - sorting and filtering 
                let reviews: Review[] = []
                this.allResources.forEach((resource) =>
                    reviews.push(...resource.reviews)
                )
                reviews = reviews.filter(review => {
                    if (
                        (   (this.filter_one && this.filter_two && this.filter_three && this.filter_five && this.filter_four) || 
                            (   (this.filter_one && parseFloat(review.rating.toString()) === 1)
                            || (this.filter_zero && parseFloat(review.rating.toString()) === 0)
                            || (this.filter_two && parseFloat(review.rating.toString()) === 2)
                            || (this.filter_three && parseFloat(review.rating.toString()) === 3)
                            || (this.filter_four && parseFloat(review.rating.toString()) === 4)
                            || (this.filter_five && parseFloat(review.rating.toString()) === 5)
                            )
                        )
                        && (
                            (this.filter_images && this.filter_video && this.no_reviews) || 
                            (   (this.filter_images && (review.image !== null))
                                || (this.filter_video && (review.video !== null))
                                || (this.no_reviews && ((review.image === null) && review.video === null))
                            )
                        )
                        && (
                            (this.my_reviews && this.me_reviews) || 
                            (   (this.me_reviews && (this.allResources.find(resource => resource.id === review.resource)))
                                || (this.my_reviews && (review.user === this.user.id))
                            )
                        )
                    ) {
                        return true
                    }
                    return false
                })
                if (this.sort_by === 'positive' || this.sort_by === 'negative') {
                    reviews = reviews.sort((review1, review2) => review1.id - review2.id)
                        return this.reviews_ordered(reviews)
                }
                this.all_reviews = reviews.sort((review1, review2) => {
                    if (this.sort_by === 'earliest' && review1.upload_date > review2.upload_date
                        || this.sort_by === 'latest' && review1.upload_date < review2.upload_date
                        || this.sort_by === 'low' && review1.rating > review2.rating
                        || this.sort_by === 'high' && review1.rating < review2.rating
                    ) {
                        return 1
                    }  
                    return -1
                })
            },
            updateWishlist(wishlist: Wishlist): void {
                const wishlist_item = wishlist.resources.map(item => item.resource)
                this.in_wishlist = false
                const mapped_resources = this.allResources.map(res => res.id)
                for (let item of wishlist_item) {
                    if (mapped_resources.includes(item)) {
                        this.in_wishlist = true
                        return
                    }
                }
            }
        },
        computed: {
            url(): string {
                return useURLStore().url
            },
            users(): User[] {
                return useUsersStore().users
            },
            async resource_sentiment(): Promise<{[key: number] : number}> {
                // Storing resource review sentiment to be used when ordering reviews
                const response: Response = await fetch(`${useURLStore().url}/api/sentiment/${this.allResources[0].name}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                })
                const scores: {[key: number] : number} = await response.json()
                return scores
            },
            total_ratings(): number {
                // Find total number of reviews
                let number_of_reviews: number = 0
                this.allResources.forEach((resource) => {
                    resource.reviews.forEach((review) => {
                        number_of_reviews += 1
                })})
                this.fill_stars()
                return number_of_reviews
            },
            average_rating(): number {
                // Determine average review rating
                let sum_of_rating: number = 0
                this.allResources.forEach((resource) => {
                    resource.reviews.forEach((review) => {
                        sum_of_rating += parseFloat(review.rating.toString())
                })})
                this.fill_stars()
                if (this.total_ratings === 0) return 0
                return (sum_of_rating/this.total_ratings)
            },
            async written_review(): Promise<boolean> {
                return this.all_reviews.find(review => review.user === this.user.id) !== undefined
            },
            user(): User {
                return useUserStore().user
            },
            reviews(): Review[] {
                return []
            },
            allResources(): Resource[] {
                const window_location: string[] = window.location.href.split('/')
                const id: string = window_location[4]
                let returnedResources = [] as Resource[]
                const initial_resource: Resource | undefined = useResourcesStore().resources.find(resource => resource.id === parseInt(id))
                if (initial_resource === undefined) return []
                if (initial_resource.unique) {
                    returnedResources.push(initial_resource)
                    return returnedResources
                }
                const resources: Resource[] = useResourcesStore().resources.filter(resource => resource.name === initial_resource.name && resource.author === initial_resource.author && !resource.unique && parseInt(resource.stock.toString()) > 0 && !resource.is_draft && (resource.allow_collection || resource.allow_delivery))
                returnedResources.push(...resources)
                return returnedResources
            },
            resource(): Resource | {} {
                if (this.seller !== -1) {
                    return this.allResources.find(resource => resource.id === this.seller) as Resource
                }
                return this.allResources[0]
            },
        },
        watch: {
            both_reviews(): void {
                // Updating whether filter item is true
                if (this.both_reviews) {
                    this.me_reviews = true
                    this.my_reviews = true
                }
            },
            all_stars(): void {
                // Updating whether filter item is true
                if (this.all_stars) {
                    this.filter_one = true
                    this.filter_zero = true
                    this.filter_two = true
                    this.filter_three = true
                    this.filter_four = true
                    this.filter_five = true
                }
            },
            all_media(): void {
                // Updating whether filter item is true
                if (this.all_media) {
                    this.filter_images = true
                    this.filter_video = true
                    this.no_reviews = true
                }
            },
            async seller(new_seller: number): Promise<void> {
                if (new_seller !== -1 && this.buying_now) {
                    this.buy_now()
                }
                if (this.cart_resource.number === 0) {
                    this.cart_price = 0
                    return
                }
                nextTick(async () => {
                    if (this.cart_resource.number === 0) {
                        this.cart_price = 0
                        return
                    }
                    // Update cart price
                    let price = await this.listedprice(this.allResources.find(resource => resource.id === this.cart_resource.resource) as Resource)
                    this.cart_price = parseFloat(price.toString().replace('€','').replace('£','').replace('$',''))
                    const resource: Resource | undefined = this.allResources.find(resource => resource.id === this.cart_resource.resource)
                    if (resource) this.currentResource = resource
                })
            },
            "user.wishlist"(wishlist: Wishlist): void {
                this.updateWishlist(wishlist)
            },
            async "cart_resource.number"(new_number: number): Promise<void> {
                // Updating styles based on whether or not + is shown for cart update
                if (this.cart_resource.number === 0) {
                    nextTick(() => {
                        let line: HTMLHRElement = document.getElementById('separator') as HTMLHRElement
                        let plus: HTMLParagraphElement = document.getElementById('plus') as HTMLParagraphElement
                        if (line && plus) {
                            line.style.display = 'none'
                            plus.style.borderTopRightRadius = '0.4rem'
                            plus.style.borderBottomRightRadius = '0.4rem'
                        }
                    })
                }
                if (new_number === 0) {
                    this.seller = -1
                }
                nextTick(async () => {
                    if (this.cart_resource.number === 0) {
                        this.cart_price = 0
                        return
                    }
                    // Update cart price
                    let price = await this.listedprice(this.allResources.find(resource => resource.id === this.cart_resource.resource) as Resource)
                    this.cart_price = parseFloat(price.toString().replace('€','').replace('£','').replace('$',''))
                    const resource: Resource | undefined = this.allResources.find(resource => resource.id === this.cart_resource.resource)
                    if (resource) this.currentResource = resource
                })
            },
            async cart_resource(new_resource: CartResource): Promise<void> {
                nextTick(async () => {
                    if (this.cart_resource.number === 0) {
                        this.cart_price = 0
                        return
                    }
                    // Update cart price
                    let price = await this.listedprice(this.allResources.find(resource => resource.id === this.cart_resource.resource) as Resource)
                    this.cart_price = parseFloat(price.toString().replace('€','').replace('£','').replace('$',''))
                    const resource: Resource | undefined = this.allResources.find(resource => resource.id === this.cart_resource.resource)
                    if (resource) this.currentResource = resource
                    if (this.buying_now) this.buy_now()
                })
            },
            viewing_sellers(new_viewing): void {
                if (this.exchanging) {
                    this.exchange()
                    return
                }
                const div: HTMLDivElement = document.getElementById('resource-view') as HTMLDivElement
                if (div && new_viewing) {
                    div.style.overflowY = 'hidden'
                } else if (div && !new_viewing) {
                    div.style.overflowY = 'scroll'
                }
            },
            async user(new_user: User): Promise<void> {
                this.get_cart()
                for (const resource of this.allResources) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resource(resource: Resource): Promise<void> {
                this.fill_stars()
                resource.price = await this.listedprice(resource)
                // Adding viewed resource to user search history
                fetch(`${useURLStore().url}/api/semantic-search/${Object.keys(this.user).length > 0 ? this.user.id : -1}/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'Content-Type' : 'application/json',
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(resource.name)
                })
            },
            sort_by() {
                this.get_all_reviews()
            },
            allResources(): void {
                // Updating this.seller, which stores the id corresponding to the resource in the cart
                if (Object.keys(this.user).length > 0) {
                    this.updateWishlist(this.user.wishlist)
                    this.get_cart()
                    for (const resource of this.allResources) {
                        const item = this.user.cart.resources.find(item => item.resource === resource.id)
                        if (item) {
                            this.seller = resource.id
                        }
                    }
                }
                this.get_all_reviews()
            },
            all_reviews(): void {
                this.scrollReviewsIntoView()
                if (!this.seen_review && window.location.href.includes('add-review')) {
                    // Take user to add review straight away
                    this.add_review()
                    this.seen_review = true
                } else if (!this.seen_review && window.location.href.includes('review')) {
                    nextTick(() => {
                        // Take user to view a review they've written straight away
                        const window_location: string[] = window.location.href.split('/')
                        const id: string = window_location[window_location.length-1]
                        const review: HTMLDivElement = document.querySelector(`[name='${id}']`) as HTMLDivElement
                        if (review) {
                            review.scrollIntoView()
                            this.seen_review = true
                        } 
                    })
                    
                }
            },
            filter_zero(): void {
                // Updating reviews shown as filter is toggled
                this.get_all_reviews()
                this.scrollReviewsIntoView()
                this.check_all_stars()
            },
            filter_one(): void {
                // Updating reviews shown as filter is toggled
                this.get_all_reviews()
                this.scrollReviewsIntoView()
                this.check_all_stars()
            },
            filter_two(): void {
                // Updating reviews shown as filter is toggled
                this.get_all_reviews()
                this.scrollReviewsIntoView()
                this.check_all_stars()
            },
            filter_three(): void {
                // Updating reviews shown as filter is toggled
                this.get_all_reviews()
                this.scrollReviewsIntoView()
                this.check_all_stars()
            },
            filter_four(): void {
                // Updating reviews shown as filter is toggled
                this.get_all_reviews()
                this.check_all_stars()
                this.scrollReviewsIntoView()
            },
            filter_five(): void {
                // Updating reviews shown as filter is toggled
                this.get_all_reviews()
                this.check_all_stars()
                this.scrollReviewsIntoView()
            },
            filter_images(): void {
                // Updating reviews shown as filter is toggled
                this.get_all_reviews()
                this.check_all_media()
                this.scrollReviewsIntoView()
            },
            filter_video(): void {
                // Updating reviews shown as filter is toggled
                this.check_all_media()
                this.get_all_reviews()
                this.scrollReviewsIntoView()
            },
            my_reviews(): void {
                // Updating reviews shown as filter is toggled
                this.check_all_reviews()
                this.get_all_reviews()
                this.scrollReviewsIntoView()
            },
            me_reviews(): void {
                // Updating reviews shown as filter is toggled
                this.check_all_reviews()
                this.get_all_reviews()
                this.scrollReviewsIntoView()
            },
            no_reviews(): void {
                // Updating reviews shown as filter is toggled
                this.check_all_media()
                this.get_all_reviews()
                this.scrollReviewsIntoView()
            }
        },
        mounted(): void {
            this.fill_stars()
            this.get_all_reviews()
            this.buying_now = false
        },
    })
</script>

<style scoped>
    #resource-view {
        display: grid;
        grid-template-columns: 1.5fr 2fr 0.5fr 0.5fr;
        grid-template-areas: "header header header header"
                             "resource resource-description view-sellers resource-cart"
                             "resource-details resource-details resource-details resource-details"
                             "stars stars stars stars"
                             "my-review my-review my-review my-review"
                             "reviews reviews reviews reviews"
                             ;
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        gap: 3rem;
        height: 90.9vh;
        overflow-y: auto;
        padding-right: 1rem;
        position: relative;
    }

    #dark #resource-view {
        color: white;
    }

    #reviews {
        grid-area: reviews;
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    #header {
        grid-area: header;
    }

    #header p {
        font-size: 1.5rem;
        margin-bottom: 0.6rem;
    }

    #resource {
        grid-area: resource;
        display: flex;
        gap: 2rem;
        align-items: center;
    }

    #resource-price-and-rating div {
        font-size: 1.2rem;
    }
    
    #resource-price-and-rating {
        display: flex;
        gap: 0.5rem;
        flex-direction: column;
        font-size: 1.2rem;
    }

    #rating, #my-rating {
        display: flex;
        gap: 0.2rem;
        align-items: center;
    }

    #rating p {
        font-size: 1.2rem;
        margin-left: 0.3rem;
    }

    #rating:hover {
        text-decoration: underline;
        cursor: pointer;
    }

    #add-review {
        color: #789ECA;
    }

    #dark #add-review {
        color: rgb(206, 206, 206);
    }

    #est-del, #add-review {
        font-size: 1rem !important;
    }

    #est-del {
        color: rgb(40, 39, 39);
    }
    
    #dark #est-del {
        color: rgb(233, 233, 233);
    }

    #add-review, #save-review {
        font-size: 1rem !important;
    }

    #add-review:hover {
        text-decoration: underline;
        cursor: pointer;
    }

    #resource img {
        height: 200px;
        width: 200px;
        object-fit: contain;
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        padding : 0.5rem;
    }

    #resource-description {
        grid-area: resource-description;
        display: flex;
        flex-direction: column;
        gap: 0.7rem;
    }

    #desc {
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        border: 0.3rem solid #D9D9D9;
        padding: 0.4rem;
        height: 10rem;
        overflow-y: auto;
    }

    #dark #desc, #dark #resource-cart div {
        color: black;
    }

    #dark #total {
        color: white !important;
    }

    #resource-cart {
        grid-area: resource-cart;
        display: flex;
        flex-direction: column;
        justify-content: center;
        justify-self: center;
        gap: 1.4rem;
    }

    #resource-cart div {
        background-color: #0DCAF0;
        border-radius: 0.5rem;
        padding: 0.5rem;
        width: 7rem;
        text-align: center;
    }

    #resource-cart div:hover, #view-sellers p:hover, #my-review #add-review:hover, #save-review:hover:hover {
        background-color: #177183;
        cursor: pointer;
    }

    #dark #resource-cart div, #dark #view-sellers p {
        background-color: white;
    }

    #dark #resource-cart div:hover, #dark #view-sellers p:hover {
        background-color: darkgray;
    }

    #view-sellers {
        align-self: center;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        justify-self: center !important;
    }

    #view-sellers p {
        grid-area: view-sellers;
        background-color: #0DCAF0;
        border-radius: 0.5rem;
        padding: 0.5rem;
        width: 7rem;
        text-align: center;
        justify-self: center;
    }

    #resource-details {
        grid-area: resource-details;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    #details {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .detail {
        display: flex;
        align-items: center;
    }

    .detail label{
        width: 6rem;
    }

    .detail .data {
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
        display: flex;
        gap: 0.4rem;
        width: 5rem;
        justify-content: center;
    }

    #stars {
        grid-area: stars;
    }

    #my-review {
        grid-area: my-review;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .item {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .item textarea {
        background-color: #D9D9D9;
        height: 10rem;
        overflow-y: auto;
    }

    .item input, .item textarea {
        width: 98% !important;
        border-radius: 0.5rem;
        padding: 0.5rem !important;
    }

    #my-review #add-review, #save-review, #delete-review {
        border: none;
        background-color: #0DCAF0;
        color: black;
        border-radius: 0.5rem;
        padding: 0.5rem;
        width: 11rem;
    }

    #save-review, #delete-review {
        width: 9rem;
    }

    #dark #my-review #add-review, #dark #save-review {
        background-color: white;
    }

    #dark #my-review #add-review:hover, #dark #save-review:hover {
        cursor: pointer;
        background-color: darkgray;
    }

    #my-review #add-review:hover {
        text-decoration: none !important;
    }

    #rating-one:hover, #rating-two:hover, #rating-three:hover, #rating-four:hover, #rating-five:hover {
        cursor: pointer;
    }

    #my-rating span {
        margin-left: 0.5rem;
    }

    #my-review select, #reviews select {
        border-radius: 0.5rem;
        padding: 0.5rem;
        background-color: #D9D9D9;
    }

    #rating-error {
        color: red;
    }

    #delete-review {
        background-color: red;
        color: white;
    }

    #delete-review:hover {
        background-color: rgb(94, 16, 16);
        cursor: pointer;
    }

    #buttons {
        display: flex;
        gap: 1rem;
    }

    #media {
        display: flex;
        gap: 2rem;
    }

    #image1, #img, #vid, #vid1, #video1 { 
        display: none;
    }

    #image, #video {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        align-items: center;
    }

    .media-square {
        height: 10rem;
        width: 10rem;
        border-radius: 1rem;
        background-color: #D9D9D9 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        background: none;
        border: none;
        cursor: pointer;
    }

    .media-square i {
        font-size: 2rem;
    }

    .media-square:hover {
        color: #0DCAF0;
        background-color: #0DCAF0;
    }

    #img, #vid, #vid1 {
        max-height: 100%;
        max-width: 100%;
    }

    .media-square .delete {
        background: transparent;
        color: red;
        border: none;
        position: absolute;
        top: 0.2rem;
        right: 0.3rem;
    }

    .media-square .delete {
        font-size: 1.3rem !important;
    }

    .media-square button {
        border: none;
    }

    .delete:hover {
        cursor: pointer;
    }

    .reviews-review {
        display: flex;
        flex-direction: column;
    }

    .review-heading {
        display: flex;
        gap: 3rem;
        align-items: center;
    }

    .review-image, .review-video {
        height: 6rem;
        width: 6rem;
        object-fit: contain;
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    .review-image:hover, .review-video:hover {
        background-color: darkgray;
        cursor: pointer;
    }

    #review-heading-one .icon {
        font-size: 3rem;
    }

    #review-heading-one {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .review-heading-one-height {
        height: 8rem;
    }

    .review-heading-one-reviewing-height {
        height: 5rem;
    }

    .title-area {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .title-area p {
        font-weight: bold;
    }

    .title-area .date {
        font-size: 0.8rem;
        font-weight: normal !important;
        color: rgb(154, 154, 154);
    }

    #dark .title-area .date {
        color: white;
    }

    .review-review {
        background-color: #D9D9D9;
        padding: 0.5rem;
        border-radius: 0.5rem;
        height: 6rem;
        overflow-y: auto;
    }

    .review-rating {
        display: flex;
        gap: 0.2rem;
    }

    .review-media {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    #edit-review {
        margin-top: 1rem;
        display: flex;
        gap: 1rem;
    }

    .edit, .trash, .save, .rewind {
        border: none;
        border-radius: 0.5rem;
        padding: 0.2rem;
    }

    .edit i, .trash i, .save i, .rewind i {
        font-size: 1.5rem;
    }

    .edit:hover, .trash:hover, .save:hover, .rewind:hover {
        cursor: pointer;
    }

    .edit, .rewind {
        background-color: #0DCAF0;
        color: white;
    }

    .edit:hover, .rewind:hover {
        background-color: #177183;
    }

    .rewind {
        padding-left: 0.3rem;
        padding-right: 0.3rem;
    }

    #dark .rewind, #dark .edit {
        background-color: white;
        color: black;
    }

    #dark .rewind:hover, #dark .edit:hover {
        background-color: darkgray;
    }

    #dark .edit {
        background-color: white;
    }

    .save {
        background-color: green;
        color: white;
        padding: 0.4rem;
    }

    .save:hover {
        background-color: rgb(123, 207, 132);
    }

    .edit:hover {
        background-color: #177183;
    }

    #dark .edit:hover {
        background-color: darkgray;
    }

    .trash {
        background-color: red;
        color: white;
    }

    .trash:hover {
        background-color: rgb(113, 22, 22);
    }

    #reviews #media {
        margin-top: 1rem;
    }

    textarea {
        resize: none;
    }

    .review-review-desc {
        height: 10rem;
    }

    .top-marg {
        margin-top: 1.3rem;
    }

    .text-desc {
        margin-bottom: 0.5rem;
    }

    #reviews-p {
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }

    #stars-span {
        margin-left: 0.4rem;
    }

    #filtering {
        display: flex;
        justify-content: space-between;
    }

    #sorting {
        display: flex;
        margin-left: auto;
    }

    .filtering {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }

    #no-reviews-to-display {
        align-self: center;
    }

    #toggle-filter {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background-color: white;
        border-radius: 0.4rem;
        padding: 0.5rem;
        cursor: pointer;
        width: 6.4rem;
        justify-content: center;
        height: 1.3rem;
        border: 0.1rem solid #7f7f7f;
    }

    #toggle-filter:hover {
        background-color: darkgray;
    }

    #filtering-section {
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
        position: relative;
    }

    #filtering select {
        background-color: white !important;
    }

    #filter-options {
        display: flex;
        flex-direction: column;
        background-color: white;
        border-radius: 0.4rem;
        position: absolute;
        top: 2.5rem;
        left: -11.8rem;
        border: 0.01rem solid #d9d9d9;
        gap: 0.5rem;
        width: 19.2rem;
        z-index: 2;
    }

    .filter-item {
        display: flex;
        flex-direction: column;
        padding: 0.5rem;
        padding-left: 0.7rem;
        padding-right: 0.7rem;
        gap: 0.5rem;
    }

    .row {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }

    .datum {
        background-color: #0DCAF0;
        border-radius: 0.5rem;
        padding: 0.5rem;
        min-width: 1rem;
        text-align: center;
    }

    .datum:hover {
        background-color: #177183;
        cursor: pointer;
    }

    .not {
        background-color: darkgray !important;
    }

    #dark .datum {
        background-color: black;
        color: white;
    }

    #dark .datum:hover {
        background-color: darkgray;
    }

    .border-top {
        border-top-right-radius: 0.4rem;
        border-top-left-radius: 0.4rem;
    }

    .border-bottom {
        border-bottom-right-radius: 0.4rem;
        border-bottom-left-radius: 0.4rem;
    }

    #filter-right {
        display: flex;
        gap: 2rem;
    }

    textarea:disabled {
        color: black;
    }

    #cart-total-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        background: transparent !important;
    }
    
    #cart {
        display: flex;
        background-color: #D9D9D9 !important;
        padding-left: 0.4rem !important;
        padding-right: 0.4rem !important;
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important; 
    }

    #cart-total {
        margin: auto;
        width: 100%;
    }

    #cart-toggle {
        display: flex;
        padding: 0 !important;
        justify-content: center;
        background-color: transparent !important;
    }

    button:disabled, button:disabled:hover {
        cursor: not-allowed !important;
        background-color: darkgray !important;
    }

    #cart-toggle p {
        font-size: 1.4rem !important;
    }

    #cart-toggle #plus {
        width: 50%;
        border-top-left-radius: 0.4rem;
        border-bottom-left-radius: 0.4rem;
        background-color: white !important;
        /* width: 1.5rem !important; */
    }

     #cart-toggle #minus {
        width: 50%;
        border-top-right-radius: 0.4rem;
        border-bottom-right-radius: 0.4rem;
        background-color: white !important;
    }

    #cart-toggle #plus:hover, #cart-toggle #minus:hover {
        background-color: darkgray !important;
    } 

    hr {
        border: none;
        height: 1.7rem;
        width: 0.08rem;
        background-color: black !important;
    }

    #minus i {
        color: red !important;
    }


    #total {
        background-color: transparent !important;
        padding: 0 !important;
    }

    .round-border {
        border-top-left-radius: 0.3rem;
        border-bottom-left-radius: 0.3rem;
    }

    .round-plus {
        border-top-right-radius: 0.3rem;
        border-bottom-right-radius: 0.3rem;
    }

    #minus {
        border-top-right-radius: 0.3rem;
        border-bottom-right-radius: 0.3rem;
    }

    #plus {
        border-top-left-radius: 0.3rem;
        border-bottom-left-radius: 0.3rem;
    } 

    #buynow {
        background-color: gold !important;
    }

    #buynow:hover {
        background-color: rgb(185, 160, 22) !important;
    }

    #dark #view-sellers, #dark #details .data, #dark #filtering-section {
        color: black;
    }

    #border {
        position: fixed;
        top: 0;
        right: 0;
        height: 100vh;
        width: 100vw;
        background-color: rgb(53, 53, 53, 50%);
        z-index: 3;
        justify-content: center;
        align-items: center;
        display: flex;
    }

    #border img, #border video {
        height: 20rem;
        width: 20rem;
        object-fit: contain;
        background-color: #d9d9d9;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    #border div {
        position: relative;
    }

    #x {
        color: red;
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        font-size: 1.2rem;
    }

    #x:hover {
        cursor: pointer;
        color: darkred;
    }

    .big-x {
        z-index: 2;
    }

    /* Responsive design */
    @media (max-width: 1594px) {
        #resource-view {
            grid-template-columns: 1fr 1.2fr 0.5fr;
            grid-template-areas: "header header header"
                                "resource resource-description view-sellers"
                                "resource-cart resource-cart resource-cart"
                                "resource-details resource-details resource-details"
                                "stars stars stars"
                                "my-review my-review my-review"
                                "reviews reviews reviews"
                                ;
        }

        #resource-cart {
            justify-self: start !important;
            flex-direction: row;
            align-items: center;
        }
    }

    @media (max-width: 1302px) {
        #resource-view {
            grid-template-columns: 1.5fr 0.7fr 0.7fr;
            grid-template-areas: "header header header"
                                "resource view-sellers resource-cart"
                                "resource-description resource-description resource-description"
                                "resource-details resource-details resource-details"
                                "stars stars stars"
                                "my-review my-review my-review"
                                "reviews reviews reviews"
                                ;
        }

        #resource-cart {
            justify-self: start !important;
            flex-direction: column;
        }

        .rating-text {
            display: block !important;
            white-space: nowrap;
        }
    }

    @media (max-width: 930px) {
        #resource-view {
            grid-template-columns: 1fr 1fr;
            grid-template-areas: "header header"
                                "resource view-sellers"
                                "resource-cart resource-cart"
                                "resource-description resource-description"
                                "resource-details resource-details"
                                "stars stars"
                                "my-review my-review"
                                "reviews reviews"
                                ;
        }

        #resource-cart, #view-sellers{
            justify-self: start !important;
        }

        #resource-cart {
            flex-direction: row;
        }
    }

    @media (max-width: 644px) {
        #resource-view {
            grid-template-columns: 0.5fr 1fr;
            grid-template-areas: "header header"
                                "resource resource"
                                "view-sellers resource-cart"
                                "resource-description resource-description"
                                "resource-details resource-details"
                                "stars stars"
                                "my-review my-review"
                                "reviews reviews"
                                ;
        }

        #resource-cart {
            justify-self: start !important;
        }

        #resource-cart {
            flex-direction: row;
        }
    }

    @media (max-width: 496px) {
        #resource-view {
            grid-template-columns: 1fr 1fr;
            grid-template-areas: "header header"
                                "resource resource"
                                "view-sellers resource-cart"
                                "resource-description resource-description"
                                "resource-details resource-details"
                                "stars stars"
                                "my-review my-review"
                                "reviews reviews"
                                ;
            gap: 2rem;
        }

        #resource-cart {
            justify-self: start !important;
        }

        #resource-cart {
            flex-direction: column;
        }

        #resource img {
            height: 8rem;
            width: 8rem;
        }

        #desc {
            height: 8rem;
        }

        .review-heading {
            flex-direction: column;
            gap: 0;
            align-items: flex-start;
            margin-bottom: 1.2rem;
        }

        #filter-right {
            gap: 0.2rem;
        }

        #filtering {
            flex-direction: column-reverse;
            gap: 1rem;
        }
    }
</style> 