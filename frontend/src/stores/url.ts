import { defineStore } from 'pinia';

export const useURLStore = defineStore('URL', {
    state: (): { url: string } => ({
        url: '',
    }),
    actions: {
        saveURL(url: 'localhost' | 'deploy'): void {
            if (url === 'localhost') {
                this.url = 'http://localhost:8000'
            } else {
                this.url = 'https://edusource-edusource.apps.a.comp-teach.qmul.ac.uk'
            }
        }
    }
})