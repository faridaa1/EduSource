import { defineStore } from 'pinia';
import type { Resource, Review } from '../types';

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
        },
        getResource(name: string): Resource | {} {
           const resource = this.resources.find(resource => resource.name === name)
           if (!resource) return {}
           return resource
        },
        addResoureReview(review: Review): void {
            this.resources.find(resource => resource.id === review.resource)?.reviews.push(review)
        },
        editResoureReview(review: Review, oldResourceId: number): void {
            const resource = this.resources.find(resource => resource.id === review.resource)
            if (resource) {
                const old_review = resource.reviews.find(review => review.id === review.id)
                if (old_review) {
                    if (resource.id === old_review.resource) {
                        // Updating resource
                        Object.assign(old_review, review)
                    } 
                } else {
                    // Adding review to new resource
                    resource.reviews.push(review)
                    const oldResource = this.resources.find(resource => resource.id === oldResourceId)
                    if (oldResource) {
                        const reviews_minus_old = oldResource.reviews.filter(review => review.id !== review.id)
                        oldResource.reviews = reviews_minus_old
                    }
                }
            }
        },
        removeReview(deletedReview: Review): void {
            const resource =  this.resources.find(resource => resource.id === deletedReview.resource)
            if (resource) {
                resource.reviews = resource.reviews.filter(review => review.id !== deletedReview.id)
            }
        },
    }
})