import { defineStore } from 'pinia';

// Storing URL globally to be accessed by different components

export const useURLStore = defineStore('URL', {
    state: (): { url: string } => ({
        url: '',
    }),
    actions: {
        saveURL(url: 'localhost' | 'deploy'): void {
            if (url === 'localhost') {
                this.url = 'http://localhost:8000'
            } else {
                this.url = 'https://edutest-edusource-test.apps.a.comp-teach.qmul.ac.uk'
                // this.url = 'https://edusource-edusource.apps.a.comp-teach.qmul.ac.uk'
            }
        }
    }
})