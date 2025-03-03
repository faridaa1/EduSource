<template>
  <div id="app-vue" v-if="complete">
    <div id="light">
      <header id="main-header">
        <img id='logo' src="/logo-light.svg" alt="EduSource" width="125" height="125" v-pre/>
        <RouterLink :to="Object.keys(user).length > 0 && user.mode === 'seller' ? '/listings' : '/'" class="hide-on-mobile link">Home</RouterLink>
        <div id="profile-div" class="hide-on-mobile">
          <p id="profile-header" v-if="authenticated" @click="toggle_profile_view">Profile</p>
          <transition name="nav">
              <div id="profile-nav" v-if="clicked_profile">
                <RouterLink class="profile-item border-bottom rounded-top" to="/details" >Details</RouterLink>
                <RouterLink class="profile-item border-bottom" to="/orders" v-if="user.mode==='buyer'">Orders</RouterLink>
                <RouterLink class="profile-item border-bottom" to="/messages">Messages</RouterLink>
                <RouterLink class="profile-item border-bottom" to="/cart">Cart</RouterLink>
                <RouterLink class="profile-item rounded-bottom" to="/wishlist" v-if="user.mode==='buyer'">Wishlist</RouterLink>
                <RouterLink class="profile-item border-bottom" to="/listings" v-if="user.mode==='seller'">Listings</RouterLink>
                <RouterLink class="profile-item rounded-bottom" to="/" v-if="user.mode==='seller'">Orders</RouterLink>
            </div>
          </transition>
        </div>
        <div id="search-div">
          <input id="search" @input="semantic_search" type="text" placeholder="Search">
          <div id="search-results" v-if="searching">
            <div class="search-result" v-for="resource in search_results" @click="conduct_search(resource)">
              {{ resource.name }}
            </div>
          </div>
          <button @click="conduct_search()"><i class="bi bi-search"></i></button>
        </div>
        <RouterLink to="/" class="hide-on-mobile link">Help</RouterLink>
        <RouterLink to="/settings" class="hide-on-mobile link" v-if="Object.keys(user).length > 0">Settings</RouterLink>
        <p v-if="authenticated" class="hide-on-mobile link sign" @click="sign_out"> Sign out </p>
        <p v-if="!authenticated" @click="sign_in" class="hide-on-mobile link sign"> Sign in</p>
        <button id="show-on-mobile" @click="mobile_menu=true"><i class="bi bi-list"></i></button>
      </header>
      <transition name="nav">
        <div id="hamburger" v-if="mobile_menu">
          <RouterLink id="item1" :to="Object.keys(user).length > 0 && user.mode === 'seller' ? '/listings' : '/'" class="show-mobile">Home</RouterLink>
          <div id="item2" class="show-mobile" v-if="authenticated">
            <p id="profile-header" @click="toggle_profile_view_mobile">Profile</p>
            <transition name="nav">
              <div id="profile-nav" v-if="clicked_profile_mobile">
                <RouterLink class="profile-item border-bottom rounded-top" to="/details" >Details</RouterLink>
                <RouterLink class="profile-item border-bottom" to="/orders" v-if="user.mode==='buyer'">Orders</RouterLink>
                <RouterLink class="profile-item border-bottom" to="/messages">Messages</RouterLink>
                <RouterLink class="profile-item border-bottom" to="/cart">Cart</RouterLink>
                <RouterLink class="profile-item rounded-bottom" to="/wishlist" v-if="user.mode==='buyer'">Wishlist</RouterLink>
                <RouterLink class="profile-item border-bottom" to="/listings" v-if="user.mode==='seller'">Listings</RouterLink>
                <RouterLink class="profile-item rounded-bottom" to="/" v-if="user.mode==='seller'">Orders</RouterLink>
            </div>
          </transition>
          </div>
          <RouterLink to="/" id="item3" class="show-mobile">Help</RouterLink>
          <RouterLink v-if="authenticated" to="/settings" id="item4" class="show-mobile">Settings</RouterLink>
          <p id="item5" v-if="authenticated" class="link sign" @click="sign_out"> Sign out </p>
          <p id="item5" v-if="!authenticated" @click="sign_in" class="link sign"> Sign in</p>
        </div>
      </transition>
      <RouterView />
   </div>
  </div>
  <div v-else>
    <Loading />
   </div>
</template>

<script lang="ts">
  import { defineComponent, nextTick } from 'vue';
  import { RouterView } from 'vue-router'
  import type { Resource, User } from './types';
  import { useUserStore } from './stores/user';
  import { useResourcesStore } from './stores/resources';
  import { useUsersStore } from './stores/users';
  import Loading from './components/user experience/loading/Loading.vue';
  export default defineComponent({
    components: { RouterView, Loading },
    data(): { searching: boolean, authenticated: boolean, search_results: Resource[], clicked_profile: boolean, mobile_menu: boolean, complete: boolean, clicked_profile_mobile: boolean } { return {
        searching: false,
        authenticated: false,
        search_results: [] as Resource[],
        complete: false,
        mobile_menu: false,
        clicked_profile_mobile: false,
        clicked_profile: false
      }
    },
    async mounted(): Promise<void> {
      this.toggle_theme()
      window.addEventListener('resize', () => {
        this.clicked_profile = false;
        this.clicked_profile_mobile = false;
        this.mobile_menu = false
      })
      document.addEventListener('click', (event) => {
        if (this.clicked_profile) {
          const div: HTMLDivElement = event.target as HTMLDivElement
          if (div.parentNode && (div.parentNode as HTMLDivElement).id !== 'profile-div') {
            this.clicked_profile = false
          } 
        }
        if (this.mobile_menu) {
          const div: HTMLDivElement = event.target as HTMLDivElement
          if (div.parentNode && (div.parentNode as HTMLDivElement).id !== 'show-on-mobile' && (div.parentNode as HTMLDivElement).id !== 'item2') {
            this.mobile_menu = false
            this.clicked_profile_mobile = false
          } 
        }
        this.searching = false
        let target: HTMLElement = event.target as HTMLElement
        if (target.id === 'logo' && !(window.location.pathname === '/') && !(window.location.pathname === '/listings')) this.go_home()
        if (target.id !== 'search') {
          this.search_results = []
        }
      })
      let usersResponse: Response = await fetch('http://localhost:8000/api/users/', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'X-CSRFToken' : useUserStore().csrf
        }
      })
      let usersData: User[] = await usersResponse.json()
      useUsersStore().updateUsers(usersData)

      let userResponse: Response = await fetch('http://localhost:8000/api/user/', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'X-CSRFToken' : useUserStore().csrf
        }
      })
      let userData: { user: User | 'unauthenticated' } = await userResponse.json()
      this.complete = true
      for (let cookie of document.cookie.split(';')) {
        const cookie_pair = cookie.split('=')
          if (cookie_pair[0] === 'csrftoken') {
            useUserStore().saveCsrf(cookie_pair[1])
          }
      }
      if (userData.user === 'unauthenticated') {
        nextTick(() => {
          let header: HTMLHeadingElement = document.getElementById('main-header') as HTMLHeadingElement
          header.style.gridTemplateColumns = '1fr 1fr 0fr 2fr 1fr 1fr'
        })
        
      } else {
        this.authenticated = true
        useUserStore().saveUser(userData.user)
        this.toggle_theme()
      }
      let getResourcesStore: Response = await fetch(`http://localhost:8000/api/resources/`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'X-CSRFToken' : useUserStore().csrf
          },
        })
        if (!getResourcesStore.ok) {
          return
        }
        let resources: Resource[] = await getResourcesStore.json()
        useResourcesStore().saveResources(resources)
        this.complete = true
    },
    computed: {
      user(): User {
        return useUserStore().user
      }
    },
    watch: {
      user(): void {
        this.toggle_theme()
      }
    },
    methods: {
      toggle_profile_view(): void {
        this.clicked_profile = !this.clicked_profile
      },
      toggle_profile_view_mobile(): void {
        this.clicked_profile_mobile = !this.clicked_profile_mobile
      },
      toggle_theme(): void {
        if (Object.keys(this.user).length === 0) return
        nextTick(() => {
          const div = document.getElementById('app-vue')
          if (div) {
            const theme = div.firstElementChild
            if (theme) {
                theme.id = this.user.theme_preference
                document.body.style.backgroundColor = theme.id === 'light' ? 'white' : '#807E7E'
                const logo: HTMLImageElement = document.getElementById('logo') as HTMLImageElement
                if (logo) {
                    logo.src = theme.id === 'light' ? '/logo-light.svg' : '/logo-dark.svg'
                }
            }
          }
        })
      },
      conduct_search(resource?: Resource): void {
        this.searching = false
        if (resource) {
          window.location.href = `/search/${resource.name}`
        } else {
          const search: HTMLInputElement = document.getElementById('search') as HTMLInputElement
          if (search) {
            window.location.href = `/search/${search.value}`
          }
        }
      },
      async semantic_search(): Promise<void> {
        this.searching = true
        const search: HTMLInputElement = document.getElementById('search') as HTMLInputElement
        if (!search) return
        if (search.value === '') {
          this.search_results = []
          return
        }
        const searchResults: Response = await fetch(`http://localhost:8000/api/semantic-search/`, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : useUserStore().csrf
          },
          body: JSON.stringify(search.value)
        })
        if (!searchResults.ok) {
          return
        }
        const search_results: Resource[] = await searchResults.json()
        this.search_results = search_results
      },
      go_home(): void {
        window.location.href = Object.keys(this.user).length === 0 || this.user.mode === 'buyer' ? '/' : '/listings'
      },
      async sign_out(): Promise<void> {
        await fetch(`http://localhost:8000/signout/`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : useUserStore().csrf
          },
        })
        window.location.href = '/'
      },
      async sign_in(): Promise<void> {
        window.location.href = 'http://localhost:8000/login'
      },
    }
  })
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
  @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css');
  
  #show-on-mobile {
    display: none;
  }

  body {
    overflow: hidden;
    position: relative;
  }

  .nav-enter-active, .nav-leave-active {
    transition: opacity 0.1s ease;
  }

  .nav-enter-from, .nav-leave-to {
    opacity: 0;
  }

  #app-vue #search-results {
    position: absolute;
    margin-top: 2rem;
    background-color: white !important;
    border-radius: 0.5rem;
    padding: 0.25rem;
    display: flex;
    flex-direction: column;
    width: 11.6rem;
  }

  .search-result {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 0.25rem;
  }

  .search-result:hover {
    cursor: pointer;
    background-color: #D9D9D9;
  }

  .sign:hover {
    cursor: pointer;
    text-decoration: underline;
  }

  #dark #hamburger #profile-header, #dark #hamburger .sign {
    color: black !important;
  }

  #logo {
    height: 1.6rem;
    padding: 0;
    margin: 0;
  }

  #logo:hover {
    cursor: pointer;
  }
  
  #app-vue header {
    padding: 0.5rem;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 2fr 1fr 1fr 1fr;
    place-items: center;
    padding-top: 0.8rem;
    background-color: #0DCAF0;
    padding-bottom: 0.8rem;
  }

  #app-vue #dark header {
    background-color: black;
  }

  #app-vue a {
    color: black;
    text-decoration: none;
  }

  #app-vue a:hover, #profile-header:hover {
    text-decoration: underline;
  }

  #app-vue #dark .link {
    color: white;
  }

  #app-vue #search-div {
    display: flex;
  }

  #app-vue input {
    background-color: #D9D9D9;
    border-top-left-radius: 0.4rem;
    border-bottom-left-radius: 0.4rem;
    border: none;
    padding: 0.3rem;
    width: 100%;
  }

  #app-vue input:focus {
    background-color: white;
  }

  #profile-header:hover {
    cursor: pointer;
  }

  #dark #profile-header {
    color: white;
  }

  #app-vue #search-div button {
    border: none;
    border-top-right-radius: 0.4rem;
    border-bottom-right-radius: 0.4rem;
    background-color: rgb(224, 222, 222);
    padding-right: 0.3rem;
    padding-left: 0.3rem;
  }

  #app-vue #search-div button:hover {
    cursor: pointer;
    background-color: darkgrey;
  }

  #profile-nav {
    position: absolute;
    display: flex;
    flex-direction: column;
    background-color: #D9D9D9;
    border-radius: 0.5rem;
    transition: opacity 0.4s ease;
    align-items: center;
    top: 2.3rem;
    right: -2.5rem;
  }

  .profile-nav-mobile {
    top: 2.3rem !important;
    right: 6rem;
    opacity: 1 !important;
    transition: opacity 0.4s ease;
  }

  #profile-div {
    position: relative;
  }

  #light .border-bottom {
    border-bottom: 0.1rem solid darkgray;
  }

  #dark .border-bottom {
    border-bottom: 0.1rem solid darkgray;
  }

  .profile-item {
    width: 6rem;
    text-align: center;
    padding: 0.6rem;
  }

  .rounded-bottom {
    border-bottom-right-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
  }

  .rounded-top {
    border-top-right-radius: 0.5rem;
    border-top-left-radius: 0.5rem;
  }

  .profile-item:hover {
    background-color: #0DCAF0;
  }


  /* Responsive Design */
  @media (max-width: 871px) {
    #hamburger {
      position: absolute;
      top: 0;
      right: 0rem;
      grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
      place-items: center;
      border-radius: 0.5rem;
    }

    #item2 #profile-nav {
      top: 0rem;
      right: 6.1rem;
    }

    #item2 .profile-nav-mobile {
      /* right: 6.2rem !important; */
      right: 10rem !important;
    }

    #app-vue header {
      grid-template-columns: 1fr 2fr 1fr!important;
    }

    .hide-on-mobile {
      display: none;
    }

    #show-on-mobile {
      position: relative;
      display: block;
      background-color: transparent;
      border: none;
      font-size: 1.5rem;
    }

    #show-on-mobile i {
      font-size: 1.5rem;
    }

    #show-on-mobile:hover {
      cursor: pointer;
    }

    #dark #show-on-mobile {
      color: white;
    }

    #item1, #item2, #item3, #item4, #item5 {
      display: block;
      width: 6rem;
      text-align: center;
      align-self: center;
      padding-top: 0.5rem;
      padding-bottom: 0.5rem;
      background-color: #D9D9D9;
    }

    #item1, #item2, #item3, #item4 {
      border-bottom: 0.1rem solid white;
    }

    #dark #item1, #dark #item2, #dark #item3, #dark #item4, #dark #item5 {
      border-bottom: 0.1rem solid darkgray;
    }

    #item1:hover, #item2:hover, #item3:hover, #item4:hover, #item5:hover {
      background-color: #0DCAF0;
    }

    #item5 {
      border-bottom-right-radius: 0.5rem;
      border-bottom-left-radius: 0.5rem;
    }

    #item1 {
      grid-column: 3;
      grid-row: 1;
      border-top-right-radius: 0.5rem;
      border-top-left-radius: 0.5rem;
    }

    #item2 {
      position: relative;
      grid-column: 3;
      grid-row: 2;
    }

    #item3 {
      grid-column: 3;
      grid-row: 3;
    }

    #item4 {
      position: relative;
      grid-column: 3;
      grid-row: 4;
    }

    #item5 {
      grid-column: 3;
      grid-row: 5;
    }
  }

  /* Responsive Design */
  @media (min-width: 1110px) {
    #app-vue input {
      width: 30rem;
    }

    #app-vue #search-results {
      width: 31.2rem;
    }
  }

  @media (min-width: 1667px) {
    #app-vue input {
      width: 40rem;
    }
    #app-vue #search-results {
      width: 41.2rem;
    }
  }

  @media (max-width: 654px) {
    #app-vue header {
      position: relative;
      display: grid;
      grid-template-columns: 1fr 2fr 1fr;
      place-items: center;
      padding-top: 0.8rem;
      padding-bottom: 0.8rem;
    }

    #app-vue .show-mobile {
      display: block;
      right: 0;
    }

    #app-vue #dark .show-mobile {
      color: black;
    }
  }

  ::-webkit-scrollbar {
      width: 0.5rem;
      height: 0.5rem;
  }

  ::-webkit-scrollbar-track {
      background: lightgray;
      border-radius: 1rem;
  }

  ::-webkit-scrollbar-thumb {
      background: darkgrey;
      border-radius: 1rem;
  }

  ::-webkit-scrollbar-thumb:hover {
      background:rgb(50, 55, 56);
      margin-left: 1rem;
  }
</style>
