<template>
    <div id="buyer-home">
        <div id="recommendations" v-if="Object.keys(user).length > 0">
            <div class="header">
                <p>Recommended for you</p>
            </div>
            <div class="displays">
                <div v-for="listing in recommendations">
                    <div class="listed" v-if="listing.type === 'Textbook'" @click="showResourcePage(listing)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Textbook">
                        {{ currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
                <div class="no_resources" v-if="recommendations.length===0"> 
                    <p>No recommendations to display</p>
                </div>
            </div>
        </div>
        <div id="textbooks">
            <div class="header">
                <p>  Textbooks</p>
            </div>
            <div class="displays">
                <div v-for="listing in textbooks">
                    <div class="listed" v-if="listing.type === 'Textbook'" @click="showResourcePage(listing)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Textbook">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
                <div class="no_resources" v-if="textbooks.length===0"> 
                    <p>No textbook listings to display</p>
                </div>
            </div>
        </div>
        <div id="notes">
            <div class="header">
                <p> Notes </p>
            </div>
            <div class="displays">
                <div v-for="listing in notes">
                    <div class="listed" @click="showResourcePage(listing)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Note">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
                <div class="no_resources" v-if="notes.length===0"> 
                    <p>No note listings to display</p>
                </div>
            </div>
        </div>
        <div id="stationery">
            <div class="header">
                <p> Stationery </p>
            </div>
            <div class="displays">
                <div v-for="listing in stationery">
                    <div class="listed" @click="showResourcePage(listing)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Note">
                        {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
                </div>
                <div class="no_resources" v-if="stationery.length===0"> 
                    <p>No stationery listings to display</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent, nextTick } from 'vue';
    import type { Resource, User } from '@/types';
    import { useResourcesStore } from '@/stores/resources';
    export default defineComponent({
        data(): {
            recommendations: Resource[]
            editingDescription: boolean
            textbookMessage: 'All' | 'Sold' | 'Drafted',
            notesMessage: 'All' | 'Sold' | 'Drafted',
            stationeryMessage: 'All' | 'Sold' | 'Drafted',
        } { return {
            recommendations: [],
            editingDescription: false,
            textbookMessage: 'All',
            notesMessage: 'All',
            stationeryMessage: 'All'
        }},
        methods: {
            async get_recommendations(): Promise<void> {
                const personalised_recommendations: Response = await fetch(`http://localhost:8000/api/recommendations/${useUserStore().user.id}/`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken' : useUserStore().csrf
                    }
                })
                if (!personalised_recommendations.ok) {
                    this.recommendations = this.resources
                }
                let recommendations: Resource[] = await personalised_recommendations.json()
                this.recommendations = recommendations
            },
            async listedprice(resource: Resource): Promise<number> {
                if (Object.keys(this.user).length === 0) {
                    // if user is unauthenticated
                    return resource.price
                }
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
            showResourcePage(resource: Resource): void {
                window.location.href = `/view/${resource.id}`
            },
            unauth_currency(resource: Resource): string {
                return resource.price_currency === 'GBP' ? '£' : resource.price_currency === 'USD' ? '$' : '€' 
            },
        },
        computed: {
            currency(): string {
                return this.user.currency === 'GBP' ? '£' : this.user.currency === 'USD' ? '$' : '€' 
            },
            user(): User {
                if (Object.keys(useUserStore().user).length > 0) {
                    this.get_recommendations()
                } else {
                    nextTick(() => {
                        let div: HTMLDivElement = document.getElementById('buyer-home') as HTMLDivElement
                        if (div) {
                            div.style.gridTemplateAreas = "'textbooks' 'notes' 'stationery'";
                        } 
                    })
                }
                return useUserStore().user
            },
            resources(): Resource[] {
                const allResources: Resource[] = useResourcesStore().resources
                let generic_items = new Map()
                let newAllResources = [] as Resource[]
                for (let resource of allResources) {
                    if (parseInt(resource.stock.toString()) < 1 || resource.is_draft || !(resource.allow_collection || resource.allow_delivery)) continue
                    if (!resource.unique) {
                        if (!(generic_items.get(resource.name)) || (generic_items.get(resource.name) !== resource.author)) {
                            newAllResources.push(resource)
                            generic_items.set(resource.name, resource.author)
                        } 
                    } else {
                        newAllResources.push(resource)
                    }
                }
                return newAllResources
            },
            textbooks(): Resource[] {
                if (!this.resources) return []
                return this.resources.filter(resource => resource.type === 'Textbook')
            },
            notes(): Resource[] {
                if (!this.resources) return []
                return this.resources.filter(resource => resource.type === 'Notes')
            },
            stationery(): Resource[] {
                if (!this.resources) return []
                return this.resources.filter(resource => resource.type === 'Stationery')
            },
        },
        watch: {
            async user(): Promise<void> {
                for (const resource of this.resources) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resources(resources: Resource[]): Promise<void> {
                for (const resource of resources) {
                    resource.price = await this.listedprice(resource)
                }
            }
        }
    })
</script>

<style scoped>
    #buyer-home {
        display: grid;
        grid-template-areas: "recommendations" "textbooks" "notes" "stationery";
        height: 89vh;
        width: 98vw;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        overflow-y: auto;
        gap: 1.5rem;
    }

    #recommendations {
        grid-area: recommendations;
    }

    #textbooks {
        grid-area: textbooks;
    }

    #recommendations, #textbooks, #notes, #stationery {
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        height: 12.5rem;
        margin-left: 1.5rem;
        margin-right: 1.5rem;
        padding: 0.5rem;
    }

    .header {
        display: flex;
        justify-content: space-between;
    }

    img {
        height: 7rem;
        width: 7rem;
        object-fit: contain;
    }

    .listed {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0.4rem;
    } 

    .displays {
        display: flex;
        gap: 3rem;
        overflow-x: scroll;
        margin-top: 1rem;
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

    .header button i {
        font-size: 2rem;
    }

    .header button:hover { 
        color: #0DCAF0;
        cursor: pointer;
    }

    .listed:hover {
        background-color: lightgray;
        border-radius: 0.5rem;
        cursor: pointer;
    }

    #dark .listed:hover {
        color: black !important;
    }

    #dark #buyer-home {
        color: white !important;
    }

    .no_resources {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Responsive Design */
    @media (max-width: 510px) {
        #recommendations, #textbooks, #notes, #stationery {
            width: 83vw;
        }
    }

    @media (max-width: 431px) {
        #recommendations, #textbooks, #notes, #stationery {
            width: 80vw;
        }
    }
</style>
