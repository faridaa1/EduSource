<template>
    <div id="settings-container" v-if="Object.keys(user).length > 0">
        <p id="settings-header">Settings</p>
        <div id="settings">
            <div id="theme" class="setting">
                <label>Theme</label>
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
                <label>Mode</label>
                <select id="currency-dropdown" v-model="mode_setting" @change="update_setting('mode', mode_setting)">
                    <option v-for="mode in ['buyer', 'seller']" :key="mode" :value="mode">
                    {{ mode }}
                    </option>
                </select>   
            </div>
        </div>
        <Error v-if="error" message="Please try updating the setting again." @close-error="error=false" />
    </div>
    <div v-else>
        <Loading />
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent } from 'vue';
    import { useUserStore } from '@/stores/user';
    import type { User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    import Loading from '@/components/user experience/loading/Loading.vue';
    import Error from '@/components/user experience/error/Error.vue';
    export default defineComponent({
      components: { Loading, Error },
      data(): { currency_setting: string, mode_setting: string, error: boolean } { return {
          currency_setting : 'GBP',
          mode_setting: 'buyer',
          error: false,
        }
      },
      mounted(): void {
            this.currency_setting = this.user.currency
            this.mode_setting = this.user.mode
      },
      computed: {
        user(): User {
          return useUserStore().user
        }
      },
      watch: {
        user(): void {
            this.currency_setting = this.user.currency
            this.mode_setting = this.user.mode
        }
      },
      methods: {
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
                this.error = true
                return
            }
            let userUpdateData: User = await updateResponse.json()
            useUserStore().saveUser(userUpdateData)
            useUsersStore().updateUser(userUpdateData)
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
        }
    })
</script>
  
  <style>

    #settings-header {
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }

    #settings-container {
        padding: 1rem;
    }

    #settings {
        display: flex;
        flex-direction: column;
    }
  
    #dark #settings {
        color: black;
    }
  
    #theme, #currency {
        border-bottom: 0.1rem solid #ebebeb;
    }
  
    #dark #theme, #dark #currency {
        border-bottom: 0.1rem solid darkgray;
    }
  
    .setting { 
        display: flex;
        align-items: center;
        gap: 2rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    #dark #settings-container, #dark .setting label {
        color: white !important;
    }
  
    .setting label {
        width: 4.5rem;
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
      background-color: #f5f5f5;
      border-radius: 1rem;
      border: 0.01rem solid rgb(48, 48, 48);
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
      cursor: pointer;
    }

    select:hover {
        cursor: pointer;
    }
  </style>
  