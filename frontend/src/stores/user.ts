import { defineStore } from 'pinia';
import type { User } from '../types';

export const useUserStor = defineStore('user', {
    state: (): { user: User, csrf: string} => ({
        user: {} as User,
        csrf: ''
    }),
    actions: {
        saveUser(user: User): void {
            this.user = user
        },
        saveCsrf(csrf: string): void {
            this.csrf = csrf
        }
    }
})