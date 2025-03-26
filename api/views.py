import datetime
from django.utils import timezone
import json
from django.core.mail import send_mail
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate
from django.db.models import Avg, Sum
from django.contrib import auth
import torch
from .forms import SignupForm, AddressForm, LoginForm
from .models import Cart, CartResource, Exchange, Messages, Order, OrderResource, Resource, Review, SearchHistory, SearchHistoryItem, Subject, User, Address, Wishlist, WishlistResource, Message
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Initialising models to be used
sentiment_analysis_bert = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
semantic_search_model = SentenceTransformer("all-MiniLM-L6-v2") 
bert = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment", max_length=512, truncation=True)
chatbot_tokeniser = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill") 
chatbot_model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")


def frontend(request: HttpRequest) -> HttpResponse:
    """Ensures frontend routing when URLs is not captured by api URLS"""
    return render(request, 'api/index.html')


def signup(request: HttpRequest) -> HttpResponse:
    """Handling user sign up"""
    if request.method == 'POST':
        signup_form: SignupForm = SignupForm(request.POST)
        address_form: AddressForm = AddressForm(request.POST)
        if signup_form.is_valid() and address_form.is_valid():
            signup_data: dict[str: str] = signup_form.cleaned_data
            address_data: dict[str: str] = address_form.cleaned_data
            user : User = User.objects.create_user(
                email=signup_data['email'],
                first_name=signup_data['first_name'],
                last_name=signup_data['last_name'],
                phone_number=signup_data['phone_number'],
                username=signup_data['username'].lower(),
                password=signup_data['password'],
                theme_preference=signup_data['theme_preference'],
                mode=signup_data['mode'],
                description=signup_data['description'],
                cart=Cart.objects.create(),
                wishlist=Wishlist.objects.create(),
            )
            user.search_history=SearchHistory.objects.create(user=user)
            Address.objects.create(
                first_line=address_data['first_line'],
                second_line=address_data['second_line'],
                city=address_data['city'],
                postcode=address_data['postcode'],
                user=user
            )
            send_mail('EduSource - Account Created',
            f'Hi {user.first_name}, Welcome to EduSource!\n\nThanks for signing up.\n\nThis is to confirm we have the correct email registered to your account. There is no need to take action.\n\nEnjoy EduSource!', 'edusource9325@gmail.com', [user.email])
            authenticated_user: User | None = authenticate(request, username=signup_data['username'], password=signup_data['password'])
            if authenticated_user:
                auth.login(request, authenticated_user)
            if 'localhost' in request.build_absolute_uri():
                return redirect('http://localhost:5173/details')
            return redirect('https://edusource-edusource.apps.a.comp-teach.qmul.ac.uk/details')
        return render(request, 'api/signup.html', {'signup_form' : signup_form, 'address_form' : address_form})
    return render(request, 'api/signup.html', {'signup_form' : SignupForm(), 'address_form' : AddressForm()})


def login(request: HttpRequest) -> HttpResponse:
    """Handling user log in"""
    if request.method == 'POST' and not b'localhost:5173' in request.body:
        login_form: LoginForm = LoginForm(request.POST)
        if login_form.is_valid():
            login_data: dict[str, str] = login_form.cleaned_data
            if '@' in login_data['user']:
                try:
                    user: User = User.objects.get(email=login_data['user'])
                    authenticated_user: User | None = authenticate(request, username=user.username, password=login_data['password'])
                except:
                    authenticated_user: None = None
            else:
               authenticated_user: User | None = authenticate(request, username=login_data['user'], password=login_data['password'])
            if authenticated_user:
                auth.login(request, authenticated_user)
                if authenticated_user.mode == 'buyer':
                    if 'localhost' in request.build_absolute_uri():
                        return redirect('http://localhost:5173/')
                    return redirect('https://edusource-edusource.apps.a.comp-teach.qmul.ac.uk/')
                if 'localhost' in request.build_absolute_uri():
                    return redirect('http://localhost:5173/listings')
                return redirect('https://edusource-edusource.apps.a.comp-teach.qmul.ac.uk/listings')
            login_form.add_error(None, 'Invalid email or password' if '@' in login_data['user'] else 'Invalid username or password')
        return render(request, 'api/login.html', {'login_form' : login_form})
    return render(request, 'api/login.html', {'login_form' : LoginForm()})


def signout(request: HttpRequest) -> JsonResponse:
    """Handling user log out"""
    try:
        auth.logout(request)
    except:
        pass
    return JsonResponse({})


def user(request: HttpRequest) -> JsonResponse:
    """Return user details if user is authenticated"""
    if request.user.is_authenticated:
        return JsonResponse({'user' : User.objects.get(username=request.user.username).as_dict()})
    return JsonResponse({'user' : 'unauthenticated'})


def users(request: HttpRequest) -> JsonResponse:
    """Return all database users"""
    return JsonResponse([user.as_dict() for user in User.objects.all()], safe=False)


def resources(request: HttpRequest) -> JsonResponse:
    """Returning all database resources"""
    return JsonResponse([resource.as_dict() for resource in Resource.objects.all()], safe=False)


def currency_conversion(request: HttpRequest, id: int, from_currency: str, to_currency: float) -> JsonResponse:
    """Implementing currency conversion"""
    resource: Resource = get_object_or_404(Resource, id=id)
    initial_value: Money = Money(resource.price, to_currency)
    return JsonResponse({'new_price': str(convert_money(initial_value, from_currency))})


def set_resource_rating(resource_id: int) -> float:
    """Update resource rating based on average sentiment"""
    average_rating = Review.objects.filter(resource=resource_id).aggregate(Avg('rating'))['rating__avg']
    return average_rating if average_rating else 0.0


def update_seller_rating(user: User) -> None:
    """Ensuring seller rating is defined based on sentiment of reviews"""
    reviews = list(Review.objects.filter(resource__user__id=user.id).values_list('review', flat=True))
    stars = list(int(review['label'][0]) for review in bert(reviews))
    if len(stars) == 0:
        user.rating = 0
    else:
        user.rating = round(sum(stars) / len(stars), 1)
    user.save()


def review(request: HttpRequest, user: int, resource: int) -> JsonResponse:
    """Handling review creation and deltion"""
    if request.method == 'POST':
        """Creating new Review object"""
        resource: Resource = Resource.objects.get(id=resource)
        media = request.FILES
        data = request.POST
        review: Review = Review.objects.create(
            resource=resource,
            user=User.objects.get(id=user),
            title=data.get('title'),
            rating=data.get('stars'),
            review=data.get('description'),
            image=media.get('image') if media.get('image') else None,
            video=media.get('video') if media.get('video') else None,
        )
        review.save()
        resource.rating=set_resource_rating(resource.id)
        resource.save()
        update_seller_rating(review.resource.user)
        return JsonResponse({'resource': resource.as_dict(),
                            'users': [user.as_dict() for user in User.objects.all()]})
    if request.method == 'DELETE':
        """Deleting review"""
        review: Review = Review.objects.get(id=resource)
        resource: Resource = Resource.objects.get(id=review.resource.id)
        review.delete()
        resource.rating = set_resource_rating(resource.id)
        resource.save()
        update_seller_rating(review.resource.user)
        return JsonResponse({'resource': resource.as_dict(),
                            'users': [user.as_dict() for user in User.objects.all()]})
    return JsonResponse({})


def edit_review(request: HttpRequest, user: int, id: int, resource: int) -> JsonResponse:
    """Implementing review editing"""
    if request.method == 'POST':
        media = request.FILES
        data = request.POST
        user: User = User.objects.get(id=user)
        resource: Resource = Resource.objects.get(id=resource)
        review: Review = Review.objects.get(id=id)
        review.title = data.get('title')
        review.rating = data.get('stars')
        review.review = data.get('description')
        review.resource = resource
        if not media.get('image'):
            review.image = None
        elif not review.image or (media.get('image').name != review.image.name.split('/')[1]):
            review.image=media.get('image')
        if not media.get('video'):
            review.video = None
        elif not review.video or (media.get('video').name != review.video.name.split('/')[1]):
            review.video=media.get('video')
        review.upload_date = timezone.now()
        review.save()
        resource.rating = set_resource_rating(resource.id)
        resource.save()
        old_resource: Resource = Resource.objects.get(id=data.get('old_resource'))
        old_resource.rating = set_resource_rating(old_resource)
        old_resource.save()
        update_seller_rating(review.resource.user)
        return JsonResponse({'old_resource' : old_resource.as_dict(),
                             'new_resource' : resource.as_dict(),
                             'users' : [user.as_dict() for user in User.objects.all()],})
    return JsonResponse({})


def delete_account(request: HttpRequest, user: int) -> JsonResponse:
    """Facilitating account deletion"""
    if request.method == 'DELETE':
        user: User = get_object_or_404(User, id=user)
        send_mail('EduSource - Account Deletion',
            f'Hi {user.first_name},\n\nThis is to confirm your account deletion.\n\nThanks for using EduSource!', 'edusource9325@gmail.com', [user.email])
        user.delete()
    return JsonResponse({})

def user_details(request: HttpRequest, id: int, attribute: str) -> JsonResponse | Http404:
    """Defining PUT and DELETE request handling of user details"""
    user: User | Http404 = get_object_or_404(User, id=id)
    if request.method == 'PUT':
        """Update user details"""
        try:
            address: Address | Http404 = get_object_or_404(Address, user=user)
        except:
            address: Address = Address.objects.create(
                first_line='test',
                city='test',
                postcode='edusrc',
                user=user
            )
        if attribute == 'theme':
            user.theme_preference = json.loads(request.body)
        elif attribute == 'currency':
            user.currency = json.loads(request.body)
        elif attribute == 'mode':
            user.mode = json.loads(request.body)
        elif attribute == 'email':
            user.email = json.loads(request.body)
        elif attribute == 'username':
            user.username = json.loads(request.body)
        elif attribute == 'password':
            user.set_password(json.loads(request.body))
        elif attribute == 'name':
            user.first_name = json.loads(request.body)
        elif attribute == 'surname':
            user.last_name = json.loads(request.body)
        elif attribute == 'number':
            user.phone_number = json.loads(request.body)
        elif attribute == 'description':
            user.description = json.loads(request.body)
        elif attribute == 'address_line_one':
            address.first_line = json.loads(request.body)
        elif attribute == 'address_line_two':
            address.second_line = json.loads(request.body)
        elif attribute == 'city':
            address.city = json.loads(request.body)
        elif attribute == 'postcode':
            address.postcode = json.loads(request.body)
        elif attribute == 'subjects':
            Subject.objects.create(
                name=json.loads(request.body),
                user=user
            )
        user.save()
        address.save()
        if attribute == 'password':
            user: User | None = authenticate(request, username=user.username, password=json.loads(request.body))
            if user:
                auth.login(request, user)
        return JsonResponse(user.as_dict())
    elif request.method == 'DELETE':
        """Delete user preferred subject"""
        if attribute == 'subjects':
            Subject.objects.get(id=json.loads(request.body)).delete()
        return JsonResponse(user.as_dict())
    return JsonResponse('no user', safe=False)


def check_details(request: HttpRequest, id: int, attribute: str) -> JsonResponse:
    """Checking whether user exists to ensure unique IDs, and ensuring new password matches old password"""
    if request.method == 'PUT':
        if attribute == 'email':
            return JsonResponse(User.objects.filter(email=json.loads(request.body)).exists(), safe=False)
        elif attribute == 'username':
            return JsonResponse(User.objects.filter(username=json.loads(request.body)).exists(), safe=False)
        elif attribute == 'password':
            user: User = User.objects.get(id=id)
            return JsonResponse(user.check_password(json.loads(request.body)), safe=False)
        elif attribute == 'number':
            return JsonResponse(User.objects.filter(phone_number=json.loads(request.body)).exists(), safe=False)
    return JsonResponse(False)


def new_listing(request: HttpRequest, id: int) -> JsonResponse:
    """Defining POST, PUT and DELETE request handling for Listing"""
    data: dict[str, any] = request.POST
    media_data: dict[str, any] = request.FILES
    user: User = get_object_or_404(User, id=id)
    if request.method == 'DELETE':
        """Deleting listing"""
        resource: Resource = get_object_or_404(Resource, id=json.loads(request.body))
        resource.delete()
    if request.method == 'POST' and not data.get('id'):
        """Creating new listing"""
        resource: Resource = Resource.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            height=data.get('height'),
            width=data.get('width'),
            weight=data.get('weight'),
            price=data.get('price'),
            stock=data.get('stock'),
            estimated_delivery_time=data.get('estimated_number'),
            subject=data.get('subject'),
            author=data.get('author'),
            self_made=False if data.get('self_made') == 'false' else True,
            is_draft=False if data.get('is_draft') == 'false' else True,
            page_start=data.get('page_start'),
            page_end=data.get('page_end'),
            height_unit=data.get('height_unit'),
            width_unit=data.get('width_unit'),
            image1=media_data.get('image1'),
            image2=media_data.get('image2'),
            video=media_data.get('video'),
            weight_unit=data.get('weight_unit'),
            price_currency=data.get('price_currency'),
            estimated_delivery_units=data.get('estimated_units'),
            type=data.get('type'),
            colour=data.get('colour'),
            source=data.get('source'),
            condition=data.get('condition'),
            media=data.get('media'),
            unique=False if data.get('unique') == 'false' else True,
            allow_delivery=False if data.get('allow_delivery') == 'false' else True,
            allow_collection=False if data.get('allow_collection') == 'false' else True,
            allow_return=False if data.get('allow_return') == 'false' else True,
            user=user
        )
        return JsonResponse(resource.as_dict())
    if request.method == 'POST' and data.get('id'):
        """Editing prior listing"""
        resource: Resource = get_object_or_404(Resource, id=data.get('id'))
        resource.name=data.get('name')
        resource.description=data.get('description')
        resource.height=data.get('height')
        resource.width=data.get('width')
        resource.weight=data.get('weight')
        resource.price=data.get('price')
        resource.stock=data.get('stock')
        resource.estimated_delivery_time=data.get('estimated_number')
        resource.subject=data.get('subject')
        resource.author=data.get('author')
        resource.self_made=False if data.get('self_made') == 'false' else True
        resource.is_draft=False if data.get('is_draft') == 'false' else True
        resource.page_start=data.get('page_start')
        resource.page_end=data.get('page_end')
        resource.height_unit=data.get('height_unit')
        resource.width_unit=data.get('width_unit')
        if media_data.get('image1'):
            resource.image1=media_data.get('image1')
        if media_data.get('image2'):
            resource.image2=media_data.get('image2')
        if media_data.get('video'):
            resource.video=media_data.get('video')
        resource.weight_unit=data.get('weight_unit')
        resource.price_currency=data.get('price_currency')
        resource.estimated_delivery_units=data.get('estimated_units')
        resource.type=data.get('type')
        resource.colour=data.get('colour')
        resource.source=data.get('source')
        resource.condition=data.get('condition')
        resource.media=data.get('media')
        resource.delivery_option=data.get('delivery')
        resource.allow_delivery=False if data.get('allow_delivery') == 'false' else True
        resource.unique=False if data.get('unique') == 'false' else True
        resource.allow_collection=False if data.get('allow_collection') == 'false' else True
        resource.allow_return=False if data.get('allow_return') == 'false' else True
        resource.user=user
        resource.save()
        return JsonResponse(resource.as_dict())
    return JsonResponse({})


def sentiment_analysis(request: HttpRequest, resource: str) -> JsonResponse:
    if request.method == 'GET':
        """Returning resource review sentiment to allow ordering based on resource sentiment"""
        resources = Resource.objects.filter(name=resource)
        reviews = list(Review.objects.filter(resource__in=resources).values_list('review', flat=True))
        reviews_ids = list(Review.objects.filter(resource__in=resources).values_list('id', flat=True))
        scores = list(review['score'] for review in sentiment_analysis_bert(reviews))
        reviews_scores = dict(zip(reviews_ids, scores))
        return JsonResponse(reviews_scores, safe=False)
    return JsonResponse({})


def update_cart(request: HttpRequest, user: int, cart: int, resource: int) -> JsonResponse:
    """Implementing GET, POST, PUT and DELETE for Cart object"""
    user: User = get_object_or_404(User, id=user)
    if user.cart is None:
        user.cart = Cart.objects.create()
        user.save()
    if user.wishlist is None:
        user.wishlist = Wishlist.objects.create()
        user.save()
    if request.method == 'GET':
        """Returning cart"""
        for cart_resource in user.cart.cart_resource.all():
            # remove item from cart if resource is a draft or the user has added too much of the item to their basket
            resource_to_check: Resource = cart_resource.resource
            if resource_to_check.is_draft or (resource_to_check.stock < cart_resource.number):
                cart_resource.delete()
        return JsonResponse(user.cart.as_dict())
    elif request.method == 'POST':
        """Adding new item to cart"""
        resource: Resource = get_object_or_404(Resource, id=resource)
        cartResource: CartResource = CartResource.objects.create(
            resource=resource,
            number=1,
            cart=user.cart,
        )
        user.cart.items += 1
        user.cart.save()
        if WishlistResource.objects.filter(wishlist=user.wishlist, resource__name=resource.name).exists():
            object = WishlistResource.objects.filter(wishlist=user.wishlist, resource__name=resource.name).first()
            object.delete()
            user.wishlist.save()
        return JsonResponse({'resource': cartResource.as_dict(), 'cart': user.cart.as_dict(), 'wishlist': user.wishlist.as_dict()})
    elif request.method == 'PUT':
        """Updating number of items of a particular resource in cart"""
        cartResource: CartResource = get_object_or_404(CartResource, id=cart)
        if cartResource.resource.id != int(resource):
            cartResource.resource = Resource.objects.get(id=resource)
        if json.loads(request.body) > cartResource.resource.stock:
            cartResource.number = cartResource.resource.stock
        else:
            cartResource.number = json.loads(request.body)
        cartResource.save()
        user.cart.items = user.cart.cart_resource.all().aggregate(Sum('number'))['number__sum'] if user.cart.cart_resource.all().aggregate(Sum('number'))['number__sum'] else 0
        user.cart.save()
        return JsonResponse({'resource': cartResource.as_dict(), 'cart': user.cart.as_dict(), 'wishlist': user.wishlist.as_dict()})
    elif request.method == 'DELETE':
        """Deleting item from cart"""
        resource: CartResource = get_object_or_404(CartResource, id=cart)
        resource.delete()
        user.cart.items = user.cart.cart_resource.all().aggregate(Sum('number'))['number__sum'] if user.cart.cart_resource.all().aggregate(Sum('number'))['number__sum'] else 0
        user.cart.save()
        return JsonResponse({'resource': [], 'cart': user.cart.as_dict(), 'wishlist': user.wishlist.as_dict()})
    return JsonResponse({})


def get_cart(request: HttpRequest, user: int) -> JsonResponse:
    if request.method == 'GET':
        """Returning user cart"""
        user: User = get_object_or_404(User, id=user)
        if user.cart is None:
            user.cart = Cart.objects.create()
            user.save()
        return JsonResponse(user.cart.as_dict())
    return JsonResponse({})


def update_wishlist(request: HttpRequest, user: int) -> JsonResponse:
    """Defining POST, PUT and DELETE handling for user wishlist"""
    resource_id = json.loads(request.body)
    if request.method == 'POST':
        """Adding item to wishlist"""
        user: User = User.objects.get(id=user)
        if user.cart is None:
            user.cart = Cart.objects.create()
            user.save()
        if user.wishlist is None:
            user.wishlist = Wishlist.objects.create()
            user.save()    
        WishlistResource.objects.create(
            resource = Resource.objects.get(id=resource_id),
            wishlist=user.wishlist
        )
        user.wishlist.items +=1
        user.wishlist.save()
        return JsonResponse({ 'wishlist': user.wishlist.as_dict() }) 
    elif request.method == 'DELETE':
        """Removing item from wishlist"""
        user: User = User.objects.get(id=user)
        if user.cart is None:
            user.cart = Cart.objects.create()
            user.save()
        if user.wishlist is None:
            user.wishlist = Wishlist.objects.create()
            user.save()
        resource: WishlistResource = get_object_or_404(WishlistResource, resource=Resource.objects.get(id=resource_id))
        user.wishlist.items -= 1
        user.wishlist.save()
        resource.delete()
        return JsonResponse({ 'wishlist': user.wishlist.as_dict() }) 
    elif request.method == 'PUT':
        """Defining move of item from wishlist to cart"""
        user: User = User.objects.get(id=user)
        if user.cart is None:
            user.cart = Cart.objects.create()
            user.save()
        if user.wishlist is None:
            user.wishlist = Wishlist.objects.create()
            user.save()
        wishlist_resource: WishlistResource = get_object_or_404(WishlistResource, id=resource_id)
        CartResource.objects.create(
            resource=wishlist_resource.resource,
            number=1,
            cart=user.cart,
        )
        user.cart.items += 1
        user.cart.save()
        user.wishlist.items -= 1
        user.wishlist.save()
        wishlist_resource.delete()
        return JsonResponse({ 'wishlist': user.wishlist.as_dict(), 'cart': user.cart.as_dict() }) 
    return JsonResponse({})


def cart_to_wishlist(request: HttpRequest, user: int) -> JsonResponse:
    """Defining request that moves cart item to wishlist"""
    if request.method == 'PUT':
        user: User = User.objects.get(id=user)
        if user.cart is None:
            user.cart = Cart.objects.create()
            user.save()
        if user.wishlist is None:
            user.wishlist = Wishlist.objects.create()
            user.save()
        cart_resource: CartResource = get_object_or_404(CartResource, id=json.loads(request.body))
        WishlistResource.objects.create(
            resource=cart_resource.resource,
            wishlist=user.wishlist,
        )
        user.wishlist.items += 1
        user.wishlist.save()
        user.cart.items -= 1
        user.cart.save()
        cart_resource.delete()
        return JsonResponse({ 'wishlist': user.wishlist.as_dict(), 'cart': user.cart.as_dict() }) 
    

def order(request: HttpRequest, user: int) -> JsonResponse:
    """Defining order GET, POST, PUT, and DELETE for Order object"""
    if request.method == 'GET':
        """Creating and returning order"""
        user: User = get_object_or_404(User, id=user)
        if user.cart is None:
            user.cart = Cart.objects.create()
            user.save()
        all_cart_resources = user.cart.cart_resource.all()
        seller_ids = {}
        for cart_resource in all_cart_resources:
            # Ensuring there is a new order for one buyer and each seller
            resource: Resource = cart_resource.resource
            if not resource.user.id in seller_ids:
                current_date = datetime.datetime.now()
                if resource.estimated_delivery_units == 'day':
                    estimated_date = current_date + datetime.timedelta(days=int(resource.estimated_delivery_time))
                elif resource.estimated_delivery_units == 'minute':
                    estimated_date = current_date + datetime.timedelta(minutes=int(resource.estimated_delivery_time))
                elif resource.estimated_delivery_units == 'hour':
                    estimated_date = current_date + datetime.timedelta(hours=int(resource.estimated_delivery_time))
                elif resource.estimated_delivery_units == 'week':
                    estimated_date = current_date + datetime.timedelta(weeks=int(resource.estimated_delivery_time))
                else:
                    estimated_date = current_date + datetime.timedelta(weeks=4*int(resource.estimated_delivery_time))
                order: Order = Order.objects.create(
                    buyer=user,
                    seller=resource.user,
                    estimated_delivery_date=estimated_date.date(),
                )
                orderResource: OrderResource = OrderResource.objects.create(
                    resource=resource,
                    order=order,
                    number=cart_resource.number
                )
                orderResource.save()
                order.save()
                seller_ids[resource.user.id] = order.id
            else:
                order = Order.objects.get(id=seller_ids[resource.user.id])
                orderResource: OrderResource = OrderResource.objects.create(
                    resource=resource,
                    order=order,
                    number=cart_resource.number
                )
                orderResource.save()
            resource.stock = resource.stock - cart_resource.number
            resource.save()
        # clear cart 
        user.cart.cart_resource.all().delete()
        return JsonResponse({'user': user.as_dict(), 'resources': [resource.as_dict() for resource in Resource.objects.all()]})
    elif request.method == 'POST':
        data = json.loads(request.body)
        user: User = get_object_or_404(User, id=user)
        current_date = datetime.datetime.now()
        if (not isinstance(data, int)) and data.get('exchange_id'):
            """Defining order caused by resource exchange"""
            exchange: Exchange = get_object_or_404(Exchange, id=data.get('exchange_id'))
            resource1: Resource = exchange.resource1
            if resource1.estimated_delivery_units == 'day':
                estimated_date = current_date + datetime.timedelta(days=int(resource1.estimated_delivery_time))
            elif resource1.estimated_delivery_units == 'minute':
                estimated_date = current_date + datetime.timedelta(minutes=int(resource1.estimated_delivery_time))
            elif resource1.estimated_delivery_units == 'hour':
                estimated_date = current_date + datetime.timedelta(hours=int(resource1.estimated_delivery_time))
            elif resource1.estimated_delivery_units == 'week':
                estimated_date = current_date + datetime.timedelta(weeks=int(resource1.estimated_delivery_time))
            else:
                estimated_date = current_date + datetime.timedelta(weeks=4*int(resource1.estimated_delivery_time))
            order: Order = Order.objects.create(
                buyer=exchange.user2,
                seller=resource1.user,
                estimated_delivery_date=estimated_date.date(),
                is_exchange=True
            )
            orderResource: OrderResource = OrderResource.objects.create(
                resource=resource1,
                order=order,
                number=exchange.resource1_number
            )
            orderResource.save()
            order.save()
            # reduce stock
            resource1.stock = resource1.stock - exchange.resource1_number
            resource1.save()
            resource2: Resource = exchange.resource2
            if resource2.estimated_delivery_units == 'day':
                estimated_date = current_date + datetime.timedelta(days=int(resource2.estimated_delivery_time))
            elif resource2.estimated_delivery_units == 'minute':
                estimated_date = current_date + datetime.timedelta(minutes=int(resource2.estimated_delivery_time))
            elif resource2.estimated_delivery_units == 'hour':
                estimated_date = current_date + datetime.timedelta(hours=int(resource2.estimated_delivery_time))
            elif resource2.estimated_delivery_units == 'week':
                estimated_date = current_date + datetime.timedelta(weeks=int(resource2.estimated_delivery_time))
            else:
                estimated_date = current_date + datetime.timedelta(weeks=4*int(resource2.estimated_delivery_time))
            order2: Order = Order.objects.create(
                buyer=exchange.user1,
                seller=resource2.user,
                estimated_delivery_date=estimated_date.date(),
                is_exchange=True
            )
            orderResource2: OrderResource = OrderResource.objects.create(
                resource=resource2,
                order=order2,
                number=exchange.resource2_number
            )
            orderResource2.save()
            order2.save()
            # reduce stock
            resource2.stock = resource2.stock - exchange.resource2_number
            resource2.save()
            exchange.delete()
            send_mail('Exchange Confirmation', f'Hi {order.buyer.first_name}!\n\nThis is to confirm that the exchange between you and {order.seller.first_name} has been accepted, and an order has been placed.\n\nThank you for shopping with EduSource.', 'edusource9325@gmail.com', [order.buyer.email])
            send_mail('Exchange Confirmation', f'Hi {order.seller.first_name}!\n\nThis is to confirm that the exchange between you and {order.buyer.first_name} has been accepted, and an order has been placed.\n\nThank you for shopping with EduSource.', 'edusource9325@gmail.com', [order.seller.email])
        else:
            """Defining order caused by 'Buy Now' shortcut"""
            cart_resource: CartResource = get_object_or_404(CartResource, id=json.loads(request.body))
            resource: Resource = cart_resource.resource
            if resource.estimated_delivery_units == 'day':
                estimated_date = current_date + datetime.timedelta(days=int(resource.estimated_delivery_time))
            elif resource.estimated_delivery_units == 'minute':
                estimated_date = current_date + datetime.timedelta(minutes=int(resource.estimated_delivery_time))
            elif resource.estimated_delivery_units == 'hour':
                estimated_date = current_date + datetime.timedelta(hours=int(resource.estimated_delivery_time))
            elif resource.estimated_delivery_units == 'week':
                estimated_date = current_date + datetime.timedelta(weeks=int(resource.estimated_delivery_time))
            else:
                estimated_date = current_date + datetime.timedelta(weeks=4*int(resource.estimated_delivery_time))
            order: Order = Order.objects.create(
                buyer=user,
                seller=resource.user,
                estimated_delivery_date=estimated_date.date(),
            )
            orderResource: OrderResource = OrderResource.objects.create(
                resource=resource,
                order=order,
                number=cart_resource.number
            )
            orderResource.save()
            order.save()
            # reduce stock
            resource.stock = resource.stock - cart_resource.number
            resource.save()
            cart_resource.delete()
            send_mail('Order Confirmation', f'Hi {user.first_name}!\n\nThis is to confirm that your order has been placed.\n\nThank you for shopping with EduSource.', 'edusource9325@gmail.com', [order.buyer.email])
            send_mail('Order Placed', f'Hi {order.seller.first_name}!\n\nPlease check your account - a new order has been placed.\n\nEduSource', 'edusource9325@gmail.com', [order.seller.email])
        return JsonResponse({'user': user.as_dict(), 'resources': [resource.as_dict() for resource in Resource.objects.all()]})
    elif request.method == 'DELETE':
        """Deleting order"""
        user: User = get_object_or_404(User, id=user)
        order: Order = get_object_or_404(Order, id=json.loads(request.body))
        order.status = 'Cancelled'
        order.save()
        send_mail(f'Order {order.id} Update', f'Hi {order.buyer.first_name},\n\nThis is to confirm that the status of your order {order.id} is now {order.status}. \n\nThank you for shopping with EduSource.', 'edusource9325@gmail.com', [order.buyer.email])
        send_mail(f'Order {order.id} Update', f'Hi {order.seller.first_name},\n\nThis is to inform you that you that the status of order {order.id} is now {order.status}.\n\nEduSource', 'edusource9325@gmail.com', [order.seller.email])
        return JsonResponse(user.as_dict())
    elif request.method == 'PUT': 
        """Updating order status"""
        user: User = get_object_or_404(User, id=user)
        data = json.loads(request.body)
        order: Order = get_object_or_404(Order, id=data['id'])
        order.status = data['status']
        order.save()
        if order.status == 'Processing' or order.status == 'Dispatched' or order.status == 'Complete':
            send_mail(f'Order {order.id} Update', f'Hi {order.buyer.first_name},\n\nThis is to inform you that you that the status of your order {order.id} is now {order.status}.\n\nEduSource', 'edusource9325@gmail.com', [order.buyer.email])
        elif order.status == 'Return Received':
            send_mail(f'Order {order.id} Update', f'Hi {order.buyer.first_name},\n\nThis is to inform you that you that the return of your order {order.id} has been received.\n\nEduSource', 'edusource9325@gmail.com', [order.buyer.email])
        elif order.status == 'Cancelled':
            send_mail(f'Order {order.id} Update', f'Hi {order.buyer.first_name},\n\nThis is to inform you that you that your order {order.id} is now {order.status}.\n\nEduSource', 'edusource9325@gmail.com', [order.buyer.email])
            send_mail(f'Order {order.id} Update', f'Hi {order.seller.first_name},\n\nThis is to inform you that you that order {order.id} has been Cancelled.\n\nEduSource', 'edusource9325@gmail.com', [order.seller.email])
        elif order.status == 'Refunded':
            send_mail(f'Order {order.id} Update', f'Hi {order.buyer.first_name},\n\nThis is to inform you that you that the return of your order {order.id} has been refunded.\n\nEduSource', 'edusource9325@gmail.com', [order.buyer.email])
        return JsonResponse(user.as_dict())
    return JsonResponse({})


def messages(request: HttpRequest, user1: int, user2: int) -> JsonResponse:
    """Create message between two users"""
    if request.method == 'POST':
        user1: User = get_object_or_404(User, id=user1)
        user2: User = get_object_or_404(User, id=user2)
        Messages.objects.create(
            user1=user1,
            user2=user2,
        )
        return users(request) # return all users
    return JsonResponse({})


def message(request: HttpRequest, id: int, sender: int) -> JsonResponse:
    if request.method == 'POST':
        """Sending message"""
        messages: Messages = get_object_or_404(Messages, id=id)
        user: User = get_object_or_404(User, id=sender)
        Message.objects.create(
            messages=messages,
            user=user,
            message=json.loads(request.body)
        )
        if messages.user1 == user:
            messages.user1_seen = timezone.now()
        else:
            messages.user2_seen = timezone.now()
        messages.last_edited = timezone.now()
        messages.save()
        return users(request) # return all users
    elif request.method == 'GET':
        """Updating last seen each time user checks messages"""
        messages: Messages = get_object_or_404(Messages, id=id)
        user: User = get_object_or_404(User, id=sender)
        if messages.user1 == user:
            messages.user1_seen = timezone.now()
        else:
            messages.user2_seen = timezone.now()
        messages.save()
        return users(request) # return all users
    return JsonResponse({})


def semantic_search(request: HttpRequest, user: int) -> JsonResponse:
    """Defining semantic search used to return relevant search results to user"""
    if request.method != 'POST' and request.method != 'PUT':
        return JsonResponse({})
    
    search: str = json.loads(request.body)

    # guide to perform semantic search: https://huggingface.co/sentence-transformers
    dataset_resources: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('id', flat=True))

    # data preprocessing
    dataset_description: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('description', flat=True))
    dataset_name: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('name', flat=True))
    dataset_subject: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('subject', flat=True))
    dataset_author: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('author', flat=True))
    dataset_colour: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('colour', flat=True))
    
    # determine embeddings
    search_embeddings = semantic_search_model.encode(search)
    embeddings_description = semantic_search_model.encode(dataset_description)
    embeddings_name = semantic_search_model.encode(dataset_name)
    embeddings_subject = semantic_search_model.encode(dataset_subject)
    embeddings_author = semantic_search_model.encode(dataset_author)
    embeddings_colour = semantic_search_model.encode(dataset_colour)

    # generate similairty matrix
    similarity_matrix_description: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings_description)
    similarity_matrix_name: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings_name)
    similarity_matrix_subject: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings_subject)
    similarity_matrix_author: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings_author)
    similarity_matrix_colour: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings_colour)

    # convert tensor to dictionary sorted on values (similarity)
    list_similarity_matrix_description = similarity_matrix_description.tolist()[0]
    search_dict_description = list(zip(dataset_description, list_similarity_matrix_description))
    
    list_similarity_matrix_name = similarity_matrix_name.tolist()[0]
    search_dict_name = list(zip(dataset_name, list_similarity_matrix_name))
    
    list_similarity_matrix_subject = similarity_matrix_subject.tolist()[0]
    search_dict_subject = list(zip(dataset_subject, list_similarity_matrix_subject))
    
    list_similarity_matrix_author = similarity_matrix_author.tolist()[0]
    search_dict_author = list(zip(dataset_author, list_similarity_matrix_author))
    
    list_similarity_matrix_colour = similarity_matrix_colour.tolist()[0]
    search_dict_colour = list(zip(dataset_colour, list_similarity_matrix_colour))
    
    search_dict = {}
    if request.method == 'POST':
        for i in range(len(dataset_resources)):
            search_dict[dataset_resources[i]] = (search_dict_description[i][1]*0.1+
                search_dict_name[i][1]*0.8+
                search_dict_subject[i][1]*0.1)
        
        sorted_search_dict = sorted(search_dict.items(), key=order_data, reverse=True)
        keys: list = [pair[0] for pair in sorted_search_dict if pair[1] >= 0.2]
    if request.method == 'PUT':
        # storing unique search history
        if user != '-1':
            user: User = get_object_or_404(User, id=user)
            contains_search = False
            search_id = -1
            try:
                get_object_or_404(SearchHistory, user=user)
            except:
                user.search_history = SearchHistory.objects.create(user=user)
                user.save()
            for search_item in user.search_history.search_item.all():
                if search_item.search.lower() == search.lower():
                    contains_search = True
                    search_id = search_item.id
                    break
            if not contains_search:
                SearchHistoryItem.objects.create(
                    search=search,
                    search_history=user.search_history
                )
            else:
                # Update timestamp
                search_history_item: SearchHistoryItem = get_object_or_404(SearchHistoryItem, id=search_id)
                search_history_item.save()
        for i in range(len(dataset_resources)):
            search_dict[dataset_resources[i]] = (search_dict_description[i][1]*0.35+
                search_dict_name[i][1]*0.35+
                search_dict_subject[i][1]*0.1+ 
                search_dict_author[i][1]*0.1+
                search_dict_colour[i][1]*0.1)
        sorted_search_dict = sorted(search_dict.items(), key=order_data, reverse=True)
        threshold = 0.5
        keys = []
        keys: list = [pair[0] for pair in sorted_search_dict if pair[1] >= threshold]
        while len(keys) == 0 and threshold > 0.4:
            keys: list = [pair[0] for pair in sorted_search_dict if pair[1] >= threshold]
            threshold = round(threshold - 0.01, 2)
    resources: list = []
    # using iteration to preserve order of resources
    for key in keys:
        resource = get_object_or_404(Resource, id=key)
        resources.append(resource.as_dict())
    return JsonResponse(resources, safe=False)


def semantic_search_subjects(request: HttpRequest) -> JsonResponse:
    """Defining semantic search used to return relevant subjects to user"""
    # guide to perform semantic search: https://huggingface.co/sentence-transformers
    dataset_resources: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('id', flat=True))

    # data preprocessing
    dataset: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('subject', flat=True))
    if request.method == 'POST':
        # ensuring values in lists are unique
        values_included: list = []
        new_dataset_resources: list = []
        new_dataset: list = []
        for i in range(len(dataset)):
            if not dataset[i] in values_included:
                new_dataset_resources.append(dataset_resources[i])
                new_dataset.append(dataset[i])
                values_included.append(dataset[i])

        # determine embeddings
        embeddings = semantic_search_model.encode(new_dataset)
        search: str = json.loads(request.body)
        search_embeddings = semantic_search_model.encode(search)

        # generate similairty matrix
        similarity_matrix: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings)
        
        # convert tensor to dictionary sorted on values (similarity)
        list_similarity_matrix = similarity_matrix.tolist()[0]
        search_dict = dict(zip(new_dataset_resources, list_similarity_matrix))
        sorted_search_dict = sorted(search_dict.items(), key=order_data, reverse=True)

        keys: list = [pair[0] for pair in sorted_search_dict]
        resources: list = []

        # using iteration to preserve order of resources
        for key in keys:
            resource = Resource.objects.get(id=key)
            resources.append(resource.as_dict()['subject'])
        return JsonResponse(resources, safe=False)
    return JsonResponse({})


def semantic_search_orders(request: HttpRequest, id: int, search: str, mode: str) -> JsonResponse:
    """Defining semantic search used to return relevant orders to user"""
    # guide to perform semantic search: https://huggingface.co/sentence-transformers
    if request.method == 'POST':
        """ logic: map each order to a corresponding id i.e. a dict
            check if any resources ordered match search with > 70%
            store orderid:boolean pair to determine whether to keep showing order """
        user: User = get_object_or_404(User, id=id)
        matching_orders = []
        if mode == 'buyer':
            orders = Order.objects.filter(buyer=user).order_by('id')
        else:
            orders = Order.objects.filter(seller=user).order_by('id')
        
        for order in orders:
            resources: list = list(OrderResource.objects.filter(order=order).order_by('id').values_list('resource', flat=True))
            dataset = list(Resource.objects.filter(id__in=resources).order_by('id').values_list('name', flat=True))

            # determine embeddings
            embeddings = semantic_search_model.encode(dataset)
            search: str = search
            search_embeddings = semantic_search_model.encode(search)

            # generate similairty matrix
            similarity_matrix: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings)

            # check if any matches are greater than 70%
            if (similarity_matrix > 0.7).any().item():
                matching_orders.append(order.id)
                continue
        return JsonResponse(matching_orders, safe=False)
    return JsonResponse({})


def order_data(item: tuple):
    """Sort dictionary based on values by returning index of element which stores similarity"""
    return item[1] 


def recommendations(request: HttpRequest, user: int) -> JsonResponse:
    user: User = get_object_or_404(User, id=user)
    """Defining semantic search used to return personalised recommendations"""
    # guide to perform semantic search: https://huggingface.co/sentence-transformers
    dataset_resources: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('id', flat=True))

    # data preprocessing - consider resource, name, subject and description
    resources = Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('description', 'name', 'subject')
    dataset: list = [ " ".join(resource) for resource in resources ]

    # ensuring values in lists are unique
    values_included: list = []
    new_dataset_resources: list = []
    new_dataset: list = []
    for i in range(len(dataset)):
        if not dataset[i] in values_included:
            new_dataset_resources.append(dataset_resources[i])
            new_dataset.append(dataset[i])
            values_included.append(dataset[i])

    # determine embeddings
    embeddings = semantic_search_model.encode(new_dataset)
    try:
        search_history: SearchHistory = SearchHistory.objects.get(user=user)
    except:
        user.search_history = SearchHistory.objects.create(user=user)
    search_history: list = list(SearchHistory.objects.get(user=user).search_item.all().order_by('-last_searched').values_list('search', flat=True))
    subject_preferences: list = list(user.subject.all().order_by('id').values_list('name', flat=True))
    subject_preferences.extend(search_history)
    history = subject_preferences
    if len(history) == 0:
        return JsonResponse([], safe=False)
    search_embeddings = semantic_search_model.encode(history)

    # generate similairty matrix
    similarity_matrix: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings)
    
    # convert tensor to dictionary sorted on values (similarity)
    list_similarity_matrix = similarity_matrix.sum(dim=0) / len(history)
    search_list = dict(zip(new_dataset_resources, list_similarity_matrix))
    sorted_search_list = sorted(search_list.items(), key=order_data, reverse=True)
    keys: list = [pair[0] for pair in sorted_search_list if pair[1] >= 0.15]
    resources: list = []

    # using iteration to preserve order of resources
    for key in keys:
        resource = Resource.objects.get(id=key)
        resources.append(resource.as_dict())
    return JsonResponse(resources, safe=False)


def order_return(request: HttpRequest, user: id, order: id, resource: id) -> JsonResponse:
    """Allowing user to edit the number of items they want to return"""
    user: User = get_object_or_404(User, id=user)
    order: Order = get_object_or_404(Order, id=order)
    resource: OrderResource = get_object_or_404(OrderResource, id=resource)
    if request.method == 'PUT':
        resource.number_for_return = json.loads(request.body)
        if resource.number_for_return > 0:
            resource.for_return = True
        else:
            resource.for_return = False
        resource.save()
        return JsonResponse({'user': user.as_dict(), 'resource': resource.resource.as_dict()})
    return JsonResponse({})


def submit_return(request: HttpRequest, user: id, order: id) -> JsonResponse:
    """Implementing submitting or cancellation of return"""
    user: User = get_object_or_404(User, id=user)
    order: Order = get_object_or_404(Order, id=order)
    if request.method == 'PUT':
        data = json.loads(request.body)
        order.status = 'Complete' if data['cancel'] == 'true' else 'Return Started'
        order.save()
        if order.status == 'Return Started':
            send_mail(f'Order {order.id} Update', f'Hi {order.buyer.first_name},\n\nThis is to inform you that you that a return has been started for your order {order.id}.\n\nEduSource', 'edusource9325@gmail.com', [order.buyer.email])
            send_mail(f'Order {order.id} Update', f'Hi {order.seller.first_name},\n\nThis is to inform you that you that a request has been made for the return of order {order.id}.\n\nEduSource', 'edusource9325@gmail.com', [order.seller.email])
        elif order.status == 'Complete':
            send_mail(f'Order {order.id} Update', f'Hi {order.buyer.first_name},\n\nThis is to inform you that you that the return of your order {order.id} has been cancelled.\n\nEduSource', 'edusource9325@gmail.com', [order.buyer.email])
            send_mail(f'Order {order.id} Update', f'Hi {order.seller.first_name},\n\nThis is to inform you that you that the return of order {order.id} is has been cancelled.\n\nEduSource', 'edusource9325@gmail.com', [order.seller.email])
        
        if data['cancel'] == 'true':
            for order_resource in order.order_resource.all():
                order_resource.for_return = False
                order_resource.number_for_return = 0
                order_resource.save()
            order.return_reason = ''
        else:
            order.return_method = data['return_method']
            order.return_reason = data['return_reason']
        order.save()
        return JsonResponse({'user': user.as_dict(), 'resources': [resource.as_dict() for resource in Resource.objects.all()]})
    return JsonResponse({})


def exchange(request: HttpRequest, user: int, seller: int, resource: int) -> JsonResponse:
    """Defining GET, PUT, and POST for Exchange object"""
    if request.method == 'GET':
        # Return Exchange instance
        return JsonResponse(get_object_or_404(Exchange, id=resource).as_dict())
    elif request.method == 'POST':
        # Create and return new Exchange instance
        exchange: Exchange = Exchange.objects.create(
            user1=get_object_or_404(User, id=user),
            user2=get_object_or_404(User, id=seller),
            resource2=get_object_or_404(Resource, id=resource),
        )
        user_to_send: User = get_object_or_404(User, id=user)
        if exchange.user1 == user_to_send:
            exchange.status1 = 'Accepted'
        else:
            exchange.status2 = 'Accepted'
        exchange.save()
        return JsonResponse({'user': user_to_send.as_dict(), 'exchange': exchange.as_dict()})
    elif request.method == 'PUT':
        # Updating user selected resource
        exchange: Exchange = get_object_or_404(Exchange, id=resource)
        data = json.loads(request.body)
        if exchange.user1.id == user:
            if data['field'] == 'resource':
                exchange.resource1 = get_object_or_404(Resource, id=data['data'])
                exchange.status2 = 'Pending'
            elif data['field'] == 'status':
                exchange.status1 = data['data']
            elif data['field'] == 'user1':
                exchange.resource1_number = data['data']
                exchange.status2 = 'Pending'
            elif data['field'] == 'user2':
                exchange.resource2_number = data['data']
                exchange.status2 = 'Pending'
        else:
            if data['field'] == 'resource':
                exchange.resource2 = get_object_or_404(Resource, id=data['data'])
                exchange.status1 = 'Pending'
            elif data['field'] == 'status':
                exchange.status2 = data['data']
            elif data['field'] == 'user1':
                exchange.resource2_number = data['data']
                exchange.status1 = 'Pending'
            elif data['field'] == 'user2':
                exchange.resource1_number = data['data']
                exchange.status1 = 'Pending'
        exchange.save()
        user_to_send: User = get_object_or_404(User, id=user)
        return JsonResponse({'user': user_to_send.as_dict(), 'exchange': exchange.as_dict()})
    elif request.method == 'DELETE':
        # Deleting exchange instance
        exchange: Exchange = get_object_or_404(Exchange, id=resource)
        exchange.delete()
        user = get_object_or_404(User, id=user)
        return JsonResponse(user.as_dict())
    return JsonResponse({})


def feedback(request: HttpRequest) -> JsonResponse:
    """Allowing users to send feedback - email is sent to myself with user feedback as the content"""
    if request.method == 'POST':
        feedback = json.loads(request.body)
        send_mail('Feedback submitted', feedback, 'edusource9325@gmail.com', ['edusource9325@gmail.com'])
    return JsonResponse({})


# Dictionary of known questions and answers - can be quickly returned by chatbot
known_questions_and_answers = {
    'How do I place an order?' : '''There are two ways to do this:\n
    The first way is as follows:
    \n1. Ensure you are in buyer mode (from settings)
    \n2. Search for the item
    \n3. Select the item
    \n4. Select Buy Now
    \n5. Select Place Order
    \nThe second way is as follows:
    \n1. Ensure you are in buyer mode (from settings)
    \n2. Search for the item
    \n3. Select the item
    \n4. Add item to Cart
    \n5. Select Cart
    \n6. Select Checkout
    \n7. Select Place Order
    \nI hope that helps.''',
    'How do I exchange resources?' : '''1. Search for the Item
    \n2. Select the item
    \n3. Select Exchange
    \n4. Select a resource you want to exchange
    \nI hope that helps.''',
    'How do I list items' : '''
    1. Ensure you are in seller mode (from settings)
    \n2. Select Account
    \n3. Select Listings
    \n4. Select the + within the listing container
    \nI hope that helps''',
    'How do I track an order?' : '''
    1. Select Account
    \n2. Select Orders
    \n3. Select Order
    \n4. View Order Status
    \nI hope that helps''',
    'How do I start a return?' : '''    
    1. Ensure you are in buyer mode (from settings)
    \n2. Select Account
    \n3. Select Orders
    \n4. Select Order
    \n5. Select Start Return
    \n6. Select number of items for return
    \n7. Select Return Method
    \n8. (Optional) Add Return Reason
    \n9. Click Submit
    \nI hope that helps.''',
    'Do you provide resource recommendations?': "Of course! Start your next sentence with 'Can you provide resource recommendations for...'",
    'Can you provide resource recommendations for': '',
    'What is the status of order': '',
    'Provide me with personalised recommendations': '',
    'Where is my wishlist': '''1. Select Account
    \n2. Select Wishlist''',
    'How can I find my wishlist': '''1. Select Account
    \n2. Select Wishlist''',
    'How can I find my order details': "Click 'View Details' on the order",
    'How do I compare resources': "Click 'Compare Resources' after searching for an item. You can compare a maximum of 2 resources at one time.",
    'How do I delete my account': '''1. Select Account
    \n2. Select Details
    \n3. Click 'Delete Account' at the bottom of the page''',
    'How can I view messages': '''1. Select Account
    \n2. Select Messages
    \n3. (Optional) Select a message'''
}

def chatbot(request: HttpRequest, user: int) -> JsonResponse:
    """Defining chatbot implementation"""
    # guide to perform semantic search: https://huggingface.co/sentence-transformers

    user_input: str = json.loads(request.body)
    
    # providing responses to known questions
    dataset: list = list(known_question for known_question in known_questions_and_answers)

    # determine embeddings
    embeddings = semantic_search_model.encode(dataset)
    search_embeddings = semantic_search_model.encode(user_input)

    # generate similairty matrix
    similarity_matrix: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings)
    
    # convert tensor to dictionary sorted on values (similarity)
    list_similarity_matrix = similarity_matrix.tolist()[0]
    search_dict = dict(zip(dataset, list_similarity_matrix))
    sorted_search_dict = sorted(search_dict.items(), key=order_data, reverse=True)
    if sorted_search_dict[0][1] > 0.44:
        if sorted_search_dict[0][0] == 'What is the status of order':
            # returning order status
            if user == '-1':
                return JsonResponse('You must be signed in to verify this.', safe=False)
            user: User = get_object_or_404(User, id=user)
            try:
                order_number: int = int((user_input.lower().replace('number','').replace('.','').replace('?','').split('what is the status of order')[1]).replace(' ',''))
                order: Order = get_object_or_404(Order, id=order_number)
                if (order.seller != user) and (order.buyer != user):
                    return JsonResponse('This order does not belong to you, so I cannot provide details.', safe=False)
                return JsonResponse(order.status, safe=False)
            except:
                return JsonResponse('Sorry, I do not recogise that order number.\nEnter a whole integer which you can see in Account -> Orders', safe=False)
        elif sorted_search_dict[0][0] == 'Provide me with personalised recommendations':
            # returning personalised recommendations
            if user == '-1':
                return JsonResponse('You must be signed in for this to be available.', safe=False)
            user: User = get_object_or_404(User, id=user)
            returned_recommendations = json.loads(recommendations(request, user.id).content)
            response_string = f'Below are some recommendations:'
            added_recommendations = {}
            for recommendation in returned_recommendations[:10]:
                if not added_recommendations.get(recommendation['name']) == recommendation['author']:
                    response_string += '\n' + recommendation['name'] + ' by ' + recommendation['author']
                    added_recommendations[recommendation['name']] = recommendation['author']
            if len(returned_recommendations) == 0:
                return JsonResponse('Sorry, I cannot do that as you do not have any personalised recommendations yet.\nAs you search through the app and add subjects preferences to your profile, this will update.', safe=False)
            return JsonResponse(response_string, safe=False)
        elif sorted_search_dict[0][0] == 'Can you provide resource recommendations for':
            """Generating resource recommendations based on input"""
            recommendation_query_list: list = (user_input.lower().split('can you provide resource recommendations for'))
            if len(recommendation_query_list) == 1 or recommendation_query_list[1].strip() == '':
                return JsonResponse('Please repeat the statement with a recommendation.', safe=False)
            recommendation_query = recommendation_query_list[1]

            dataset_resources: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('id', flat=True))
            # data preprocessing
            resources: list = list(Resource.objects.filter(stock__gt=0, is_draft=False).order_by('id').values_list('description', 'name', 'subject', 'type'))
            dataset = [ " ".join(resource) for resource in resources ]
            # ensuring values in lists are unique
            values_included: list = []
            new_dataset_resources: list = []
            new_dataset: list = []
            for i in range(len(dataset)):
                if not dataset[i] in values_included:
                    new_dataset_resources.append(dataset_resources[i])
                    new_dataset.append(dataset[i])
                    values_included.append(dataset[i])

            # determine embeddings
            embeddings = semantic_search_model.encode(new_dataset)
            search_embeddings = semantic_search_model.encode(recommendation_query)

            # generate similairty matrix
            similarity_matrix: torch.Tensor = semantic_search_model.similarity(search_embeddings, embeddings)
            
            # convert tensor to dictionary sorted on values (similarity)
            list_similarity_matrix = similarity_matrix.tolist()[0]
            search_dict = dict(zip(new_dataset_resources, list_similarity_matrix))
            sorted_search_dict = sorted(search_dict.items(), key=order_data, reverse=True)

            # use first 10 results
            reduced_search_dict = sorted_search_dict[0:min(10,len(sorted_search_dict))]
            keys: list = [pair[0] for pair in reduced_search_dict if pair[1] >= 0.45]
            resources: list = []

            added_recommendations = {}
            response_string = f'Below are some recommendations:'
            # using iteration to preserve order of resources
            for key in keys:
                resource = Resource.objects.get(id=key)
                if not added_recommendations.get(resource.name) == resource.author:
                    response_string += '\n' + resource.name + ' by ' + resource.author
                    added_recommendations[resource.name] = resource.author
            if len(added_recommendations) == 0:
                return JsonResponse('Sorry. We were unable to find resources matching your query.', safe=False)
            return JsonResponse(response_string, safe=False)
        return JsonResponse(known_questions_and_answers[sorted_search_dict[0][0]], safe=False)

    try:
        # guide to implement chatbot: https://huggingface.co/docs/transformers/en/model_doc/blenderbot
        tokenised_input = chatbot_tokeniser([user_input], return_tensors='pt')
        model_output = chatbot_model.generate(**tokenised_input)
        response = chatbot_tokeniser.decode(model_output[0], temperature=0.8, max_length=1000, skip_special_tokens=True)
        return JsonResponse(response, safe=False)
    except:
        # accounting for the input limitations of the chatbot
        return JsonResponse("I'm having trouble processing this. Could you make your request shorter?", safe=False)