<template>
    <div id="search-container">
        <div id="search-heading">
            <div id="heading1">
                <p>Search Results</p>
            </div>
            <div id="heading2">
                <div id="sort_by">
                    <label>Sort by</label>
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
                    <label>Filter</label>
                </div>
            </div>
        </div>
        <div id="search-content">
            <div class="search-item" v-for="resource in resources">
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
    import { defineComponent, nextTick } from 'vue';
    import type { Resource, User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            resources: Resource[],
            search_value: string,
            sorting: boolean,
            filtering: boolean,
            sort_by: 'listing-new' | 'listing-old' | 'rating-low' | 'rating-high' | 'price-low' | 'price-high'
        } { return {
            search_value: '',
            resources: [],
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
        },
        watch: {
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
            },
            sort_by() {
                this.sort_resources()
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

    #search-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        margin: 1rem;
    }

    #search-heading {
        display: flex;
        justify-content: space-between;
    }

    #heading1 p, #heading2 label {
        font-size: 1.5rem;
    }

    #heading2 {
        display: flex;
        gap: 2rem;
    }

    select {
        padding: 0.4rem;
        font-size: 1.3rem;
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
        overflow-y: scroll;
    }
</style>
