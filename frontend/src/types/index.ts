export interface User {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    username: string;
    phone_number: string;
    rating: number;
    description: string;
    theme_preference: 'light' | 'dark';
    mode: 'buyer' | 'seller';
    currency: 'USD' | 'GBP' | 'EUR';
    address_line_one: string;
    address_second_line: string;
    city: string;
    postcode: string;
}