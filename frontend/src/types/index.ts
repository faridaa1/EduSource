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
    listings: Resource[];
    cart: Cart;
    wishlist: Wishlist;
}

export interface Resource {
    id: number,
    name: string,
    description: string,
    height: number,
    width: number,
    weight: number,
    price: number,
    stock: number,
    estimated_delivery_time: number,
    subject: string,
    author: string,
    self_made: boolean,
    is_draft: boolean,
    page_start: number,
    page_end: number,
    height_unit: 'cm' | 'm' | 'in',
    width_unit: 'cm' | 'm' | 'in',
    image1: string,
    image2: string,
    video: string,
    weight_unit: 'kg' | 'ml' | 'L' | 'oz' | 'mg' | 'lb',
    price_currency: 'EUR' | 'GBP' | 'USD',
    estimated_delivery_units: 'day' | 'minute' | 'hour' | 'month' | 'week',
    type: 'Textbook' | 'Notes' | 'Stationery',
    rating: number,
    colour: 'Black' | 'Red' | 'Yellow' | 'Pink' | 'Purple' | 'Green' | 'Blue' | 'White' | 'Orange' | 'Brown' | 'Grey',
    source: 'AI' | 'Internet' | 'None',
    condition: 'New' | 'Used',
    media: 'Online' | 'Paper',
    delivery_option: 'Delivery' | 'Collection',
    user: number,
    reviews: Review[],
    upload: string,
    unique: boolean
}

export interface Review {
    id: number,
    resource: number,
    user: number,
    title: string,
    review: string,
    rating: number,
    upload_date: string,
    image: string,
    video: string,
}

export interface Cart {
    id: number,
    resources: {
        id: number,
        number: number,
        resource: number
    }[]
    items: number,
    total: number
}

export interface Wishlist {
    id: number,
    resources: Resource[],
    items: number,
    total: number
}

export interface CartResource {
    id: number,
    resource: number
    number: number
}

export interface WishlistResource {
    id: number,
    resource: number
}