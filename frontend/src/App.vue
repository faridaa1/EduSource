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
        <div class="hide-on-mobile">
          Settings
          <div id="settings">
            <div id="theme" class="setting">
              <label for="">Theme</label>
              <div id="toggle" @click="toggle_theme">
                <div id="circle">
                </div>
              </div>
            </div>
            <div id="currency" class="setting">
              <label for="">Currency</label>
            </div>
            <div id="mode" class="setting">
              <label for="">Mode</label>
              <select name="" id="" value="">
                <option value=""></option>
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
    async mounted(): Promise<void> {
      let userResponse: Response = await fetch('http://localhost:8000/api/user/', {
        method: 'GET',
        credentials: 'include'
      })
      let userData: { user: User | 'unauthenticated' } = await userResponse.json()
      if (userData.user === 'unauthenticated') {
      } else {
        let theme_preference = userData.user.theme_preference
        // useUserStore().saveCsrf()
        console.log(document.cookie)
        useUserStore().saveUser(userData.user)
      }
    },
    methods: {
      toggle_theme(event: Event): void {
        const div = document.getElementById('app-vue')
        if (div) {
          const theme = div.firstElementChild
          if (theme) {
            theme.id = theme.id === 'light' ? 'dark' : 'light'
            document.body.style.backgroundColor = theme.id === 'light' ? 'white' : '#807E7E'
            document.body.style.color = theme.id === 'light' ? 'black' : 'white'
            const logo: HTMLImageElement = document.getElementById('logo') as HTMLImageElement
            if (logo) {
              logo.src = theme.id === 'light' ? '/logo-light.svg' : '/logo-dark.svg'
            }
          }
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
    background-color: rgb(224, 222, 222);
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
    right: -6rem;
    grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
    place-items: center;
    border-radius: 0.5rem;
    transition: 0.5s ease;
    overflow: hidden;
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

  .setting {
    display: flex;
    width: 10rem;
    gap: 2rem;
  }

  #toggle {
    position: relative;
    height: 1.5rem;
    width: 3.5rem;
    background-color: white;
    border-radius: 1rem;
  }

  #circle {
    position: absolute;
    height: 1.1rem;
    width: 1.1rem;
    border-radius: 1rem;
    top: 0.23rem;
    transform: translateX(0);
    left: 0.4rem;
    background-color: yellow;
    transition: transform 0.5s ease;
  }

  #dark #circle {
    background-color: darkblue;
  }

  #dark #circle {
    transform: translateX(155%);
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

    #app-vue #light .show-mobile {
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

    .hide-on-mobile {
      display: none;
    }
  }
</style>
