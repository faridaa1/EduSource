import { defineStore } from 'pinia';
import type { User } from '../types';

export const useUsersStore = defineStore('users', {
    state: (): { users: User[]} => ({
        users: [] as User[],
    }),
    actions: {
        updateUsers(users: User[]): void {
            this.users = users
        },
        updateUser(updated_user: User): void {
            this.users.map(user => user.id === updated_user.id ? updated_user : user)
        },
    }
})