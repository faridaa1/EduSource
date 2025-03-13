import { defineStore } from 'pinia';

export const useURLStore = defineStore('URL', {
    state: (): { url: string } => ({
        url: '',
    }),
    actions: {
        saveURL(url: string): void {
            this.url = url
        },
    }
})