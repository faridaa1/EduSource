<template>
  <div id="app-vue">
    <div id="light">
      <header>
        <img id='logo' src="/logo-light.svg" alt="EduSource" width="125" height="125" v-pre/>
        <RouterLink to="/" class="hide-on-mobile">Home</RouterLink>
        <RouterLink to="/" class="hide-on-mobile">Profile</RouterLink>
        <div id="search-div">
          <input type="text" placeholder="Search">
          <button><i class="bi bi-search"></i></button>
        </div>
        <RouterLink to="/" class="hide-on-mobile">Help</RouterLink>
        <div id="main-settings" class="hide-on-mobile">
          Settings
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
        <RouterLink to="/" class="hide-on-mobile">Sign out</RouterLink>
        <button id="show-on-mobile" @click="show_menu"><i class="bi bi-list"></i></button>
      </header>
      <div id="hamburger">
        <button><i class="bi bi-x"></i></button>
        <RouterLink to="/" id="item1" class="show-mobile">Home</RouterLink>
        <RouterLink to="/" id="item2" class="show-mobile">Profile</RouterLink>
        <RouterLink to="/" id="item3" class="show-mobile">Help</RouterLink>
        <p id="item4" class="show-mobile">Settings</p>
        <RouterLink to="/" id="item5" class="show-mobile">Sign out</RouterLink>
      </div>
      <RouterView />
   </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { RouterLink, RouterView } from 'vue-router'
  import type { User } from './types';
  import { useUserStore } from './stores/user';
  export default defineComponent({
    components: { RouterView },
    data(): { currency_setting: string, mode_setting: string } { return {
        currency_setting : 'GBP',
        mode_setting: 'buyer'
      }
    },
    async mounted(): Promise<void> {
      let userResponse: Response = await fetch('http://localhost:8000/api/user/', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'X-CSRFToken' : useUserStore().csrf
        }
      })
      let userData: { user: User | 'unauthenticated' } = await userResponse.json()
      if (userData.user === 'unauthenticated') {
      } else {
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
    },
    computed: {
      user(): User {
        return useUserStore().user
      }
    },
    methods: {
      async update_setting(called_by: string, data: string): Promise<void> {
        let updateResponse: Response = await fetch(`http://localhost:8000/api/user/settings/${useUserStore().user.id}/${called_by}/`, {
              method: 'PUT',
              credentials: 'include',
              headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : useUserStore().csrf
              },
              body: JSON.stringify(data)
            })
            if (!updateResponse.ok) {
              console.error(called_by === 'theme' ? 'Error updating theme' : 'Error updating currency')
              alert(called_by === 'theme' ? 'Error updating theme' : 'Error updating currency')
              return
            }
            let userUpdateData: User = await updateResponse.json()
            useUserStore().user.theme_preference = userUpdateData.theme_preference
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
            document.body.style.color = theme.id === 'light' ? 'black' : 'white'
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
      hide_menu(event: Event): void {
        const hamburgerElement = document.getElementById('show-on-mobile')
        const menuElement = document.getElementById('hamburger')
        if (hamburgerElement && !hamburgerElement.contains(event.target as Node) && menuElement) {
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

  #app-vue a:hover {
    text-decoration: underline;
  }

  #app-vue #dark a {
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
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .setting {
    display: flex;
    align-items: center;
    gap: 2rem;
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
    }

    #item2 {
      grid-column: 3;
      grid-row: 2;
    }

    #item3 {
      grid-column: 3;
      grid-row: 3;
    }

    #item4 {
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
</style>
