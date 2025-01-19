<template>
  <header>
    <img id='logo' src="/logo-light.svg" alt="EduSource" width="125" height="125" v-pre/>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/">Profile</RouterLink>
        <RouterLink to="/">Help</RouterLink>
        <RouterLink to="/">Settings</RouterLink>
        <RouterLink to="/">Sign out</RouterLink>
      </nav>
  </header>
  <RouterView />
</template>

<script lang="ts">
    import { defineComponent } from 'vue';
    import { RouterLink, RouterView } from 'vue-router'
    import type { User } from './types';
    export default defineComponent({
      components: { RouterView },
      async mounted(): Promise<void> {
          let userResponse: Response = await fetch('/api/user', {
            method: 'GET',
            credentials: 'include'
          })
          let userData: { user: User } = await userResponse.json()
          console.log(userData)
      }
    })
</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css');
    #logo {
        height: 4rem;
        padding:0;
        margin: 0;
    }
    
    header {
      display: flex;
      background-color: #0DCAF0;
      border-radius: 1rem;
    }
</style>
