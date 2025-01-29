<template>
    <div id="buyer-home">
        <div id="recommendations">
            <div class="header">
                <p>Recommendations</p>
            </div>
            <div class="displays">
                <div v-for="listing in textbooks">
                    <div class="listed" v-if="listing.type === 'Textbook'" @click="showResourcePage(listing.name)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Textbook">
                        {{ listing.price }}
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
                    <div class="listed" v-if="listing.type === 'Textbook'" @click="showResourcePage(listing.name)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Textbook">
                        {{ listing.price }}
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
                    <div class="listed" @click="showResourcePage(listing.name)">
                        <img :src="`http://localhost:8000${listing.image1}`" alt="Note">
                        {{ listing.price }}
                    </div>
                </div>
            </div>
        </div>
        <div id="stationery">
            <div>
                <p> Stationery</p>
                <div class="displays">
                    <div v-for="listing in stationery">
                        <div class="listed" @click="showResourcePage(listing.name)">
                            <img :src="`http://localhost:8000${listing.image1}`" alt="Note">
                            {{ listing.price }}
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
            showResourcePage(resourceName: string): void {
                window.location.href = `/view-resource/${resourceName}`
            },
        },
        computed: {
            user(): User {
                return useUserStore().user
            },
            resources(): Resource[] {
                return useResourcesStore().resources
            },
            textbooks(): Resource[] {
                if (!this.resources) return []
                return this.resources.filter(resource => resource.type === 'Textbook' && !resource.is_draft)
            },
            notes(): Resource[] {
                if (!this.resources) return []
                return this.resources.filter(resource => resource.type === 'Notes' && !resource.is_draft)
            },
            stationery(): Resource[] {
                if (!this.resources) return []
                return this.resources.filter(resource => resource.type === 'Stationery' && !resource.is_draft)
            }
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
