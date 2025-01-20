<template>
  <div id="app-vue">
    <div id="light">
      <header>
        <img id='logo' src="/logo-light.svg" alt="EduSource" width="125" height="125" v-pre/>
        <RouterLink to="/" class="hide-on-mobile">Home</RouterLink>
        <RouterLink to="/" class="hide-on-mobile">Profile</RouterLink>
        <div id="search-div">
          <input type="text" placeholder="Search">
          <button><i class="bi bi-search search-icon"></i></button>
        </div>
        <RouterLink to="/" class="hide-on-mobile">Help</RouterLink>
        <p class="hide-on-mobile">Settings</p>
        <RouterLink to="/" class="hide-on-mobile">Sign out</RouterLink>
        <button id="show-on-mobile" @click="show_menu"><i class="bi bi-list"></i></button>
      </header>
      <div id="hamburger">
        <RouterLink to="/" id="item1" class="hide-on-mobile">Home</RouterLink>
        <RouterLink to="/" id="item2" class="hide-on-mobile">Profile</RouterLink>
        <RouterLink to="/" id="item3" class="hide-on-mobile">Help</RouterLink>
        <p id="item4" class="hide-on-mobile">Settings</p>
        <RouterLink to="/" id="item5" class="hide-on-mobile">Sign out</RouterLink>
      </div>
      <RouterView />
   </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, shallowReactive } from 'vue';
  import { RouterLink, RouterView } from 'vue-router'
  import type { User } from './types';
  export default defineComponent({
    components: { RouterView },
    async mounted(): Promise<void> {
      let userResponse: Response = await fetch('http://localhost:8000/api/user/', {
        method: 'GET',
        credentials: 'include'
      })
      let userData: { user: User | 'unauthenticated' } = await userResponse.json()
      if (!(userData.user === 'unauthenticated')) {
        let theme_preference = userData.user.theme_preference
        console.log(document.getElementById('light'))
      }
    },
    methods: {
      hide_menu(event: Event): void {
        const hamburgerElement = document.getElementById('show-on-mobile')
        const menuElement = document.getElementById('hamburger')
        if (hamburgerElement && !hamburgerElement.contains(event.target as Node) && menuElement) {
          hamburgerElement.style.display = 'block'
          menuElement.style.display = 'none'
          document.removeEventListener('click', this.hide_menu)
        }
      },
      show_menu(): void {
        const hamburgerElement = document.getElementById('show-on-mobile')
        const menuElement = document.getElementById('hamburger')
        if (hamburgerElement && menuElement) {
          hamburgerElement.style.display = 'none'
          menuElement.style.display = 'block'
          document.addEventListener('click', this.hide_menu)
        }
      }
    }
  })
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
  @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css');
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
    padding-bottom: 0.8rem;
  }

  #app-vue #light header {
    background-color: #0DCAF0;
  }

  #app-vue a {
    text-decoration: none;
  }

  #app-vue a:hover {
    text-decoration: underline;
  }

  #app-vue #light a {
    color: black;
  }

  #app-vue #search-div {
    position: relative;
  }

  #app-vue input {
    background-color: rgb(224, 222, 222);
    border-radius: 0.4rem;
    border: none;
    padding: 0.3rem;
    width: 100%;
  }

  #app-vue input:focus {
    background-color: white;
  }

  #app-vue #search-div button {
    position: absolute;
    top: 0.2rem;
    right: 0.5rem;
    border: none;
    background-color: transparent;
  }

  #app-vue #search-div i:hover {
    cursor: pointer;
    color: #0DCAF0;
  }

  #show-on-mobile, #hamburger, #item1, #item2, #item3, #item4, #item5 { 
    display: none;
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
    .hide-on-mobile {
      display: none;
    }

    #app-vue header {
      display: grid;
      grid-template-columns: 1fr 2fr 1fr;
      place-items: center;
      padding-top: 0.8rem;
      padding-bottom: 0.8rem;
    }

    #app-vue #hamburger {
      position: absolute;
      right: 0;
      top: 0;
      grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
      place-items: center;
      border-radius: 0.5rem;
      background-color: darkgray;
    }

    #item1, #item2, #item3, #item4, #item5 {
      display: block;
      width: 6rem;
      text-align: center;
      align-self: center;
      padding-top: 0.5rem;
      padding-bottom: 0.5rem;
    }

    #item1, #item2, #item3, #item4 {
      border-bottom: 0.1rem solid white;
    }

    #item1:hover, #item2:hover, #item3:hover, #item4:hover, #item5:hover {
      background-color: #0DCAF0;
    }

    #item5:hover {
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

    #show-on-mobile i {
      font-size: 1.5rem;
    }
  }
</style>
