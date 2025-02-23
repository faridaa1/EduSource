<template>
  <div id="app-vue">
    <div id="light">
      <header id="main-header">
        <img id='logo' src="/logo-light.svg" alt="EduSource" width="125" height="125" v-pre/>
        <RouterLink to="/" class="hide-on-mobile link">Home</RouterLink>
        <div id="profile-div" class="hide-on-mobile" @click="show_profile('desktop')">
          <p id="profile-header" v-if="authenticated">Profile</p>
          <div id="profile-nav">
            <RouterLink class="profile-item border-bottom rounded-top" to="/details" >Details</RouterLink>
            <RouterLink class="profile-item border-bottom" to="/orders" v-if="user.mode==='buyer'">Orders</RouterLink>
            <RouterLink class="profile-item border-bottom" to="/cart">Cart</RouterLink>
            <RouterLink class="profile-item rounded-bottom" to="/wishlist" v-if="user.mode==='buyer'">Wishlist</RouterLink>
            <RouterLink class="profile-item border-bottom" to="/listings" v-if="user.mode==='seller'">Listings</RouterLink>
            <RouterLink class="profile-item rounded-bottom" to="/" v-if="user.mode==='seller'">Orders</RouterLink>
          </div>
        </div>
        <div id="search-div">
          <input type="text" placeholder="Search">
          <button><i class="bi bi-search"></i></button>
        </div>
        <RouterLink to="/" class="hide-on-mobile link">Help</RouterLink>
        <div id="main-settings" class="hide-on-mobile">
          <p id="settings-header" @click="show_settings('desktop')" v-if="authenticated">Settings</p>
          <div id="settings">
            <div id="theme" class="setting">
              <label for="">Theme</label>
              <div id="toggle" @click="(event) => toggle_theme('click', event)">
                <div id="circle">
                </div>
              </div>
            </div>
            <div id="currency" class="setting">
              <label for="">Currency</label>
              <select id="currency-dropdown" v-model="currency_setting" @change="update_setting('currency', currency_setting)">
                <option v-for="currency in ['USD', 'GBP', 'EUR']" :key="currency" :value="currency">
                  {{ currency }}
                </option>
              </select>
            </div>
            <div id="mode" class="setting" v-if="authenticated">
              <label for="">Mode</label>
              <select id="currency-dropdown" v-model="mode_setting" @change="update_setting('mode', mode_setting)">
                <option v-for="mode in ['buyer', 'seller']" :key="mode" :value="mode">
                  {{ mode }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <!-- <RouterLink to="http://localhost:8000/login" class="hide-on-mobile link">Sign out</RouterLink> -->
        <p v-if="authenticated" class="hide-on-mobile link" @click="sign_out"> Sign out </p>
        <p v-if="!authenticated" @click="sign_in" class="hide-on-mobile link"> Sign in</p>
        <button id="show-on-mobile" @click="show_menu"><i class="bi bi-list"></i></button>
      </header>
      <div id="hamburger">
        <button><i class="bi bi-x"></i></button>
        <RouterLink to="/" id="item1" class="show-mobile">Home</RouterLink>
        <div id="item2" class="show-mobile" @click="show_profile('mobile')">
          <p id="profile-header" v-if="authenticated">Profile</p>
          <div id="profile-nav">
            <RouterLink class="profile-item border-bottom rounded-top" to="/details" >Details</RouterLink>
            <RouterLink class="profile-item border-bottom" to="/">Orders</RouterLink>
            <RouterLink class="profile-item border-bottom" to="/">Cart</RouterLink>
            <RouterLink class="profile-item rounded-bottom" to="/">Wishlist</RouterLink>
          </div>
        </div>
        <RouterLink to="/" id="item3" class="show-mobile">Help</RouterLink>
        <div id="item4" class="show-mobile">
          <p id="settings-header" @click="show_settings('mobile')">Settings</p>
          <div id="settings-mobile">
            <div id="theme" class="setting">
              <label for="">Theme</label>
              <div id="toggle" @click="(event) => toggle_theme('click', event)">
                <div id="circle">
                </div>
              </div>
            </div>
            <div id="currency" class="setting">
              <label for="">Currency</label>
              <select id="currency-dropdown" v-model="currency_setting" @change="update_setting('currency', currency_setting)">
                <option v-for="currency in ['USD', 'GBP', 'EUR']" :key="currency" :value="currency">
                  {{ currency }}
                </option>
              </select>
            </div>
            <div id="mode" class="setting">
              <label for="">Mode</label>
              <select id="currency-dropdown" v-model="mode_setting" @change="update_setting('mode', mode_setting)">
                <option v-for="mode in ['buyer', 'seller']" :key="mode" :value="mode">
                  {{ mode }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <RouterLink to="/" id="item5" class="show-mobile link">Sign out</RouterLink>
      </div>
      <RouterView />
   </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { RouterLink, RouterView } from 'vue-router'
  import type { Resource, User } from './types';
  import { useUserStore } from './stores/user';
  import { useResourcesStore } from './stores/resources';
  import { useUsersStore } from './stores/users';
  export default defineComponent({
    components: { RouterView },
    data(): { currency_setting: string, mode_setting: string, authenticated: boolean } { return {
        currency_setting : 'GBP',
        mode_setting: 'buyer',
        authenticated: false
      }
    },
    async mounted(): Promise<void> {
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
      if (userData.user === 'unauthenticated') {
        let header: HTMLHeadingElement = document.getElementById('main-header') as HTMLHeadingElement
        header.style.gridTemplateColumns = '1fr 1fr 0fr 2fr 1fr 0fr 1fr'
      } else {
        this.authenticated = true
        useUserStore().saveUser(userData.user)
        for (let cookie of document.cookie.split(';')) {
          const cookie_pair = cookie.split('=')
           if (cookie_pair[0] === 'csrftoken') {
              useUserStore().saveCsrf(cookie_pair[1])
           }
        }
        this.toggle_theme('mounted')
        this.currency_setting = this.user.currency
        this.mode_setting = this.user.mode
      }
      let getResourcesStore: Response = await fetch(`http://localhost:8000/api/resources/`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'X-CSRFToken' : useUserStore().csrf
          },
        })
        if (!getResourcesStore.ok) {
          console.error('Error getting resources')
          return
        }
        let resources: Resource[] = await getResourcesStore.json()
        useResourcesStore().saveResources(resources)
    },
    computed: {
      user(): User {
        return useUserStore().user
      }
    },
    methods: {
      go_home(): void {
        window.location.href = '/'
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
        this.go_home()
      },
      sign_in(): void {
        window.location.href = 'http://localhost:8000/login'
      },
      async update_setting(called_by: string, data: string): Promise<void> {
            let updateResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/${called_by}/`, {
              method: 'PUT',
              credentials: 'include',
              headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : useUserStore().csrf
              },
              body: JSON.stringify(data)
            })
            if (!updateResponse.ok) {
              console.error(called_by === 'theme' ? 'Error updating theme' : called_by === 'theme' ? 'Error updating currency' : 'Error updating mode')
              alert(called_by === 'theme' ? 'Error updating theme' : called_by === 'theme' ? 'Error updating currency' : 'Error updating mode')
              return
            }
            let userUpdateData: User = await updateResponse.json()
            useUserStore().saveUser(userUpdateData)
            useUsersStore().updateUser(userUpdateData)
            if (called_by === 'mode') {
              if (data === 'seller') {
                window.location.href = '/listings'
                return
              } else {
                window.location.href = '/'
              }
            } 
      },
      async toggle_theme(called_by: string, event?: Event): Promise<void> {
        const div = document.getElementById('app-vue')
        if (div) {
          const theme = div.firstElementChild
          if (theme) {
            if (called_by === 'mounted') {
              theme.id = useUserStore().user.theme_preference
            } else {
              theme.id = theme.id === 'light' ? 'dark' : 'light'
            }
            document.body.style.backgroundColor = theme.id === 'light' ? 'white' : '#807E7E'
            const logo: HTMLImageElement = document.getElementById('logo') as HTMLImageElement
            if (logo) {
              logo.src = theme.id === 'light' ? '/logo-light.svg' : '/logo-dark.svg'
            }
            if (called_by === 'mounted') return
            this.update_setting('theme', theme.id)
          }
        }
      },
      toggle_hamburger(): void {
        const hamburgerElement = document.getElementById('show-on-mobile')
        if (!hamburgerElement) return
        if (window.innerWidth >= 654) {
            hamburgerElement.style.display = 'none'
        } else {
          hamburgerElement.style.display = 'block'
        }
      }, 
      show_profile(called_by: string): void {
        const profileElement = document.getElementById('profile-nav')
        if (profileElement) {
          profileElement.classList.add('profile-nav-mobile')
          document.addEventListener('click', (event) => this.hide_profile(event, called_by))
        }
      },
      hide_profile(event: Event, called_by: string): void {
        const profileElement = document.getElementById('profile-nav')
        const mainProfileElement = document.getElementById(called_by === 'mobile' ? 'item2' : 'profile-div')
        if (profileElement && mainProfileElement && !mainProfileElement.contains(event.target as Node)) {
          profileElement.classList.remove('profile-nav-mobile')
          document.removeEventListener('click', (event) => this.hide_profile(event, called_by))
        }
      },
      show_settings(called_by: string): void {
        const settingElement = document.getElementById(called_by !== 'mobile' ? 'settings' :'settings-mobile')
        if (settingElement) {
          settingElement.classList.add('show-settings')
          document.addEventListener('click', (event) => this.hide_settings(event, called_by))
        }
      },
      hide_settings(event: Event, called_by: string): void {
        const settingElement = document.getElementById(called_by !== 'mobile' ? 'settings' :'settings-mobile')
        const mainSettingsElement = document.getElementById(called_by !== 'mobile' ? 'main-settings' : 'item4')
        if (settingElement && mainSettingsElement && !mainSettingsElement.contains(event.target as Node)) {
          settingElement.classList.remove('show-settings')
          document.removeEventListener('click', (event) => this.hide_settings(event, called_by))
        }
      },
      hide_menu(event: Event): void {
        const hamburgerElement = document.getElementById('show-on-mobile')
        const menuElement = document.getElementById('hamburger')
        if (hamburgerElement && !hamburgerElement.contains(event.target as Node) && menuElement && !menuElement.contains(event.target as Node)) {
          hamburgerElement.style.display = 'block'
          menuElement.classList.remove('show-mobile')
          document.removeEventListener('click', this.hide_menu)
        }
      },
      show_menu(): void {
        const hamburgerElement = document.getElementById('show-on-mobile')
        const menuElement = document.getElementById('hamburger')
        if (hamburgerElement && menuElement) {
          hamburgerElement.style.display = 'none'
          menuElement.classList.add('show-mobile')
          document.addEventListener('click', this.hide_menu)
          window.addEventListener('resize', this.toggle_hamburger)
        }
      }
    }
  })
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
  @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css');
  
  body {
    overflow: hidden;
    position: relative;
  }

  #logo {
    height: 1.6rem;
    padding: 0;
    margin: 0;
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

  #app-vue a:hover, #settings-header:hover, #profile-header:hover {
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

  #settings-header:hover, #profile-header:hover {
    cursor: pointer;
  }

  #dark #settings-header, #dark #profile-header {
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

  #show-on-mobile, .show-mobile { 
    display: none;
  }

  #hamburger {
    position: absolute;
    top: 0;
    right: -8rem;
    grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
    place-items: center;
    border-radius: 0.5rem;
    transition: 0.5s ease;
  }

  #hamburger button {
    position: absolute;
    color: rgb(236, 99, 99);
    border: none;
    background: none;
    right: 6rem;
  }

  #hamburger button:hover {
    color: red;
  }

  #hamburger button i {
    font-size: 2rem;
  }

  #main-settings {
    position: relative;
  }

  #settings {
    position: absolute;
    top: -11rem;
    right: -4rem;
    display: flex;
    flex-direction: column;
    background-color: #D9D9D9;
    border-radius: 0.5rem;
    transition: 0.5s ease;
  }

  #item4 #settings-mobile {
    position: absolute;
    top: -17rem;
    right: 6.5rem;
    display: flex;
    flex-direction: column;
    background-color: #D9D9D9;
    border-radius: 0.5rem;
    transition: top 0.5s ease;
  }

  .show-settings {
    top: 0rem;
    margin-top: 13.3rem;
  }
  
  #item4 .show-settings {
    top: 0rem;
    margin-top: 15.3rem;
  }

  #dark #settings {
    color: black;
  }

  #theme, #currency {
    border-bottom: 0.1rem solid white;
  }

  #dark #theme, #dark #currency {
    border-bottom: 0.1rem solid darkgray;
  }

  .setting {
    display: flex;
    align-items: center;
    gap: 2rem;
    padding: 0.5rem;
  }

  .setting label {
    width: 3rem;
  }

  .setting select {
    border-radius: 1rem;
    height: 1.9rem;
    width: 4.5rem;
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
    padding-left: 0.2rem;
  }

  #toggle {
    position: relative;
    height: 1.6rem;
    width: 4.4rem;
    background-color: white;
    border-radius: 1rem;
  }

  #circle {
    position: absolute;
    height: 1.3rem;
    width: 1.3rem;
    border-radius: 1rem;
    top: 0.14rem;
    transform: translateX(1%);
    left: 0.4rem;
    background-color: yellow;
    transition: transform 0.5s ease;
  }

  #dark #circle {
    background-color: darkblue;
  }

  #dark #circle {
    transform: translateX(180%);
  }

  #toggle:hover {
    background-color: rgb(245, 245, 245);
  }

  #profile-nav {
    position: absolute;
    display: flex;
    flex-direction: column;
    background-color: #D9D9D9;
    border-radius: 0.5rem;
    align-items: center;
    top: -13rem;
    right: -2.5rem;
    opacity: 0;
  }

  .profile-nav-mobile {
    top: 2.3rem !important;
    right: 6rem;
    opacity: 1 !important;
    transition: opacity 0.4s ease;
  }
  
  #item2 #profile-nav {
    top: 0.3rem;
    right: 2rem;
    opacity: 100%;
  }

  #item2 .profile-nav-mobile {
    /* right: 6.2rem !important; */
    right: 10rem !important;
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
  @media (min-width: 1110px) {
    #app-vue input {
      width: 30rem;
    }
  }

  @media (min-width: 1667px) {
    #app-vue input {
      width: 40rem;
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

    #dark #item1, #dark #item2, #dark #item3, #dark #item4 {
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

    #show-on-mobile {
      display: block;
      border: none;
      background: none;
    }

    #dark #show-on-mobile {
      color: white;
    }

    #show-on-mobile i {
      font-size: 1.5rem;
    }

    .hide-on-mobile {
      display: none;
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
