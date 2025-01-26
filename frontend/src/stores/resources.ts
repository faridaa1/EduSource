import { defineStore } from 'pinia';
import type { Resource, User } from '../types';

export const useResourcesStore = defineStore('resources', {
    state: (): { resources: Resource[]} => ({
        resources: [] as Resource[],
    }),
    actions: {
        saveResources(resources: Resource[]): void {
            this.resources = resources
        },
        addResource(resource: Resource): void {
            this.resources.push(resource)
        },
        removeResource(id: number): void {
            this.resources = this.resources.filter(resource => resource.id !== id)
        },
        updateResorce(resource: Resource): void {
            let old_resource = this.resources.find(resource => resource.id === resource.id) 
            if (old_resource) {
                Object.assign(old_resource, resource)
            }
        }
    }
})