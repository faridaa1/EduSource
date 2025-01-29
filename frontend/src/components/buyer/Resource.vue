<template>
    <div id="resource-view" v-if="resource && Object.keys(resource).length > 0">
        <div id="header">
            <p>{{ (resource as Resource).name }}</p>
        </div>
        <div id="resource">
            <img id="resource-image" :src="`http://localhost:8000/${(resource as Resource).image1}`" :alt="`${(resource as Resource).type}`">
            <div id="resource-price-and-rating">
                <div>{{ (resource as Resource).price }}</div>
                <div id="rating" v-if="total_ratings > 0">
                    <i id="one" class="bi bi-star-fill"></i>
                    <i id="two" class="bi bi-star-fill"></i>
                    <i id="three" class="bi bi-star-fill"></i>
                    <i id="four" class="bi bi-star-fill"></i>
                    <i id="five" class="bi bi-star-fill"></i>
                    <p>{{ average_rating }}</p>
                    <span v-if="total_ratings === 1">({{total_ratings}} rating)</span>
                    <span v-if="total_ratings !== 1">({{total_ratings}} ratings)</span>
            </div>
                <span v-if="total_ratings === 0">0 ratings</span>
                <div id="add-review" v-if="!written_review && total_ratings === 0" @click="add_review">Be the first to write a review</div>
                <div id="add-review" v-if="total_ratings > 0 && possible_sellers.length > 0" @click="add_review">Add Review</div>
                <div id="est-del">Estimated: {{ parseFloat((resource as Resource).estimated_delivery_time.toString()) }} {{ (resource as Resource).estimated_delivery_units }} {{ (resource as Resource).delivery_option }}</div>
            </div>
        </div>
        <div id="resource-description">
            <div>Description</div>
            <div id="desc">{{ (resource as Resource).description }}</div>
        </div>
        <div id="resource-cart">
            <div>Add to Cart</div>
            <div>Add to Wishlist</div>
        </div>
        <div id="view-sellers">
            <p @click="viewing_sellers = true">View Sellers</p>
        </div>
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
            <button id="add-review" v-if="!addingReview && possible_sellers.length > 0" @click="add_review">Click to add Review</button>
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
                <select id="seller">
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
                    <input id="image1" type="file" accept=".png" @change="show_image">
                    <label for="image1" class="media-square">
                        <i v-if="image.name === ''" class="bi bi-plus-lg"></i>
                        <img id="img" alt="image1">
                        <button v-if="!(image.name === '')" @click="remove_image"><i class="bi bi-x-lg delete"></i></button>
                    </label>
                </div>
                <div id="video">
                    <p>Video</p>
                    <input id="video1" type="file" accept=".mp4" @change="(event: Event) => show_video(event, 0)">
                    <label for="video1" class="media-square">
                        <i v-if="video.name === ''" class="bi bi-plus-lg"></i>
                        <video controls id="vid"></video>
                        <button v-if="!(video.name === '')" @click="(event: Event) => remove_video(event,0)"><i class="bi bi-x-lg delete"></i></button>
                    </label>
                </div>
            </div>
            <div id="buttons" v-if="addingReview">
                <button id="save-review" @click="save_review">Save Review</button>
                <button id="delete-review" @click="addingReview = false">Cancel</button>
            </div>
        </div>
        <div id="reviews">
            <div class="reviews-review" v-for="review in all_reviews">
                <div class="review-heading">
                    <div id="review-heading-one" class="review-heading-one-height">
                        <div v-if="!editing">
                            <i class="bi bi-person-circle icon"></i>
                        </div>
                        <div class="title-area">
                            <p v-if="editing" style="font-weight: normal;">Stars</p>
                            <div class="review-rating">
                                <i v-if="!editing" class="bi bi-star-fill" style="color: orange;"></i>
                                <i v-if="editing" class="bi bi-star-fill" id="rating-one" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="!editing && review.rating >= 2" class="bi bi-star-fill" style="color: orange;" ></i>
                                <i v-if="editing && review.rating >= 2" id="rating-two" class="bi bi-star-fill" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="!editing && review.rating < 2"class="bi bi-star-fill"></i>
                                <i v-if="editing && review.rating < 2" id="rating-two" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                                <i v-if="!editing && review.rating >= 3" class="bi bi-star-fill" style="color: orange;"></i>
                                <i v-if="editing && review.rating >= 3" id="rating-three" class="bi bi-star-fill" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="!editing && review.rating < 3" class="bi bi-star-fill"></i>
                                <i v-if="editing && review.rating < 3" id="rating-three" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                                <i v-if="!editing && review.rating >= 4" class="bi bi-star-fill" style="color: orange;"></i>
                                <i v-if="editing && review.rating >= 4" id="rating-four" class="bi bi-star-fill" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="!editing && review.rating < 4" class="bi bi-star-fill"></i>
                                <i v-if="editing && review.rating < 4" id="rating-four" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                                <i v-if="!editing && review.rating == 5" class="bi bi-star-fill" style="color: orange;"></i>
                                <i v-if="editing && review.rating == 5" id="rating-five" class="bi bi-star-fill" style="color: orange;" @mouseenter="show_potential_rating"></i>
                                <i v-if="!editing && review.rating < 5" class="bi bi-star-fill"></i>
                                <i v-if="editing && review.rating < 5" id="rating-five" class="bi bi-star-fill" @mouseenter="show_potential_rating"></i>
                                <span v-if="editing" id="stars-span">{{ parseFloat(rating.toString()) }}</span>
                            </div>
                            <p v-if="!editing" id="title">{{ review.title }} (Ordered from {{ allResources.find(resource => resource.id === review.resource)?.author }})</p>
                            <p v-if="!editing" class="date">{{ to_date(review.upload_date) }}</p>
                        </div>
                    </div>
                    <div v-if="!editing" class="review-media">
                        <img class="review-image" v-if="review.image" :src="`http://localhost:8000${review.image}`" alt="image">
                        <video class="review-video" v-if="review.video" :src="`http://localhost:8000${review.video}`" controls></video>
                    </div>
                </div>
                <div v-if="editing">
                    <div class="item">
                        <p>Title</p>
                        <input type="text" id="specific-review-title" :value="review.title" @input="reset_validity(1)">
                    </div>
                    <div class="item top-marg">
                        <p>Seller</p>
                        <select id="review-seller" :value="review.resource">
                            <option :value="resource.id" v-for="resource in possible_sellers(true)">
                                <p>{{ resource.author }}</p>
                            </option>
                        </select>
                    </div>
                </div>
                <p class="top-marg text-desc" v-if="editing">Review</p>
                <textarea :disabled="!editing" id="review-review" @input="reset_validity(1)">{{ review.review }}</textarea>
                <div id="media" v-if="editing">
                    <div id="image">
                        <p>Image</p>
                        <input id="image1" type="file" accept=".png" @change="show_image">
                        <label for="image1" class="media-square">
                            <i v-if="image.name === ''" class="bi bi-plus-lg"></i>
                            <img id="img" alt="image1" :src="`http://localhost:8000${review.image}`">
                            <button v-if="!(image.name === '')" @click="remove_image"><i class="bi bi-x-lg delete"></i></button>
                        </label>
                    </div>
                    <div id="video">
                        <p>Video</p>
                        <input id="video1" type="file" accept=".mp4" @change="(event: Event) => show_video(event,1)">
                        <label for="video1" class="media-square">
                            <i v-if="video.name === ''" class="bi bi-plus-lg"></i>
                            <video controls id="vid1" :src="`http://localhost:8000${review.video}`"></video>
                            <button v-if="!(video.name === '')" @click="(event: Event) => remove_video(event,1)"><i class="bi bi-x-lg delete"></i></button>
                        </label>
                    </div>
                </div>
                <div v-if="review.user === user.id" id="edit-review">
                    <button v-if="!editing" class="edit" @click="edit_review(review)"><i class="bi bi-pencil-fill"></i></button>
                    <button v-if="editing" class="save" @click="save_edited_review(review)"><i class="bi bi-floppy-fill"></i></button>
                    <button v-if="editing" class="rewind" @click="close_review"><i class="bi bi-arrow-counterclockwise"></i></button>
                    <button class="trash" @click="delete_review(review)"><i class="bi bi-trash3-fill"></i></button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Resource, Review, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import Stars from './Stars.vue';
    export default defineComponent({
        components: {Stars},
        data(): {
            addingReview: boolean,
            rating_error: boolean,
            viewing_sellers: boolean,
            review: number,
            editing: boolean,
            rating: number,
            image: File,
            video: File
        } { return {
            addingReview: false,
            rating: 0,
            review: -1,
            viewing_sellers: false,
            editing: false,
            rating_error: false,
            video: new File([''], ''),
            image: new File([''], ''),
        }},
        methods: {
            close_review(): void {
                document.getElementById('review-review')?.classList.remove('review-review-desc')
                document.getElementById('review-heading-one')?.classList.add('review-heading-one-height')
                document.getElementById('review-heading-one')?.classList.remove('review-heading-one-reviewing-height')
                this.editing = false
                this.review = -1
            },
            edit_review(review: Review): void {
                this.editing = true
                nextTick(() => { 
                    this.review = review.id
                    const reviews: HTMLDivElement = document.getElementById('reviews') as HTMLDivElement
                    const img: HTMLImageElement = reviews.querySelector('img') as HTMLImageElement
                    const vid: HTMLVideoElement = document.getElementById('vid1') as HTMLVideoElement
                    if (review.image) {
                        this.image = new File([], img.src)
                        img.style.display = 'block'
                    } 
                    if (review.video) {
                        this.video = new File([], vid.src)
                        vid.style.display = 'block'
                    } 
                    document.getElementById('review-review')?.classList.add('review-review-desc')
                    document.getElementById('review-heading-one')?.classList.remove('review-heading-one-height')
                    document.getElementById('review-heading-one')?.classList.add('review-heading-one-reviewing-height')
                    this.rating = review.rating
                })
            },
            async delete_review(review: Review) {
                await fetch(`http://localhost:8000/api/user/${this.user.id}/review/${review.id}/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                })
                useResourcesStore().removeReview(review)
            },
            to_date(date: string): string {
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
                this.addingReview = true
                nextTick(() => {
                    document.getElementById('stars-text')?.scrollIntoView()
                })
            },
            reset_validity(number: number): void {
                const title: HTMLInputElement = document.getElementById(number === 0 ? 'review-title' : 'specific-review-title') as HTMLInputElement
                const description: HTMLTextAreaElement = document.getElementById(number === 0 ? 'review-text' : 'review-review') as HTMLTextAreaElement
                title.setCustomValidity('')
                title.reportValidity()
                description.setCustomValidity('')
                description.reportValidity()
            },
            async save_edited_review(review: Review): Promise<void> {
                const title: HTMLInputElement = document.getElementById('specific-review-title') as HTMLInputElement
                const description: HTMLTextAreaElement = document.getElementById('review-review') as HTMLTextAreaElement

                if (!title && !description) return

                if (title.value === '') {
                    title.setCustomValidity('Cannot be empty')
                    title.reportValidity()
                    return
                } else if (!title.value.match(/^[a-zA-Z0-9]+(( [a-zA-Z0-9]+)*(: [a-zA-Z0-9]+)*(- [a-zA-Z0-9]+)*(\'[a-zA-Z0-9]+)*(, [a-zA-Z0-9]+)*(\([a-zA-Z0-9]+\))*(\[[a-zA-Z0-9]+\])*("[a-zA-Z0-9]+")*)*[\.!\?]*$/)) {
                    title.setCustomValidity('Invalid format')
                    title.reportValidity()
                    return
                }

                if (description.value === '') {
                    description.setCustomValidity('Cannot be empty')
                    description.reportValidity()
                    return
                } else if (!description.value.match(/^[a-zA-Z0-9]+(( [a-zA-Z0-9]+)*(: [a-zA-Z0-9]+)*(- [a-zA-Z0-9]+)*(\'[a-zA-Z0-9]+)*(, [a-zA-Z0-9]+)*(\([a-zA-Z0-9]+\))*(\[[a-zA-Z0-9]+\])*("[a-zA-Z0-9]+")*)*[\.!\?]*$/)) {
                    description.setCustomValidity('Invalid format')
                    description.reportValidity()
                    return
                }

                this.reset_validity(1)
                const seller_element: HTMLSelectElement = document.getElementById('review-seller') as HTMLSelectElement
                const seller = seller_element.value
                const data: FormData = new FormData()
                data.append('stars', this.rating.toString())
                data.append('title', title.value)
                data.append('description', description.value)
                data.append('image', this.image)
                data.append('video', this.video)
                let savedReview: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/edit-review/${review.id}/${seller}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: data
                })
                if(!savedReview.ok) {
                    console.error('Error editing review')
                    alert('Error saving review')
                    return
                }
                let reviewData: Review = await savedReview.json()
                useResourcesStore().editResoureReview(reviewData, review.resource)
                this.close_review()
            },
            async save_review(): Promise<void> {
                const title: HTMLInputElement = document.getElementById('review-title') as HTMLInputElement
                const description: HTMLTextAreaElement = document.getElementById('review-text') as HTMLTextAreaElement

                if (!title && !description) return

                if (title.value === '') {
                    title.setCustomValidity('Cannot be empty')
                    title.reportValidity()
                    return
                } else if (!title.value.match(/^[a-zA-Z0-9]+(( [a-zA-Z0-9]+)*(: [a-zA-Z0-9]+)*(- [a-zA-Z0-9]+)*(\'[a-zA-Z0-9]+)*(, [a-zA-Z0-9]+)*(\([a-zA-Z0-9]+\))*(\[[a-zA-Z0-9]+\])*("[a-zA-Z0-9]+")*)*[\.!\?]*$/)) {
                    title.setCustomValidity('Invalid format')
                    title.reportValidity()
                    return
                }

                if (description.value === '') {
                    description.setCustomValidity('Cannot be empty')
                    description.reportValidity()
                    return
                } else if (!description.value.match(/^[a-zA-Z0-9]+(( [a-zA-Z0-9]+)*(: [a-zA-Z0-9]+)*(- [a-zA-Z0-9]+)*(\'[a-zA-Z0-9]+)*(, [a-zA-Z0-9]+)*(\([a-zA-Z0-9]+\))*(\[[a-zA-Z0-9]+\])*("[a-zA-Z0-9]+")*)*[\.!\?]*$/)) {
                    description.setCustomValidity('Invalid format')
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
                const seller_element: HTMLSelectElement = document.getElementById('seller') as HTMLSelectElement
                const seller = seller_element.value
                const data: FormData = new FormData()
                data.append('stars', this.rating.toString())
                data.append('title', title.value)
                data.append('description', description.value)
                data.append('image', this.image)
                data.append('video', this.video)
                let savedReview: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/review/${seller}/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: data
                })
                let review: Review = await savedReview.json()
                useResourcesStore().addResoureReview(review)
                this.addingReview = false
            },
            show_potential_rating(event: Event): void {
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
            fill_stars(): void {
                const star1: HTMLElement = document.getElementById('one') as HTMLElement
                const star2: HTMLElement = document.getElementById('two') as HTMLElement
                const star3: HTMLElement = document.getElementById('three') as HTMLElement
                const star4: HTMLElement = document.getElementById('four') as HTMLElement
                const star5: HTMLElement = document.getElementById('five') as HTMLElement
                if (star1 && star2 && star3 && star4 && star5) {
                    console.log(this.average_rating)
                    star1.style.color = this.average_rating >= 1 ? 'orange' : 'none'
                    star2.style.color = this.average_rating >= 2 ? 'orange' : 'none'
                    star3.style.color = this.average_rating >= 3 ? 'orange' : 'none'
                    star4.style.color = this.average_rating >= 4 ? 'orange' : 'none'
                    star5.style.color = this.average_rating == 5 ? 'orange' : 'none'
                }
            },
            possible_sellers(editing: boolean): Resource[] {
                // filter so that user cannot review seller twice; check who theyve reviewed and remove them
                let resources = this.allResources.filter(resource =>  resource.user !== this.user.id)
                if (editing) {
                    return resources.filter(resource => resource.reviews.length === 0 || resource.reviews.some(review => this.review === review.id || review.user !== this.user.id))
                }
                return resources = resources.filter(resource => resource.reviews.length === 0 || resource.reviews.some(review => review.user !== this.user.id))
            },
        },
        computed: {
            total_ratings(): number {
                let number_of_reviews: number = 0
                this.allResources.forEach((resource) => {
                    resource.reviews.forEach((review) => {
                        number_of_reviews += 1
                })})
                this.fill_stars()
                return number_of_reviews
            },
            average_rating(): number {
                let sum_of_rating: number = 0
                this.allResources.forEach((resource) => {
                    resource.reviews.forEach((review) => {
                        sum_of_rating += review.rating
                })})
                this.fill_stars()
                if (this.total_ratings === 0) return 0
                return (sum_of_rating/this.total_ratings)
            },
            written_review(): boolean {
                return this.all_reviews.find(review => review.user === this.user.id) !== undefined
            },
            user(): User {
                return useUserStore().user
            },
            reviews(): Review[] {
                return []
            },
            all_reviews(): Review[] {
                let reviews: Review[] = []
                this.allResources.forEach((resource) =>
                    reviews.push(...resource.reviews)
                )
                return reviews
            },
            allResources(): Resource[] {
                const window_location: string[] = window.location.href.split('/')
                const name: string = window_location[window_location.length-1]
                return useResourcesStore().resources.filter(resource => resource.name === name)
            },
            resource(): Resource | {} {
                const window_location: string[] = window.location.href.split('/')
                const name: string = window_location[window_location.length-1]
                return this.allResources[0]
            },
        },
        watch: {
            async user(new_user: User): Promise<void> {
                for (const resource of this.allResources) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resource(resource: Resource): Promise<void> {
                this.fill_stars()
                resource.price = await this.listedprice(resource)
            }
        },
        mounted(): void {
            this.fill_stars()
        }
    })
</script>

<style scoped>
    #resource-view {
        display: grid;
        grid-template-columns: 2fr 2fr 1fr 1fr;
        grid-template-areas: "header header header header"
                             "resource resource-description view-sellers resource-cart"
                             "resource-details resource-details resource-details resource-details"
                             "stars stars stars stars"
                             "my-review my-review my-review my-review"
                             "reviews reviews reviews reviews"
                             ;
        margin-top: 1rem;
        margin-bottom: 1rem;
        margin-left: 1rem;
        gap: 2rem;
        max-height: 92vh;
        overflow-y: scroll;
        padding-right: 1rem;
    }

    #reviews {
        grid-area: reviews;
        display: flex;
        flex-direction: column;
        gap: 5rem;
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

    #add-review {
        color: #0DCAF0;
    }

    #est-del, #add-review {
        font-size: 1rem !important;
    }

    #est-del {
        color: rgb(40, 39, 39);
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
        max-width: 200px;
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
        padding: 0.4rem;
        height: 100%;
        overflow-y: scroll;
    }

    #resource-cart {
        grid-area: resource-cart;
        display: flex;
        flex-direction: column;
        justify-content: center;
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
        height: 5rem;
        background-color: #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
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

    #review-review {
        background-color: #D9D9D9;
        padding: 0.5rem;
        border-radius: 0.5rem;
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
        justify-content: flex-end;
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
    }

    #stars-span {
        margin-left: 0.4rem;
    }
</style>