<template>
    <div id="details">
        <form ref="detailsForm" id="detailsForm" @submit.prevent="validate('details')">
            <h1>Account Details</h1>
            <div class="form-item">
                <label for="">Email</label>
                <input required type="email" autocomplete="username" v-model="email" @input="validate_email(false)">
                <div class="button-container">
                    <button id="email-save" type="submit" class="save" v-if="editingEmail" @click="validate_email(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="email-cancel" type="button" class="cancel" v-if="editingEmail" @click="editingEmail = false; email = user.email"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div class="form-item">
                <label for="">Username</label>
                <input required id="username" type="text" autocomplete="username" v-model="username" @input="validate_username(false)">
                <div class="button-container">
                    <button id="username-save" class="save" type="submit" v-if="editingUsername" @click="validate_username(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="username-cancel" type="button" class="cancel" v-if="editingUsername" @click="editingUsername = false; username = user.username"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div id="password-item">
                <div id="passwords">
                    <div class="form-item">
                        <label for="">Password</label>
                        <div class="button-container">
                            <input id="pass" type="password" placeholder="************" autocomplete="current-password" v-model="password" @input="validate_password(false)">
                            <button type="button" class="edit see" v-if="editingPassword && !show_pass" @click="toggle_password('password', true)"><i class="bi bi-eye"></i></button>
                            <button type="button" class="edit see" v-if="editingPassword && show_pass" @click="toggle_password('password', false)"><i class="bi bi-eye-slash-fill"></i></button>
                        </div>
                    </div>
                    <div class="form-item" v-if="editingPassword">
                        <label for="">New Password</label>
                        <div class="button-container">
                            <input required id="new_pass" type="password" autocomplete="new-password" v-model="new_password" @input="validate_password(false)">
                            <button type="button" class="edit see" v-if="editingPassword && !show_new_pass" @click="toggle_password('new-password', true)"><i class="bi bi-eye"></i></button>
                            <button type="button" class="edit see" v-if="editingPassword && show_new_pass" @click="toggle_password('new-password', false)"><i class="bi bi-eye-slash-fill"></i></button>
                        </div>
                    </div>
                    <div class="form-item" v-if="editingPassword">
                        <label for="">Re-enter New Password</label>
                        <div class="button-container">
                            <input required id="re_pass" type="password" autocomplete="new-password" v-model="re_password" @input="validate_password(false)">
                            <button type="button" class="edit see" v-if="editingPassword && !show_re_pass" @click="toggle_password('re-password', true)"><i class="bi bi-eye"></i></button>
                            <button type="button" class="edit see" v-if="editingPassword && show_re_pass" @click="toggle_password('re-password', false)"><i class="bi bi-eye-slash-fill"></i></button>
                        </div>
                    </div>
                </div>
                <div class="buttons">
                    <button id="password-save" class="save" type="submit" v-if="editingPassword" @click="validate_password(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="password-cancel" type="button" class="cancel" v-if="editingPassword" @click="clear_passwords"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div class="form-item">
                <label for="">First Name</label>
                <input required id="first_name" type="text" v-model="first_name" @input="validate_name(false)">
                <div class="button-container">
                    <button id="name-save" class="save" type="submit" v-if="editingFirstName" @click="validate_name(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="name-cancel" type="button" class="cancel" v-if="editingFirstName" @click="editingFirstName = false; first_name = user.first_name"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div class="form-item">
                <label for="">Last Name</label>
                <input required id="last_name" type="text" v-model="last_name" @input="validate_surname(false)">
                <div class="button-container">
                        <button id="surname-save" class="save" type="submit" v-if="editingLastName" @click="validate_surname(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="surname-cancel" type="button" class="cancel" v-if="editingLastName" @click="editingLastName = false; last_name = user.last_name"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div class="form-item">
                <label for="">Phone Number</label>
                <input required id="number" type="text" v-model="phone_number" @input="validate_number(false)">
                <div class="button-container">
                    <button id="number-save" class="save" type="submit" v-if="editingPhoneNumber" @click="validate_number(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="number-cancel" type="button" class="cancel" v-if="editingPhoneNumber" @click="editingPhoneNumber = false; phone_number = user.phone_number"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div id="description-item" class="form-item" >
                <label for="">Seller Description</label>
                <div id="description-input">
                    <textarea name="" id="description" v-model="description" @input="validate_description(false)"></textarea>
                </div>
                <div id="description-buttons">
                    <button id="description-save" class="save" type="submit" v-if="editingDescription" @click="validate_description(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="description-cancel" type="button" class="cancel" v-if="editingDescription" @click="editingDescription = false; description = user.description"><i class="bi bi-x"></i></button>
                </div>
            </div>
        </form>
        <div>
            <h1>Subject Preferences</h1>
            <div id="subject-preferences" class="form-item">
                <div id="semantic-search">
                    <input type="text" id="sub-pref" @input="semantic_subject" @click="semantic_subject">
                    <i class="bi bi-search" @click="save_subject()"></i>
                </div>
                <div class="options" v-if="show_subjects">
                    <div class="option" v-for="subject in search_preferences">
                        <p @click="save_subject(subject)">{{ subject }}</p>
                    </div>
                </div>
                <div id="user-subjects" v-if="user.subjects.length > 0">
                    <div id="subject-item" v-for="subject in user.subjects.sort((a,b) => b.id - a.id)" @click="delete_subject(subject.id)">
                        <div>
                            <p>{{ subject.name }}</p>
                            <i class="bi bi-x"></i>
                        </div>
                        <hr v-if="subject !== user.subjects[user.subjects.length-1]">
                    </div>
                </div>
            </div>
        </div>
        <form id="addressForm" ref="addressForm" @submit.prevent="validate('address')">
            <h1>Address</h1>
            <div class="form-item">
                <label>Address Line One</label>
                <input required id="line1" type="text" v-model="line1" @input="validate_line1(false)">
                <div class="button-container">
                    <button id="line1-save" class="save" type="submit" v-if="editingLine1" @click="validate_line1(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="line1-cancel" type="button" class="cancel" v-if="editingLine1" @click="editingLine1 = false; line1 = user.address_line_one"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div class="form-item">
                <label>Address Line Two</label>
                <input required id="line2" type="text" v-model="line2" @input="validate_line2(false)">
                <div class="button-container">
                    <button id="line2-save" class="save" type="submit" v-if="editingLine2" @click="validate_line2(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="line2-cancel" type="button" class="cancel" v-if="editingLine2" @click="editingLine2 = false; line2 = user.address_second_line"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div class="form-item">
                <label>City</label>
                <input required id="city" type="text" v-model="city" @input="validate_city(false)">
                <div class="button-container">
                    <button id="city-save" class="save" type="submit" v-if="editingCity" @click="validate_city(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="city-cancel" type="button" class="cancel" v-if="editingCity" @click="editingCity = false; city = user.city"><i class="bi bi-x"></i></button>
                </div>
            </div>
            <div class="form-item">
                <label>Postcode</label>
                <input required id="postcode" type="text" v-model="postcode" @input="validate_postcode(false)">
                <div class="button-container">
                    <button id="postcode-save" class="save" type="submit" v-if="editingPostcode" @click="validate_postcode(true)"><i class="bi bi-floppy-fill"></i></button>
                    <button id="postcode-cancel" type="button" class="cancel" v-if="editingPostcode" @click="editingPostcode = false; postcode = user.postcode"><i class="bi bi-x"></i></button>
                </div>
            </div>
        </form>
    </div>
</template>

<script lang="ts">
    import { useUserStore } from '@/stores/user';
    import { defineComponent } from 'vue';
    import type { User } from '@/types';
    import { useUsersStore } from '@/stores/users';
    export default defineComponent({
        data(): {
            show_subjects: boolean,
            subject: string,
            email: string,
            username: string,
            password: string,
            new_password: string,
            re_password: string,
            first_name: string,
            search_preferences: string[],
            last_name: string,
            phone_number: string,
            description: string,
            line1: string,
            line2: string,
            city: string,
            postcode: string,
            editingEmail: boolean,
            editingUsername: boolean,
            editingPassword: boolean,
            editingFirstName: boolean,
            editingLastName: boolean,
            editingPhoneNumber: boolean,
            editingDescription: boolean,
            editingLine1: boolean,
            editingLine2: boolean,
            editingCity: boolean,
            editingPostcode: boolean,
            show_pass: boolean,
            show_new_pass: boolean,
            show_re_pass: boolean
        } { return {
            email: '',
            username: '',
            password: '',
            new_password: '',
            show_subjects: false,
            re_password: '',
            first_name: '',
            last_name: '',
            phone_number: '',
            description: '',
            line1: '',
            line2: '',
            city: '',
            postcode: '',
            editingEmail: false,
            editingUsername: false,
            editingPassword: false,
            editingFirstName: false,
            editingLastName: false,
            editingPhoneNumber: false,
            editingDescription: false,
            editingLine1: false,
            editingLine2: false,
            editingCity: false,
            editingPostcode: false,
            show_pass: false,
            show_new_pass: false,
            search_preferences: [],
            subject: '',
            show_re_pass: false
        }},
        methods: {
            async delete_subject(id: number): Promise<void> {
                const response: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/subjects/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'Content-Type' : 'application/json',
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(id)
                })
                if (!response.ok) {
                    return
                }
                const user: User = await response.json()
                useUsersStore().updateUser(user)
                useUserStore().saveUser(user)
            },
            async save_subject(subject? : string): Promise<void> {
                const search: HTMLInputElement = document.getElementById('sub-pref') as HTMLInputElement
                if (!search) return
                this.show_subjects = false;
                if ((!subject && search.value.trim() === '') || (subject && this.user.subjects.map(subject => subject.name).includes(subject)) || (!subject && this.user.subjects.map(subject => subject.name).includes(search.value))) {
                    search.value = ''
                    this.subject = ''
                    return
                } 
                this.update_details('subjects', subject ? subject : search.value.trim())
                search.value = ''
                this.subject = ''
                
            },
            async semantic_subject(): Promise<void> {
                const search: HTMLInputElement = document.getElementById('sub-pref') as HTMLInputElement
                if (!search) return
                this.show_subjects = true
                this.subject = search.value
                const searchResults: Response = await fetch(`http://localhost:8000/api/semantic-search-subjects/`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type' : 'application/json',
                        'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(search.value)
                })
                if (!searchResults.ok) {
                    return
                }
                const search_preferences: string[] = await searchResults.json()
                this.search_preferences = search_preferences.filter(search_preferences => !this.user.subjects.map(subject => subject.name).includes(search_preferences))
                let unique_subjects: string[] = []
                let new_array: string[] = []
                for (let subject of this.search_preferences) {
                    if (unique_subjects.includes(subject)) continue
                    new_array.push(subject)
                    unique_subjects.push(subject)
                }
            },
            async validate_line2(submit: boolean): Promise<void> {
                this.clear_details('address')
                const address_line_two: HTMLInputElement = document.getElementById('line2') as HTMLInputElement
                if (this.line2 !== this.user.address_second_line) {
                    this.editingLine2 = true
                    if (this.line2.length === 0) {
                        address_line_two.setCustomValidity('Cannot be empty')
                        return
                    }
                    if (!(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/.test(this.line2))) {
                        address_line_two.setCustomValidity('No special characters allowed')
                        return
                    }
                    address_line_two.setCustomValidity('')
                    if (submit) {
                        this.update_details('address_line_two', this.line2)
                        this.editingLine2 = false
                    }
                    return
                } 
                address_line_two.setCustomValidity('')
                this.editingLine2 = false
            },
            async validate_city(submit: boolean): Promise<void> {
                this.clear_details('address')
                const city: HTMLInputElement = document.getElementById('city') as HTMLInputElement
                if (this.city !== this.user.city) {
                    this.editingCity = true
                    if (this.city.length === 0) {
                        city.setCustomValidity('Cannot be empty')
                        return
                    }
                    if (!(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/.test(this.city))) {                     
                        city.setCustomValidity('No special characters allowed')
                        return
                    }
                    city.setCustomValidity('')
                    if (submit) {
                        this.update_details('city', this.city)
                        this.editingCity = false
                    }
                    return
                } 
                city.setCustomValidity('')
                this.editingCity = false
            },
            async validate_postcode(submit: boolean): Promise<void> {
                this.clear_details('address')
                const postcode: HTMLInputElement = document.getElementById('postcode') as HTMLInputElement
                if (this.postcode !== this.user.postcode) {
                    this.editingPostcode = true
                    if (this.postcode.length === 0) {
                        postcode.setCustomValidity('Cannot be empty')
                        return
                    }
                    if (!(/^[A-Za-z0-9]{5,7}$/.test(this.postcode))) {
                        postcode.setCustomValidity('Enter 5-7 character postcode without spaces')
                        return
                    }
                    postcode.setCustomValidity('')
                    if (submit) {
                        this.update_details('postcode', this.postcode)
                        this.editingPostcode = false
                    }
                    return
                } 
                postcode.setCustomValidity('')
                this.editingPostcode = false
            },
            async validate_line1(submit: boolean): Promise<void> {
                this.clear_details('address')
                const address_line_one: HTMLInputElement = document.getElementById('line1') as HTMLInputElement
                if (this.line1 !== this.user.address_line_one) {
                    this.editingLine1 = true
                    if (this.line1.length === 0) {
                        address_line_one.setCustomValidity('Cannot be empty')
                        return
                    }
                    if (!(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/.test(this.line1))) {
                        address_line_one.setCustomValidity('No special characters allowed')
                        return
                    }
                    address_line_one.setCustomValidity('')
                    if (submit) {
                        this.update_details('address_line_one', this.line1)
                        this.editingLine1 = false
                    }
                    return
                } 
                address_line_one.setCustomValidity('')
                this.editingLine1 = false
            },
            async validate_description(submit: boolean): Promise<void> {
                this.clear_details('details')
                const description: HTMLInputElement = document.getElementById('description') as HTMLInputElement
                if (this.description !== this.user.description) {
                    this.editingDescription = true
                    if (this.description.length === 0) {
                        description.setCustomValidity('Description cannot be empty')
                        return
                    }
                    if (!(/^\S+( \S+)*$/.test(this.description))) {
                        description.setCustomValidity('Only one space between words')
                        return
                    }
                    description.setCustomValidity('')
                    if (submit) {
                        this.update_details('description', this.description)
                        this.editingDescription = false
                    }
                    return
                } 
                description.setCustomValidity('')
                this.editingDescription = false
            },
            async validate_number(submit: boolean): Promise<void> {
                this.clear_details('details')
                const number: HTMLInputElement = document.getElementById('number') as HTMLInputElement
                this.editingPhoneNumber = true
                if (!submit) {
                    number.setCustomValidity('')
                    return
                }
                if (this.phone_number.length === 0) {
                    number.setCustomValidity('Phone number cannot be empty')
                    return
                } else if (!(/^07(\d{8,9})$/.test(this.phone_number))) {
                    number.setCustomValidity('Must be 10 or 11 digit number starting with 07')
                    return
                }
                let correctNumber: Promise<string> = this.attribute_existence('number', this.phone_number)
                if (await correctNumber === 'true') {
                    number.setCustomValidity('Account already exists with this phone number')
                    number.reportValidity()
                    return
                } else if (await correctNumber === 'error') {
                    console.error('Error saving phone number')
                    confirm('Error saving phone number')
                    return
                }
                number.setCustomValidity('')
                if (submit) {
                    this.update_details('number', this.phone_number)
                }
                this.editingPhoneNumber = false
            },
            async validate_surname(submit: boolean): Promise<void> {
                this.clear_details('details')
                const name: HTMLInputElement = document.getElementById('last_name') as HTMLInputElement
                if (this.last_name !== this.user.last_name) {
                    this.editingLastName = true
                    if (this.last_name.length === 0) {
                        name.setCustomValidity('Name cannot be empty')
                        return
                    }
                    if (!(/^[a-zA-Z ]+$/.test(this.last_name))) {
                        name.setCustomValidity('Name cannot contain special characters')
                        return
                    }
                    name.setCustomValidity('')
                    if (submit) {
                        this.update_details('surname', this.last_name)
                        this.editingLastName = false
                    }
                    return
                } 
                name.setCustomValidity('')
                this.editingLastName = false
            },
            async validate_name(submit: boolean): Promise<void> {
                this.clear_details('details')
                const name: HTMLInputElement = document.getElementById('first_name') as HTMLInputElement
                if (this.first_name !== this.user.first_name) {
                    this.editingFirstName = true
                    if (this.first_name.length === 0) {
                        name.setCustomValidity('Name cannot be empty')
                        return
                    }
                    if (!(/^[a-zA-Z ]+$/.test(this.first_name))) {
                        name.setCustomValidity('Name cannot contain special characters')
                        return
                    }
                    name.setCustomValidity('')
                    if (submit) {
                        this.update_details('name', this.first_name)
                        this.editingFirstName = false
                    }
                    return
                } 
                name.setCustomValidity('')
                this.editingFirstName = false
            },
            clear_passwords(): void {
                this.editingPassword = false
                this.password = ''
                this.re_password = ''
                this.new_password = ''
            },
            toggle_password(field: string, show_password: boolean): void {
                if (field === 'password') {
                    const passwordElement: HTMLInputElement = document.getElementById('pass') as HTMLInputElement
                    if (passwordElement) {
                        passwordElement.type = show_password === true ? 'text' : 'password'
                        this.show_pass = show_password === true ? true : false
                    }
                } else if (field === 'new-password') {
                    const passwordElement: HTMLInputElement = document.getElementById('new_pass') as HTMLInputElement
                    if (passwordElement) {
                        passwordElement.type = show_password === true ? 'text' : 'password'
                        this.show_new_pass = show_password === true ? true : false
                    }
                } if (field === 're-password') {
                    const passwordElement: HTMLInputElement = document.getElementById('re_pass') as HTMLInputElement
                    if (passwordElement) {
                        passwordElement.type = show_password === true ? 'text' : 'password'
                        this.show_re_pass = show_password === true ? true : false
                    }
                } 
            },
            validate(caller: string): void {
                const detailsForm: HTMLFormElement = caller === 'details' ? this.$refs.detailsForm as HTMLFormElement : this.$refs.addressForm as HTMLFormElement
                detailsForm.checkValidity()
            },
            async validate_password(submit : boolean): Promise<void> {
                this.editingPassword = true
                this.clear_details('details')
                const password: HTMLInputElement = document.getElementById('pass') as HTMLInputElement
                const new_password: HTMLInputElement = document.getElementById('new_pass') as HTMLInputElement
                const re_password: HTMLInputElement = document.getElementById('re_pass') as HTMLInputElement
                if (!password || !new_password || !re_password) {
                    return
                }
                if (!submit) {
                    password.setCustomValidity('')
                    new_password.setCustomValidity('')
                    re_password.setCustomValidity('')
                    return
                }
                if (this.password.length === 0) {
                    password.setCustomValidity('Password cannot be empty')
                    new_password.setCustomValidity('')
                    return
                }
                if (this.new_password.length === 0) {
                    new_password.setCustomValidity('Password cannot be empty')
                    return
                } else if (/\s/.test(this.new_password)) {
                    new_password.setCustomValidity('Password cannot contain spaces')
                    return
                } else if (this.new_password.length < 8 || this.new_password.length > 15) {
                    new_password.setCustomValidity('Password must be between 8 to 15 characters long')
                    return
                } else if (this.new_password !== this.re_password) {
                    re_password.setCustomValidity('Both new passwords must match')
                    return
                } else if (this.new_password === this.username) {
                    new_password.setCustomValidity('Password cannot be the same as username')
                    return
                } else if (this.new_password === this.email) {
                    new_password.setCustomValidity('Password cannot be the same as email')
                    return
                }
                let correctPassword: Promise<string> = this.attribute_existence('password', this.password)
                if (await correctPassword === 'false') {
                    password.setCustomValidity('Incorrect password')
                    password.reportValidity()
                    return
                } else if (await correctPassword === 'error') {
                    console.error('Error saving password')
                    confirm('Error saving password')
                    return
                }
                if (submit) {
                    this.update_details('password', this.new_password)
                }
                password.setCustomValidity('')
                new_password.setCustomValidity('')
                re_password.setCustomValidity('')
                this.editingPassword = false
            },
            async validate_username(submit : boolean): Promise<void> {
                this.clear_details('details')
                const username: HTMLInputElement = document.getElementById('username') as HTMLInputElement
                if (this.username !== this.user.username) {
                    this.editingUsername = true
                    if (this.username.length === 0) {
                        username.setCustomValidity('Username cannot be empty')
                        return
                    }
                    if (!(/^[a-zA-Z0-9]+$/.test(this.username))) {
                        if (! /\s/.test(this.username)) {
                            username.setCustomValidity('Username cannot contain special characters')
                            return
                        }
                        username.setCustomValidity('Username cannot contain spaces')
                        username.reportValidity()
                        return
                    }
                    let usernameExists: Promise<string> = this.attribute_existence('username', this.username)
                    if (await usernameExists === 'true') {
                        username.setCustomValidity('Account with this username exists')
                        return
                    } else if (await usernameExists === 'error') {
                        console.error('Error saving username')
                        confirm('Error saving username')
                        return
                    }
                    username.setCustomValidity('')
                    if (submit) {
                        this.update_details('username', this.username)
                    }
                    return
                } 
                username.setCustomValidity('')
                this.editingUsername = false
            }, 
            clear_details(form: string) {
                const detailsForm: HTMLFormElement = form === 'details' ? this.$refs.detailsForm as HTMLFormElement : this.$refs.addressForm as HTMLFormElement
                const inputs = detailsForm.querySelectorAll('input, textarea')
                inputs.forEach(input => {
                    const element = input as HTMLInputElement | HTMLTextAreaElement
                    element.setCustomValidity('')
                    // element.reportValidity()
                })
            },
            async validate_email(submit : boolean): Promise<void> {
                this.clear_details('details')
                const detailsForm: HTMLFormElement = this.$refs.detailsForm as HTMLFormElement
                const email: HTMLInputElement = detailsForm.querySelector('input[type="email"]') as HTMLInputElement
                if (this.email !== this.user.email) {
                    this.editingEmail = true
                    if (this.email.length === 0) {
                        email.setCustomValidity('Email cannot be empty')
                        return
                    }
                    if (!(/\.[a-zA-Z-0-9][a-zA-Z-0-9]+$/).test(this.email)) {
                        email.setCustomValidity('Email ending is invalid')
                        return
                    } 
                    let emailExists: Promise<string> = this.attribute_existence('email', this.email)
                    if (await emailExists === 'true') {
                        email.setCustomValidity('Account with this email exists')
                        email.reportValidity()
                        return
                    } else if (await emailExists === 'error') {
                        console.error('Error saving email')
                        confirm('Error saving email')
                        return
                    }
                    if (submit) {
                        this.update_details('email', this.email)
                    }
                    email.setCustomValidity('')
                    return
                } 
                email.setCustomValidity('')
                this.editingEmail = false
            },
            async attribute_existence(attribute: string, data: string): Promise<string> {
                const saveButton: HTMLButtonElement = attribute === 'email' ? document.getElementById('email-save') as HTMLButtonElement : attribute === 'username' ? document.getElementById('username-save') as HTMLButtonElement : attribute === 'password' ? document.getElementById('password-save') as HTMLButtonElement : document.getElementById('number-save') as HTMLButtonElement 
                const cancelButton: HTMLButtonElement = attribute === 'email' ? document.getElementById('email-cancel') as HTMLButtonElement : attribute === 'username' ? document.getElementById('username-cancel') as HTMLButtonElement : attribute === 'password' ? document.getElementById('password-cancel') as HTMLButtonElement : document.getElementById('number-cancel') as HTMLButtonElement
                if (saveButton) {
                    console.log('save disab')
                    saveButton.disabled = true
                } 
                if (cancelButton) {
                    console.log('hicancelbye')
                    cancelButton.disabled = true
                }
                let userResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/check/${attribute}/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                    'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(data)
                })  
                if (userResponse.ok) {
                    if (saveButton) {
                        saveButton.disabled = false
                    } 
                    if (cancelButton) {
                        cancelButton.disabled = false
                    }
                    let attributeExists: boolean = await userResponse.json()
                    return attributeExists ? 'true' : 'false'
                }
                return 'error'
            },
            async update_details(attribute: string, data: string): Promise<void> {
                const saveButton: HTMLButtonElement = 
                    attribute === 'email' ? document.getElementById('email-save') as HTMLButtonElement 
                    : attribute === 'username' ? document.getElementById('username-save') as HTMLButtonElement 
                    : attribute === 'password' ? document.getElementById('password-save') as HTMLButtonElement 
                    : attribute === 'name' ? document.getElementById('name-save') as HTMLButtonElement 
                    : attribute === 'surname' ? document.getElementById('surname-save') as HTMLButtonElement 
                    : attribute === 'description' ? document.getElementById('description-save') as HTMLButtonElement
                    : attribute === 'address_line_one' ? document.getElementById('line1-save') as HTMLButtonElement
                    : attribute === 'address_line_two' ? document.getElementById('line2-save') as HTMLButtonElement
                    : attribute === 'city' ? document.getElementById('city-save') as HTMLButtonElement
                    : document.getElementById('postcode-save') as HTMLButtonElement
                const cancelButton: HTMLButtonElement = 
                    attribute === 'email' ? document.getElementById('email-cancel') as HTMLButtonElement 
                    : attribute === 'username' ? document.getElementById('username-cancel') as HTMLButtonElement 
                    : attribute === 'password' ? document.getElementById('password-cancel') as HTMLButtonElement 
                    : attribute === 'name' ? document.getElementById('name-cancel') as HTMLButtonElement 
                    : attribute === 'surname' ? document.getElementById('surname-cancel') as HTMLButtonElement 
                    : attribute === 'description' ? document.getElementById('description-cancel') as HTMLButtonElement
                    : attribute === 'address_line_one' ? document.getElementById('line1-cancel') as HTMLButtonElement
                    : attribute === 'address_line_two' ? document.getElementById('line2-cancel') as HTMLButtonElement
                    : attribute === 'city' ? document.getElementById('city-cancel') as HTMLButtonElement
                    : document.getElementById('postcode-cancel') as HTMLButtonElement
                    if (saveButton) {
                    saveButton.disabled = true
                } 
                if (cancelButton) {
                    cancelButton.disabled = true
                }
                let userResponse: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/${attribute}/`, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                    'X-CSRFToken' : useUserStore().csrf
                    },
                    body: JSON.stringify(data)
                })
                if (userResponse.ok) {
                    const user: User = await userResponse.json()
                    useUsersStore().updateUser(user)
                    useUserStore().saveUser(user)
                    
                    if (saveButton) {
                        saveButton.disabled = false
                    } 
                    if (cancelButton) {
                        cancelButton.disabled = false
                    }
                    if (attribute === 'email') {
                        this.editingEmail = false
                    } else if (attribute === 'username') {
                        this.editingUsername = false
                    } else if (attribute === 'password') {
                        for (let cookie of document.cookie.split(';')) {
                            const cookie_pair = cookie.split('=')
                            if (cookie_pair[0] === 'csrftoken') {
                                useUserStore().saveCsrf(cookie_pair[1])
                            }
                        }
                        this.clear_passwords()
                    } else if (attribute === 'name') {
                        this.editingFirstName = false
                    } else if (attribute === 'surname') {
                        this.editingLastName = false
                    } else if (attribute === 'address_line_one') {
                        this.editingLine1 = false
                    } else if (attribute === 'address_line_two') {
                        this.editingLine2 = false
                    } else if (attribute === 'city') {
                        this.editingCity = false
                    } else if (attribute === 'postcode') {
                        this.editingPostcode = false
                    }
                } else {
                    console.error(`Error updating ${attribute}`)
                    confirm(`Error updating ${attribute}`)
                }
            }
        },
        computed: {
            user(): User {
                let user: User = useUserStore().user
                this.email = user.email
                this.username = user.username
                this.first_name = user.first_name
                this.last_name = user.last_name
                this.phone_number = user.phone_number
                this.description = user.description
                this.line1 = user.address_line_one
                this.line2 = user.address_second_line
                this.city = user.city
                this.postcode = user.postcode
                return user
            }
        },
        watch: {
            user(new_user) {
                this.email = new_user.email
                this.username = new_user.username
                this.first_name = new_user.first_name
                this.last_name = new_user.last_name
                this.phone_number = new_user.phone_number
                this.description = new_user.description
                this.line1 = new_user.address_line_one
                this.line2 = new_user.address_second_line
                this.city = new_user.city
                this.postcode = new_user.postcode
            }
        },
        mounted(): void {
            document.addEventListener('click', (event) => {
                if (this.show_subjects && !((event.target as HTMLDivElement).id === 'sub-pref')) {
                    this.subject = ''
                    this.show_subjects = false
                }
            })
            document.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' && this.show_subjects && ((event.target as HTMLDivElement).id === 'sub-pref')) {
                    this.save_subject()
                }
            })
            const form: HTMLFormElement = this.$refs.detailsForm as HTMLFormElement
            const addressForm: HTMLFormElement = this.$refs.addressForm as HTMLFormElement
            if (form) {
                form.addEventListener('keydown', (event) => {
                    if (event.key === 'Enter') {
                        event.preventDefault()
                    }
                })
            }
            if (addressForm) {
                addressForm.addEventListener('keydown', (event) => {
                    if (event.key === 'Enter') {
                        event.preventDefault()
                    }
                })
            }
        }
    })
</script>

<style scoped>
    #user-subjects {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
        width: 100%;
        overflow: auto;
        max-height: 10rem;
        border-radius: 0.2rem;
        border: 0.01rem solid darkgray;
    }

    #user-subjects #subject-item {
        display: flex;
        flex-direction: column;
        padding: 0.2rem;
        gap: 0.5rem;
    }

    #subject-item div {
        display: flex;
        padding: 0.2rem;
        align-items: center;
        justify-content: space-between;
    }

    hr {
        background-color: #f3f3f3;
        width: 97%;
    }

    #user-subjects i {
        color: red;
    }

    #user-subjects:hover {
        cursor: pointer;
    }

    #user-subjects #subject-item div:hover {
        background-color: red;
        color: white;
    }

    #semantic-search {
        display: flex;
        align-items: center;
        background-color: #D9D9D9;
        border-radius: 0.5rem;
    }

    #semantic-search input {
        border-top-right-radius: 0rem;
        border-bottom-right-radius: 0rem;
    }

    #semantic-search i:hover {
        background-color: #b7b5b5;
        cursor: pointer;
    }

    #semantic-search i {
        border-top-right-radius: 0.5rem;
        border-bottom-right-radius: 0.5rem;
        padding: 0.25rem;
    }

    #details {
        margin-left: 3rem;
        margin-top: 3rem;
    }

    h1 {
        margin-bottom: 2rem;
    }

    form {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    form label {
        width: 9rem;
    }

    input, textarea {
        width: 14rem !important;
        border-radius: 0.5rem;
    }

    .form-item {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }

    .save, .cancel, .edit {
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
    }

    .save, .cancel {
        color: white;
    }

    .save {
        background-color: green;
        padding: 0.3rem;
    }

    .cancel {
        background-color: red;
        padding-top: 0.1rem;
        padding-left: 0.1rem;
        padding-right: 0.1rem;
        padding-bottom: 0.1rem;
    }

    .edit {
        background-color: #0DCAF0;
        color: white;
        padding: 0.3rem;
    }

    .edit:hover {
        background-color: #177183;
    }

    #dark .edit:hover {
        background-color: rgb(87, 87, 87);
    }

    #dark .edit {
        background-color: black;
        color: white;
    }

    .button-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .cancel i {
        font-size: 1.3rem;
    }
    
    .save:hover {
        background-color: rgb(105, 214, 105);
    }

    .cancel:hover {
        background-color: rgb(255, 131, 131);
    }

    textarea { 
        padding: 0.3rem;
        background-color: #D9D9D9;
    }

    textarea:focus { 
        background-color: white;
    }

    #password-item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 0.5rem;
    }

    #passwords {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .buttons {
        display: flex;
        gap: 0.5rem;
        align-self: flex-start;
        margin-inline-start: 9.5rem;
    }

    .see, .edit {
        margin-left: 0.5rem;
    }

    #description-item {
        flex-direction: column;
        align-self: flex-start;
    }

    #description-item label {
        margin-right: auto;
    }

    #description-item textarea {
        width: 23.4rem !important;
        height: 5rem;
    }

    #details {
        display: flex;
        gap: 4rem;
        justify-content: center;
        margin: 5rem;
    }

    #details h1 {
        margin: 0;
    }

    #description-input {
        display: flex;
        margin-right: auto;
    }

    #description-buttons {
        display: flex;
        gap: 0.5rem;
        margin-left: 0.4rem;
        align-self: flex-end;
    }

    #subject-preferences {
        margin-top: 2rem;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: start;
        margin-left: auto;
        gap: 1rem;
    }

    .options {
        position: absolute;
        top: 1.8rem;
        display: flex;
        flex-direction: column;
        background-color: #D9D9D9;
        width: 100%;
        max-height: 10rem;
        border: 0.01rem solid darkgray;
        border-radius: 0.1rem;
        overflow-y: scroll;
    }

    .option {
        padding: 0.2rem;
    }

    .option:hover {
        cursor: pointer;
        text-decoration: underline;
        border-radius: 0.5rem;
    }

    /* Responsive design */
    @media (max-width: 1397px) {
        #details {
            flex-direction: column;
            width: 30.5rem;
            margin-top: 2rem;
            justify-self: center;
            justify-content: unset !important;
            overflow: auto;
            height: 90vh;
        }

        #user-subjects, .options {
            width: 50%;
        }

        #description-item textarea {
            width: 27.5rem !important;
        }

        form {
            gap: 1rem;
        }
    }


    @media (max-width: 556px) {
        h1, #subject-preferences {
            margin-left: 2rem !important;
        }

        #user-subjects, .options {
            width: 16rem;
        }

        #details {
            width: 90% !important;
            overflow: auto;
            height: 88vh !important;
            justify-content: unset;
        }

        .form-item {
            flex-direction: column;
            align-items: start;
            margin-left: 2rem;
        }

        .buttons {
            margin-top: 0.5rem;
            margin-inline-start: 2rem;
        }

        #description-item textarea {
            width: 18rem !important;
        }

        #password-item {
            gap: 0;
        }

        #description-buttons {
            align-self: flex-start !important;
        }
    }
</style>
