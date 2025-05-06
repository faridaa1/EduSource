import { defineStore } from 'pinia';
import type { Resource, Review } from '../types';

// Global store to access data and methods relating to all resources

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
        getResource(name: string): Resource | {} {
           const resource = this.resources.find(resource => resource.name === name)
           if (!resource) return {}
           return resource
        },
        addResoureReview(review: Review): void {
            const target_resource: Resource | undefined = this.resources.find(resource => resource.id === review.resource)
            if (target_resource) {
                target_resource.reviews.push(review)
                const temp_resources = this.resources.map(resource => resource.id === review.resource ? target_resource : resource)
                this.resources = temp_resources
            }
        },
        editResource(old_resource: Resource, new_resource: Resource): void {
            this.resources = this.resources.map(resource => resource.id === new_resource.id ? new_resource : resource.id === old_resource.id ? old_resource : resource)
        },
        updateResource(new_resource: Resource): void {
            this.resources = this.resources.map(resource => resource.id === new_resource.id ? new_resource : resource)
        },
    }
})