<template>
    <div id="new-listing">
        <h1>New Resource Listing</h1>
        <div>
            <div>
                <label for="">Name</label>
                <input type="text" name="" id="" v-model="name">
            </div>
            <div>
                <label for="">Description</label>
                <textarea name="" id=""></textarea>
            </div>
            <div>
                <label for="">Dimension</label>
                <div>
                    <div>
                        <label for="">Height</label>
                        <input type="number" min="0" v-model="height">
                        <select name="" id="" v-model="dimension_unit">
                            <option value="cm">cm</option>
                            <option value="m">m</option>
                            <option value="in">in</option>
                        </select>
                    </div>
                    <div>
                        <label for="">Width</label>
                        <input type="number" min="0" v-model="width">
                        <select name="" id="" v-model="dimension_unit">
                            <option value="cm">cm</option>
                            <option value="m">m</option>
                            <option value="in">in</option>
                        </select>
                    </div>
                    <div>
                        <label for="">Weight</label>
                        <input type="number" min="0" v-model="weight">
                        <select name="" id="" v-model="weight_unit">
                            <option value="kg">kg</option>
                            <option value="ml">ml</option>
                            <option value="L">L</option>
                            <option value="mg">mg</option>
                            <option value="oz">oz</option>
                            <option value="lb">lb</option>
                        </select>
                    </div>
                </div>
            </div>
            <div>
                <label for="">Type</label>
                <select name="" id="" v-model="type">
                    <option value="Textbook">Textbook</option>
                    <option value="Notes">Notes</option>
                    <option value="Stationery">Stationery</option>
                </select>
            </div>
            <div>
                <label for="">Colour</label>
                <select name="" id="" v-model="colour">
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
            <div>
                <label for="">Author</label>
                <input type="text" v-model="author">
                <div>
                    <label for="">Select if the listed resource was self-made</label>
                    <input type="checkbox" name="" id="">
                </div>
            </div>
            <div>
                <label for="">Assisted Sources</label>
                <select name="" id="" v-model="source">
                    <option value="AI">AI</option>
                    <option value="Internet">Internet</option>
                    <option value="None">None</option>
                </select>
            </div>
            <div>
                <label for="">Condition</label>
                <select name="" id="" v-model="condition">
                    <option value="New">New</option>
                    <option value="Used">Used</option>
                </select>
            </div>
            <div>
                <label for="">Price</label>
                <input type="number" min="0" step="0.01">
            </div>
            <div>
                <label for="">Images</label>
                <div>
                    <input id="image1" type="file" accept=".png" @change="(event) => show_image(event, 1)">
                    <img id="img1" src="" alt="">
                </div>
                <div>
                    <input id="image2" type="file" accept=".png" @change="(event) => show_image(event, 2)">
                    <img id="img2" src="" alt="">
                </div>
            </div>
            <div>
                <label for="">Videos</label>
                <div>
                    <input id="video1" type="file" accept=".mp4" @change="(event) => show_video(event, 1)">
                    <video id="vid1" src="" controls></video>
                </div>
                <div>
                    <input id="video2" type="file" accept=".mp4" @change="(event) => show_video(event, 2)">
                    <video id="vid2" src="" controls></video>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { User } from '@/types';
    export default defineComponent({
        data(): {
            name: string,
            description: string,
            height: number,
            width: number,
            weight: number,
            weight_unit: string,
            dimension_unit: string,
            type: 'Textbook' | 'Notes' | 'Stationery'
            colour: 'Black' | 'Red' | 'Yellow' | 'Pink'
                    | 'Purple' | 'Green' | 'Blue' | 'White'
                    | 'Orange' | 'Brown' | 'Grey'
            author: string | 'Self',
            condition: 'New' | 'Used',
            source: 'AI' | 'Internet' | 'None',
            price: number
        } { return {
            name: '',
            description: '',
            height: 0,
            width: 0,
            weight: 0,
            weight_unit: 'lb',
            dimension_unit: 'cm',
            type: 'Textbook',
            colour: 'Black',
            author: 'Self',
            condition: 'Used',
            source: 'None',
            price: 0
        }},
        methods: {
            show_video(event: Event, image_number: number): void {
                const inputElement: HTMLInputElement = event.target as HTMLInputElement
                if (!inputElement.files) return
                const video: File = inputElement.files[0]
                if (!video) return
                const vid: HTMLImageElement = document.getElementById(image_number === 1 ? 'vid1' : 'vid2') as HTMLImageElement
                if (!vid) return
                vid.src = URL.createObjectURL(video)
            },
            show_image(event: Event, image_number: number): void {
                const inputElement: HTMLInputElement = event.target as HTMLInputElement
                if (!inputElement.files) return
                const image: File = inputElement.files[0]
                if (!image) return
                const img: HTMLImageElement = document.getElementById(image_number === 1 ? 'img1' : 'img2') as HTMLImageElement
                if (!img) return
                img.src = URL.createObjectURL(image)
            },
            new_listing():void {
                window.location.href = '/new-listing'
            }
        },
        computed: {
            user(): User {
                let user: User = useUserStore().user
                return user
            }
        },
        watch: {
            user(new_user) {
            }
        },
        mounted(): void {
        }
    })
</script>
<style scoped>
    #new-listing {
        height: 54rem;
        overflow-y: auto;
        padding-right: 10rem;
        padding-top: 3rem;
        padding-left: 3rem;
    }

    h1 {
        margin-bottom: 2rem;
    }
    img {
        height: 10rem;
        width: 10rem;
    }
    video {
        width: 30rem;
        height: auto;
    }
</style>
