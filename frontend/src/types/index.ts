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
    placed_orders: Order[];
    sold_orders: Order[];
    cart: Cart;
    subjects: Subject[];
    messages: Messages[];
    wishlist: Wishlist;
    exchanges: Exchange[];
}

export interface Subject {
    id: number,
    name: string,
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
    allow_delivery: boolean,
    allow_collection: boolean,
    allow_return: boolean,
    user: number,
    last_edited: string,
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
    resources: {
        id: number,
        resource: number
    }[]
    items: number,
    total: number
}

export interface Exchange {
    id: number,
    status1: 'Pending' | 'Rejected' | 'Accepted',
    status2: 'Pending' | 'Rejected' | 'Accepted',
    user1: number,
    user2: number,
    resource1: number,
    resource2: number,
    resource1_number: number,
    resource2_number: number,
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

export interface Order {
    id: number,
    status: 'Placed' | 'Requested Return' | 'Processing' | 'Refund Rejected' | 'Cancelled' | 'Dispatched' | 'Complete' | 'Being Returned' | 'Refunded',
    buyer: number,
    seller: number,
    resources: OrderResource[],
    estimated_delivery_date: string,
    delivery_image: string,
    date: string,
    return_method: 'Delivery' | 'Collection',
    return_reason: string,
    is_exchange: boolean
}

export interface OrderResource {
    id: number,
    resource: number,
    number: number,
    for_return: boolean,
    number_for_return: number,
}

export interface Messages {
    id: number,
    user1: number,
    user2: number,
    user1_seen: number,
    user2_seen: number,
    last_edited: string,
    messages: Message[]
}

export interface Message {
    id: number,
    user: number,
    message: string,
    sent: string
}