<template>
    <div id="new-listing">
        <div id="header">
            <h1>{{ isPriorListing ? '' : 'New' }} Resource Listing</h1>
            <div id="buttons">
                <button v-if="!duplicate_resource" @click="submit(isPriorListing ? resource.is_draft : false)">{{ isPriorListing ? 'Update Details' : 'List Item' }}</button>
                <button v-if="!duplicate_resource" @click="submit(isPriorListing ? resource.is_draft ? false : true : true)">{{ resource && resource.is_draft ? 'List Item' : 'Save as Draft'}}</button>
                <button class="delete_listing" @click="delete_listing">Delete Listing</button>
            </div>
        </div>
        <div id="form" @input="clear_errors" @change="clear_errors">
            <div class="form-item" id="author">
                <label for="" id="author-container">Author <span class="required">*</span></label>
                <input type="text" v-model="author" id="author-field" :disabled="self_made">
                <div id="author-div">
                    <label for="">Resource was self-made</label>
                    <input type="checkbox" :checked="self_made" @click="self_made = !self_made">
                </div>
                <p v-if="self_made">Author will show up as your username, <span>{{ user.username }}</span></p>
            </div>
            <div class="form-item">
                <label for="">Name <span class="required">*</span></label>
                <input type="text" name="" id="name" v-model="name">
                <div id="resource_exists" v-if="exists_resource">
                    <p>A resource exists with this name, so certain details below cannot be changed.</p>
                    <p>Select 'Resource was self-made', change the resource name,  or change the resource author name to be able to edit all details.</p>
                </div>
                <div id="duplicate" v-if="duplicate_resource">
                    <p>You already sell this resource.</p>
                    <p>Select 'Resource was self-made', change the resource name, or change the author name to be able to save this item.</p>
                </div>
            </div>
            <div class="form-item">
                <label for="">Description <span class="required">*</span></label>
                <textarea name="" id="description" v-model="description" :disabled="exists_resource"></textarea>
            </div>
            <div id="dimensions" class="form-item">
                <label for="">Dimensions <span class="required">*</span></label>
                <div id="dimensions-container">
                    <div class="dimension">
                        <label for="">Height</label>
                        <div>
                            <input required type="number" min="1" max="1000.00" step="0.01" v-model="height" :disabled="exists_resource">
                            <select name="" id="height_dimension" v-model="dimension_unit" :disabled="exists_resource">
                                <option value="cm">cm</option>
                                <option value="m">m</option>
                                <option value="in">in</option>
                            </select>
                        </div>
                    </div>
                    <div class="dimension">
                        <label for="">Width</label>
                        <div>
                            <input required type="number" max="1000.00" min="1" step="0.01" v-model="width" :disabled="exists_resource">
                            <select name="" id="width_dimension" v-model="dimension_unit" :disabled="exists_resource">
                                <option value="cm">cm</option>
                                <option value="m">m</option>
                                <option value="in">in</option>
                            </select>
                        </div>
                    </div>
                    <div class="dimension">
                        <label for="">Weight</label>
                        <div>
                            <input required type="number" min="1" max="1000.00" step="0.01" v-model="weight" :disabled="exists_resource">
                            <select name="" id="weight_dimension" v-model="weight_unit" :disabled="exists_resource">
                                <option value="kg">kg</option>
                                <option value="ml">ml</option>
                                <option value="L">L</option>
                                <option value="mg">mg</option>
                                <option value="oz">oz</option>
                                <option value="lb">{{ weight > 0 && weight < 2 ? 'lb' : 'lbs' }}</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="form-item" id="type-container">
                <label for="">Type <span class="required">*</span></label>
                <select name="" id="type" v-model="type" :disabled="exists_resource">
                    <option value="Textbook">Textbook</option>
                    <option value="Notes">Notes</option>
                    <option value="Stationery">Stationery</option>
                </select>
            </div>
            <div v-if="type !== 'Stationery'" class="form-item" id="type-container">
                <label for="">Media <span class="required">*</span></label>
                <select name="" id="type" v-model="media">
                    <option value="Online">Online</option>
                    <option value="Paper">Paper</option>
                </select>
            </div>
            <div v-if="type !== 'Stationery'" class="form-item" id="pages-container">
                <label for="">Page Range <span class="required">*</span></label>
                <div>
                <input required type="number" min="1" max="9999" step="1" v-model="page_start">
                <p>to</p>
                <input required type="number" :min="page_start" max="9999" step="1" v-model="page_end">
                </div>
            </div>
            <div class="form-item" id="subject-container">
                <label for="">Subject <span class="required">*</span></label>
                <div>
                    <input id="subject" type="text" v-model="subject" :disabled="exists_resource">
                    <select v-model="subject_select" :disabled="exists_resource">
                        <option value="" selected disabled hidden>
                            Select
                        </option>
                        <option :value="subject" v-for="subject in all_subjects">
                            {{ subject }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="form-item" id="colour-container">
                <label for="">Colour <span class="required">*</span></label>
                <select name="" id="colour" v-model="colour">
                    <option value="Black">Black</option>
                    <option value="Red">Red</option>
                    <option value="Yellow">Yellow</option>
                    <option value="Pink">Pink</option>
                    <option value="Purple">Purple</option>
                    <option value="Green">Green</option>
                    <option value="Blue">Blue</option>
                    <option value="White">White</option>
                    <option value="Orange">Orange</option>
                    <option value="Brown">Brown</option>
                    <option value="Grey">Grey</option>
                </select>
            </div>
            <div v-if="self_made" class="form-item" id="sources-container">
                <label for="">Assisted Sources <span class="required">*</span></label>
                <select name="" id="sources-field" v-model="source">
                    <option value="AI">AI</option>
                    <option value="Internet">Internet</option>
                    <option value="None">None</option>
                </select>
            </div>
            <div class="form-item" id="condition-container">
                <label for="">Condition <span class="required">*</span></label>
                <select name="" id="condition-field" v-model="condition">
                    <option value="New">New</option>
                    <option value="Used">Used</option>
                </select>
            </div>
            <div class="form-item" id="price-container">
                <label for="">Price <span class="required">*</span></label>
                <div id="price-flex">
                    <input required type="number" max="9999.00" min="0" step="0.01" v-model="price">
                    <select name="" id="price-field" v-model="currency">
                        <option value="GBP">GBP</option>
                        <option value="USD">USD</option>
                        <option value="EUR">EUR</option>
                    </select>
                </div>
            </div>
            <div class="form-item" id="price-container">
                <label for="">Stock <span class="required">*</span></label>
                <input id="price-field" required type="number" max="9999.00" v-model="stock" step="1" min="0">
            </div>
            <div class="form-item" id="delivery-container">
                <label for="">Delivey Options <span class="required">*</span></label>
                <div id="options">
                    <div>
                        <label for="">Delivery</label>
                        <input type="checkbox" v-model="allow_delivery">
                    </div>
                    <div>
                        <label for="">Collection</label>
                        <input type="checkbox" v-model="allow_collection">
                    </div>
                    <div>
                        <label for="">Allow Returns</label>
                        <input type="checkbox" v-model="allow_return">
                    </div>
                </div>
            </div>
            <div class="form-item" id="price-container">
                <label for="">Estimated Delivery Time <span class="required">*</span></label>
                <div id="price-flex">
                    <input required type="number" max="9999.00" min="1" step="1" v-model="estimated_delivery_number">
                    <select name="" id="estimated-delivery-field" v-model="estimated_delivery_units">
                        <option value="minute">{{ estimated_delivery_number === 1.00 ? 'minute' : 'minutes' }}</option>
                        <option value="hour">{{ estimated_delivery_number === 1.00 ? 'hour' : 'hours' }}</option>
                        <option value="day">{{ estimated_delivery_number === 1.00 ? 'day' : 'days' }}</option>
                        <option value="week">{{ estimated_delivery_number === 1.00 ? 'week' : 'weeks' }}</option>
                        <option value="month">{{ estimated_delivery_number === 1.00 ? 'month' : 'months' }}</option>
                    </select>
                </div>
            </div>
            <div class="form-item" id="image-container">
                <label for="">Images (.png) <span class="required">*</span></label>
                <p id="images-label" v-if="image_error">{{ image_error }}</p>
                <div id="images">
                    <div class="image_input" id="image">
                        <input id="image1" type="file" accept=".png" @change="(event) => show_image(event, 1)">
                        <label for="image1" class="input-square">
                            <i v-if="image1.name === ''" class="bi bi-plus-lg"></i>
                            <img id="img1" alt="image1">
                            <button v-if="!(image1.name === '')" @click="(event) => remove_image(event, 1)"><i class="bi bi-x-lg"></i></button>
                        </label>
                    </div>
                    <div class="image_input" id="image_2">
                        <input id="image2" type="file" accept=".png" @change="(event) => show_image(event, 2)">
                        <label for="image2" class="input-square">
                            <i v-if="image2.name === ''" class="bi bi-plus-lg"></i>
                            <img id="img2" alt="image2">
                            <button v-if="!(image2.name === '')" @click="(event) => remove_image(event, 2)"><i class="bi bi-x-lg"></i></button>
                        </label>
                    </div>
                </div>
            </div>
            <div class="form-item" id="video-container">
                <label for="">Videos (.mp4) <span class="required">*</span></label>
                <p id="videos-label" v-if="video_error">{{ video_error }}</p>
                <div class="video_input" id="video_1">
                    <input id="video1" type="file" accept=".mp4" @change="show_video">
                    <label for="video1" class="video-square">
                        <i v-if="video1.name === ''" class="bi bi-plus-lg"></i>
                        <video controls id="vid1"></video>
                        <button v-if="!(video1.name === '')" @click="remove_video"><i class="bi bi-x-lg"></i></button>
                    </label>
                </div>
            </div>
        </div>
        <div id="buttons1">
                <button v-if="!duplicate_resource" @click="submit(isPriorListing ? resource.is_draft : false)">{{ isPriorListing ? 'Update Details' : 'List Item' }}</button>
                <button v-if="!duplicate_resource" @click="submit(isPriorListing ? resource.is_draft ? false : true : true)">{{ resource && resource.is_draft ? 'List Item' : 'Save as Draft'}}</button>
                <button class="delete_listing" @click="delete_listing">Delete Listing</button>
            </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { CartResource, Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            isPriorListing: boolean,
            name: string,
            description: string,
            height: number,
            width: number,
            weight: number,
            subject_select: string
            weight_unit: string,
            dimension_unit: string,
            type: 'Textbook' | 'Notes' | 'Stationery'
            subject: string
            colour: 'Black' | 'Red' | 'Yellow' | 'Pink'
                    | 'Purple' | 'Green' | 'Blue' | 'White'
                    | 'Orange' | 'Brown' | 'Grey'
            author: string,
            condition: 'New' | 'Used',
            source: 'AI' | 'Internet' | 'None',
            price: number,
            self_made: boolean,
            currency: 'GBP' | 'EUR' | 'USD',
            image1: File,
            image2: File,
            allow_delivery: boolean,
            allow_collection: boolean,
            allow_return: boolean,
            video1: File,
            estimated_delivery_number: number,
            estimated_delivery_units: 'day' | 'minute' | 'hour' | 'month' | 'week',
            stock: number,
            is_draft: boolean,
            image_error: string,
            video_error: string,
            media: 'Online' | 'Paper',
            page_start: number,
            page_end: number,
            image1Changed: boolean,
            image2Changed: boolean,
            videoChanged: boolean,
            duplicate_resource: boolean,
            existing_resource: Resource,
            exists_resource: boolean,
        } { return {
            isPriorListing: false,
            duplicate_resource: false,
            exists_resource: false,
            existing_resource: {} as Resource,
            name: '',
            description: '',
            allow_delivery: false,
            allow_collection: false,
            allow_return: false,
            height: 1,
            width: 1,
            weight: 1,
            weight_unit: 'lb',
            dimension_unit: 'cm',
            type: 'Textbook',
            subject: '',
            colour: 'Black',
            subject_select: '',
            author: '',
            condition: 'Used',
            source: 'None',
            price: 0,
            self_made: false,
            currency: useUserStore().user.currency,
            image1: new File([''], ''),
            image2: new File([''], ''),
            video1: new File([''], ''),
            estimated_delivery_number: 1.00,
            estimated_delivery_units: 'day',
            stock: 0,
            is_draft: true,
            image_error: '',
            video_error: '',
            media: 'Paper',
            page_start: 1,
            page_end: 1,
            image1Changed: false,
            image2Changed: false,
            videoChanged: false,
        }},
        methods: {
            async delete_listing(): Promise<void> {
                if (confirm('Are you sure you want to delete this listing? This action cannot be undone.')) {
                    let deleteListingResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/new-listing/`, {
                        method: 'DELETE',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf
                        },
                        body: JSON.stringify(this.resource.id)
                    })
                    if (!deleteListingResponse.ok) {
                        console.error('Failed to delete listing')
                        alert('Failed to delete listing')
                        return
                    }
                    useResourcesStore().removeResource(this.resource.id)
                    useUserStore().removeResource(this.resource.id)
                    useUsersStore().updateUser(this.user)
                    window.location.href = '/listings'
                }
            },
            clear_errors(): void {
                const form: HTMLDivElement = document.getElementById('new-listing') as HTMLDivElement
                const inputs = form.querySelectorAll('input, textarea, select')
                inputs.forEach(input => {
                    const element = input as HTMLInputElement | HTMLTextAreaElement
                    element.setCustomValidity('')
                })
                this.image_error = ''
                this.video_error = ''
            },
            submit(is_draft: boolean) {
                this.clear_errors()
                // name valiadtion
                const nameInputField: HTMLInputElement = document.getElementById('name') as HTMLInputElement
                if (this.name.length === 0) {
                    nameInputField.setCustomValidity('Cannot be empty')
                    nameInputField.reportValidity()
                    return
                } else if (this.name.length > 151) {
                    nameInputField.setCustomValidity('Name must be less than 150 characters')
                    nameInputField.reportValidity()
                    return
                } else if (!this.name.match(/^[a-zA-Z0-9]+(( [a-zA-Z0-9]+)*(: [a-zA-Z0-9]+)*(- [a-zA-Z0-9]+)*('[a-zA-Z0-9]+)*(, [a-zA-Z0-9]+)*(\([a-zA-Z0-9]+\))*(\[[a-zA-Z0-9]+\])*("[a-zA-Z0-9]+")*)*$/)) {
                    nameInputField.setCustomValidity('Incorrect format')
                    nameInputField.reportValidity()
                    return
                }
                
                // description validation
                const descriptionInputField: HTMLInputElement = document.getElementById('description') as HTMLInputElement
                if (this.description.length === 0) {
                    descriptionInputField.setCustomValidity('Cannot be empty')
                    descriptionInputField.reportValidity()
                    return
                } else if (!this.description.match(/^[a-zA-Z0-9]+(( [a-zA-Z0-9]+)*(: [a-zA-Z0-9]+)*(- [a-zA-Z0-9]+)*('[a-zA-Z0-9]+)*(, [a-zA-Z0-9]+)*(\([a-zA-Z0-9]+\))*(\[[a-zA-Z0-9]+\])*("[a-zA-Z0-9]+")*)*$/)) {
                    descriptionInputField.setCustomValidity('Incorrect format')
                    descriptionInputField.reportValidity()
                    return
                }

                // subject validation
                const subjectInputField: HTMLInputElement = document.getElementById('subject') as HTMLInputElement
                if (this.subject.length === 0) {
                    subjectInputField.setCustomValidity('Cannot be empty')
                    subjectInputField.reportValidity()
                    return
                } else if (this.subject.length > 151) {
                    subjectInputField.setCustomValidity('Subject must be less than 150 characters')
                    subjectInputField.reportValidity()
                    return
                } else if (!this.subject.match(/^[a-zA-Z]+( [a-zA-Z]+)*$/)) {
                    if (!this.subject.match(/^\S/)) {
                        subjectInputField.setCustomValidity('Cannot start with space')
                    } else if (!this.subject.match(/\S$/)) {
                        subjectInputField.setCustomValidity('Cannot end in space')
                    } else if (this.subject.match(/\s\s/)) {
                        subjectInputField.setCustomValidity('Only one space between words')
                    } else {
                        subjectInputField.setCustomValidity('Only enter letters')
                    }
                    subjectInputField.reportValidity()
                    return
                }

                // author validation
                const authorInputField: HTMLInputElement = document.getElementById('author-field') as HTMLInputElement
                if (this.self_made) {
                } else if (this.author.length === 0) {
                    authorInputField.setCustomValidity('Cannot be empty')
                    authorInputField.reportValidity()
                    return
                } else if (this.author.length > 151) {
                    authorInputField.setCustomValidity('Name must be less than 150 characters')
                    authorInputField.reportValidity()
                    return
                } else if ((!(this.author === this.user.username)) && !this.author.match(/^[a-zA-Z]+( [a-zA-Z]+)*$/)) {
                    if (!this.author.match(/^\S/)) {
                        authorInputField.setCustomValidity('Cannot start with space')
                    } else if (!this.author.match(/\S$/)) {
                        authorInputField.setCustomValidity('Cannot end in space')
                    } else if (this.author.match(/\s\s/)) {
                        authorInputField.setCustomValidity('Only one space between words')
                    } else {
                        authorInputField.setCustomValidity('Only enter letters')
                    }
                    authorInputField.reportValidity()
                    return
                }

                // ensuring images are uploaded
                if (this.image1.name === '' && this.image2.name === '') {
                    this.image_error = 'Upload 2 supporting images'
                    nextTick(() => {
                        const imageInputField: HTMLInputElement = document.getElementById('images-label') as HTMLInputElement
                        imageInputField.scrollIntoView()
                    })
                } else if ((this.image1.name === '' || this.image2.name === '')) {
                    this.image_error = 'Upload 1 supporting image'
                    const imageInputField: HTMLInputElement = document.getElementById('images-label') as HTMLInputElement
                    imageInputField.scrollIntoView()
                }

                // ensuring video is uploaded
                if (this.video1.name === '') {
                    this.video_error = 'Upload 1 supporting video'
                    nextTick(() => {
                        const videoInputField: HTMLInputElement = document.getElementById('videos-label') as HTMLInputElement
                        videoInputField.scrollIntoView()
                    })
                    return
                } 

                // built in validation
                const form: HTMLDivElement = document.getElementById('new-listing') as HTMLDivElement
                const inputs = form.querySelectorAll('input, textarea, select')
                inputs.forEach(input => {
                    const element = input as HTMLInputElement | HTMLTextAreaElement
                    element.setCustomValidity('')
                    if (element.reportValidity()) {
                        element.reportValidity()
                        return
                    }
                })
                this.post_listing(is_draft)
            },
            async post_listing(is_draft: boolean): Promise<void> {
                const data: FormData = new FormData()
                if (this.isPriorListing) {
                    data.append('id', this.resource.id.toString())
                }
                data.append('name', this.name)
                data.append('description', this.description)
                data.append('height', this.height.toString())
                data.append('height_unit', this.dimension_unit)
                data.append('width', this.width.toString())
                data.append('width_unit', this.dimension_unit)
                data.append('weight', this.weight.toString())
                data.append('weight_unit', this.weight_unit)
                data.append('type', this.type)
                data.append('media', this.media)
                data.append('page_start', this.page_start.toString())
                data.append('page_end', this.page_end.toString())
                data.append('subject', this.subject)
                data.append('colour', this.colour)
                data.append('author', this.self_made ? this.user.username : this.author)
                data.append('self_made', this.self_made.toString())
                data.append('price', this.price.toString())
                data.append('price_currency', this.currency)
                data.append('stock', this.stock.toString())
                data.append('estimated_number', this.estimated_delivery_number.toString())
                data.append('estimated_units', this.estimated_delivery_units)
                data.append('allow_delivery', this.allow_delivery.toString())
                data.append('allow_return', this.allow_return.toString())
                data.append('allow_collection', this.allow_collection.toString())
                if (this.isPriorListing) {
                    if (this.image1Changed) data.append('image1', this.image1)
                    if (this.image2Changed) data.append('image2', this.image2)
                    if (this.videoChanged) data.append('video', this.video1)
                } else {
                    data.append('image1', this.image1)
                    data.append('image2', this.image2)
                    data.append('video', this.video1)
                }
                data.append('is_draft', is_draft.toString())
                data.append('source', this.source)
                data.append('condition', this.condition)
                data.append('unique', (!this.exists_resource).toString())
                let postListingResponse: Response
                if (!this.isPriorListing) {
                    postListingResponse = await fetch(`http://localhost:8000/api/user/${this.user.id}/new-listing/`, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf
                        },
                        body: data
                    }) 
                } else {
                    postListingResponse = await fetch(`http://localhost:8000/api/user/${this.user.id}/new-listing/`, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken' : useUserStore().csrf
                        },
                        body: data
                    })
                }
                if (!postListingResponse.ok) {
                    console.error(is_draft ? 'Error saving listing as draft' : 'Error posting listing')
                    return
                }
                const postListingData: Resource = await postListingResponse.json()
                if (this.isPriorListing) {
                    useUserStore().updateListing(postListingData)
                    useResourcesStore().updateResource(postListingData)
                } else {
                    useUserStore().addListing(postListingData)
                }
                useUsersStore().updateUser(this.user)
                window.location.href = '/listings'
            },
            remove_video(event:Event): void {
                event.preventDefault()
                const vid: HTMLImageElement = document.getElementById('vid1') as HTMLImageElement
                const video: HTMLInputElement = document.getElementById('video1') as HTMLInputElement
                if (vid && video) {
                    vid.src = ''
                    this.video1 = new File([''], '')
                    vid.style.display = 'none'
                    video.value = ''
                }
            },
            show_video(event: Event): void {
                const inputElement: HTMLInputElement = event.target as HTMLInputElement
                if (!inputElement.files) return
                const video: File = inputElement.files[0]
                if (!video) return
                const vid: HTMLImageElement = document.getElementById('vid1') as HTMLImageElement
                if (!vid) return
                vid.src = URL.createObjectURL(video)
                vid.style.display = 'block'
                this.video1 = video
                this.videoChanged = true
            },
            remove_image(event: Event, image_number: number): void {
                event.preventDefault()
                const img: HTMLImageElement = document.getElementById(image_number === 1 ? 'img1' : 'img2') as HTMLImageElement
                const image: HTMLInputElement = document.getElementById(image_number === 1 ? 'image1' : 'image2') as HTMLInputElement
                if (img && image) {
                    img.src = ''
                    if (image_number === 1) {
                        this.image1 = new File([''], '')
                    } else {
                        this.image2 = new File([''], '')
                    }
                    img.style.display = 'none'
                    image.value = ''
                }
            },
            show_image(event: Event, image_number: number): void {
                const inputElement: HTMLInputElement = event.target as HTMLInputElement
                if (!inputElement.files) return
                const image: File = inputElement.files[0]
                if (!image) return
                const img: HTMLImageElement = document.getElementById(image_number === 1 ? 'img1' : 'img2') as HTMLImageElement
                if (!img) return
                img.src = URL.createObjectURL(image)
                img.style.display = 'block'
                if (image_number === 1) {
                    this.image1 = image
                    this.image1Changed = true
                } else {
                    this.image2 = image
                    this.image2Changed = true
                }
            },
            new_listing():void {
                window.location.href = '/new-listing'
            },
            duplicated_resource(compared_resource: Resource): boolean {
                // if it is a shared resource user cannot duplicate it unless they change the author
                const potential_duplicates: Resource | undefined = this.resources.find(resource => resource.user === this.user.id && !resource.unique && resource.name === compared_resource.name && resource.author === this.author)
                return potential_duplicates === undefined ? false : true
            },
            duplicate_resource_checks(): void {
                for (let resource of this.resources) {
                    if ((this.name !== resource.name) || resource.unique) continue
                    if (this.duplicated_resource(resource)) {
                        this.duplicate_resource = true
                        return
                    } 
                    if (resource.user !== this.user.id && this.author === resource.author) {
                        this.exists_resource = true
                        this.existing_resource = resource
                        return
                    }
                }
                this.existing_resource = {} as Resource
                this.duplicate_resource = false
                this.exists_resource = false
            }
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
            resource(): Resource {
                const emptyResource: Resource = {} as Resource
                const url: string | undefined = window.location.href
                if (url === undefined) return emptyResource
                const urlArray: string | undefined = url.split('/').pop()
                if (urlArray === undefined) return emptyResource
                const resourceId: number = parseInt(urlArray) as number

                let resource: Resource = useUserStore().user.listings?.find(listing => listing.id === resourceId) as Resource
                return resource
            },
            resources(): Resource[] {
                return useResourcesStore().resources
            },
            all_subjects(): string[] {
                let subjects = [] as string[]
                for (let resource of this.resources) {
                    if (!subjects.includes(resource.subject)) {
                        subjects.push(resource.subject)
                    }
                }
                return subjects
            },
        },
        watch: {
            user(new_user: User): void {
                this.currency = new_user.currency
            },
            resource(new_resource: Resource): void{
                this.currency = this.user.currency
                this.name = new_resource.name
                this.description = new_resource.description
                this.height = new_resource.height
                this.dimension_unit = new_resource.height_unit
                this.width = new_resource.width
                this.weight = new_resource.weight
                this.weight_unit = new_resource.weight_unit
                this.type = new_resource.type
                this.media = new_resource.media
                this.page_start = new_resource.page_start
                this.page_end = new_resource.page_end
                this.subject = new_resource.subject
                this.colour = new_resource.colour
                this.author = new_resource.author
                this.self_made = new_resource.self_made
                this.source = new_resource.source
                this.condition = new_resource.condition
                this.price = new_resource.price
                this.currency = new_resource.price_currency
                this.stock = new_resource.stock
                this.is_draft = new_resource.is_draft
                this.allow_delivery = new_resource.allow_delivery
                this.allow_collection = new_resource.allow_collection
                this.allow_return = new_resource.allow_return
                this.estimated_delivery_number = parseFloat(new_resource.estimated_delivery_time.toString())
                this.estimated_delivery_units = new_resource.estimated_delivery_units
                const image1: HTMLImageElement = document.getElementById('img1') as HTMLImageElement
                image1.src = `http://localhost:8000${new_resource.image1}`
                image1.style.display = 'block'
                this.image1 = new File([], image1.src)
                const image2: HTMLImageElement = document.getElementById('img2') as HTMLImageElement
                image2.src = `http://localhost:8000${new_resource.image2}`
                this.image2 = new File([], image2.src)
                image2.style.display = 'block'
                const vid: HTMLImageElement = document.getElementById('vid1') as HTMLImageElement
                vid.src = `http://localhost:8000${new_resource.video}`
                vid.style.display = 'block'
                this.video1 = new File([], vid.src)
            },
            subject(new_subject: string): void {
                if (this.resources.map(resource => resource.subject).includes(new_subject)) {
                    this.subject_select = new_subject
                } else {
                    this.subject_select = ''
                }
            },
            subject_select(new_subject: string): void {
                if (new_subject !== '') {
                    this.subject = new_subject
                }
            },
            name(new_name: string): void {
                if (this.self_made) return
                this.duplicate_resource_checks()
            },
            self_made(new_self_made: boolean): void {
                if (new_self_made) {
                    this.author = this.user.username
                    this.existing_resource = {} as Resource
                    this.exists_resource = false
                    this.duplicate_resource = false
                    return
                }
                this.duplicate_resource_checks()
            },
            author(new_author: string): void {
                if (new_author !== this.user.username) {
                    this.self_made = false
                } 
                this.duplicate_resource_checks()
            },
            existing_resource(new_existing_resource: Resource): void {
                if (Object.keys(this.existing_resource).length > 0) {
                    this.author = new_existing_resource.author
                    this.description = new_existing_resource.description
                    this.height = new_existing_resource.height
                    this.dimension_unit = new_existing_resource.height_unit
                    this.width = new_existing_resource.width
                    this.weight = new_existing_resource.weight
                    this.weight_unit = new_existing_resource.weight_unit
                    this.subject = new_existing_resource.subject
                    this.colour = new_existing_resource.colour
                }
            }
        },
        mounted(): void {
            this.currency = this.user.currency
            if (window.location.href.includes('notes')) {
                this.type = 'Notes'
            } else if (window.location.href.includes('stationery')) {
                this.type = 'Stationery'
            } else if (window.location.href.includes('resource')) {
                this.isPriorListing = true
            }
        }
    })
</script>
<style scoped>
    #new-listing {
        height: 58.5rem;
        overflow-y: auto;
        padding-right: 10rem;
        padding-left: 3rem;
        margin-top: 2rem;
        padding-bottom: 3rem !important;
    }

    h1 {
        font-size: 1.4rem;
    }

    #form {
        display: flex;
        flex-direction: column;
        gap: 3rem;
    }

    .form-item {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    textarea, select {
        background-color: #D9D9D9;
        padding: 0.3rem;
    }

    input, textarea {
        width: 100% !important;
        border-radius: 0.5rem;
    }

    select {
        border-radius: 0.5rem;
    } 

    #dimensions-container, .dimension {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .dimension div {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    #dimensions-container .dimension select {
        border-radius: 0.4rem;
        text-align: center;
        width: 4rem !important;
    }

    #type-container select, #price-container input, #pages-container input, #colour-container select, #sources-container select, #condition-container select, .dimension input {
        width: 8rem !important;
        text-align: center;
    }

    #pages-container div {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    #subject-container div {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    #subject-container input {
        width: 20rem !important;
    }

    #author-div {
        display: flex;
        align-items: center;
    }

    #author-div input, #delivery-container #options div input, #returns-container input {
        width: 3.5rem !important;
        border-radius: 10rem !important;
        height: 1.3rem;
    }

    #author span {
        color: #0DCAF0;
    }

    #dark #author span {
        color: white;
    }

    #images {
        display: flex;
        gap: 1rem;
    }

    #image-container p, #video-container p {
        color: red;
    }

    #image1, #image2, #video1 {
        display: none;
    }

    .input-square, .video-square {
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

    .input-square i, .video-square i {
        font-size: 2rem;
    }

    .input-square:hover, .video-square:hover {
        color: #0DCAF0;
        background-color: #0DCAF0;
    }

    img {
        display: none;
        max-height: 100%;
        max-width: 100%;
    }

    #price-flex {
        display: flex;
        gap: 1rem;
    }

    .image_input button, .video_input button {
        background: transparent;
        color: red;
        border: none;
        position: absolute;
        top: 0.2rem;
        right: 0.3rem;
    }

    .image_input button i, .video_input button i {
        font-size: 1.3rem;
    }

    .image_input button:hover, .video_input button:hover {
        color: rgb(96, 28, 28);
        cursor: pointer;
    }

    video {
        display: none;
        max-height: 100%;
        width: 100%;
        background-color: yellow;
    }

    #header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }

    #header button, #buttons1 button {
        font-size: 1.2rem;
        padding: 0.3rem;
        padding-left: 1rem;
        padding-right: 1rem;
        border-radius: 0.5rem;
        border: none;
        background-color: #0DCAF0;
    }

    #header button:hover, #buttons1 button:hover {
        background-color: #50afc2;
        cursor: pointer;
    }

    #dark #header button, #dark #buttons1 button {
        background-color: black;
        color: white;
    }

    #dark #header button:hover, #dark #buttons1 button:hover {
        background-color: darkgray;
        color: black;
    }

    #buttons, #buttons1 {
        display: flex;
        gap: 1rem;
    }

    textarea {
        height: 6rem;
    }

    .required {
        color: red !important;
    }

    #first_image {
        padding: 0;
        background: none;
        width: 3.6rem !important;
        color: black;
        pointer-events: none;
    }

    #first_image:focus {
        border: none;
        pointer-events: none;
    }

    textarea:focus {
        background-color: white;
    }

    #buttons1 {
        margin-top: 1rem;
        justify-content: flex-end;
    }

    #resource_exists {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
        background-color: #0DCAF0;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    #dark #resource_exists {
        background-color: darkgray;
    }

    #duplicate {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
        background-color: red;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    #images-label, #videos-label {
        display: flex;
        margin-right: auto;
        background-color: red;
        color: white !important;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    .delete_listing {
        color: white !important;
        background-color: red !important;
    }

    .delete_listing:hover {
        background-color: rgb(133, 21, 21) !important;
    }

    #delivery-container #options {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    #delivery-container #options div {
        display: flex;
        align-items: center;
    }

    #delivery-container #options label {
        width: 8rem;
    }

</style>