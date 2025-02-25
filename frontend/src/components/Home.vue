<template>
    <div id="buyer-home">
        <div id="recommendations" v-if="Object.keys(user).length > 0">
            <div class="header">
                <p>Recommendations</p>
            </div>
            <div class="displays">
                <div v-for="listing in textbooks">
                    <div class="listed" v-if="listing.type === 'Textbook'" @click="showResourcePage(listing)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Textbook">
                        {{ currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                    </div>
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
            </div>
        </div>
        <div id="stationery">
            <div>
                <p> Stationery</p>
                <div class="displays">
                    <div v-for="listing in stationery">
                        <div class="listed" @click="showResourcePage(listing)">
                            <img :src="`http://localhost:8000${listing.image1}`" alt="Note">
                            {{ Object.keys(user).length === 0 ? unauth_currency(listing) : currency }}{{ listing.price.toString().replace('€','').replace('£','').replace('$','') }}
                        </div>
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
    import { useResourcesStore } from '@/stores/resources';
    export default defineComponent({
        data(): {
            editingDescription: boolean
            textbookMessage: 'All' | 'Sold' | 'Drafted',
            notesMessage: 'All' | 'Sold' | 'Drafted',
            stationeryMessage: 'All' | 'Sold' | 'Drafted',
        } { return {
            editingDescription: false,
            textbookMessage: 'All',
            notesMessage: 'All',
            stationeryMessage: 'All'
        }},
        methods: {
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
            async user(new_user: User): Promise<void> {
                // this.user = new_user
                for (const resource of this.resources) {
                    resource.price = await this.listedprice(resource)
                }
            },
            async resources(resources: Resource[]): Promise<void> {
                for (const resource of resources) {
                    resource.price = await this.listedprice(resource)
                }
            }
        },
        async mounted() {
            
        }
    })
</script>

<style scoped>
    #buyer-home {
        display: grid;
        grid-template-areas: "recommendations recommendations"
                             "textbooks textbooks"
                             "notes stationery";
        padding-right: 30rem;
    }

    #recommendations {
        grid-area: recommendations;
        align-items: center;
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 2rem;
        width: 98vw;
    }

    #textbooks {
        grid-area: textbooks;
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 2rem;
        width: 98vw;
    }

    .header {
        display: flex;
        justify-content: space-between;
    }

    img {
        height: 10rem;
        width: fit-content;
    }

    .listed {
        display: flex;
        flex-direction: column;
        align-items: center;
    } 

    .displays {
        display: flex;
        gap: 4rem;
        overflow-x: scroll;
        margin-top: 1rem;
        padding-bottom: 1rem;
    }

    #notes {
        grid-area: notes;
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 2rem;
        margin-right: 1rem;
        width: 96.5%;
    }

    #stationery {
        grid-area: stationery;
        border: 0.1rem solid #D9D9D9;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin-top: 2rem;
        width: 90.5%;
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
</style>
