import datetime
from decimal import Decimal
from django.utils import timezone
import json
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.contrib import auth
from .forms import SignupForm, AddressForm, LoginForm
from .models import Cart, CartResource, Messages, Order, OrderResource, Resource, Review, User, Address, WishlistResource, Message
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money
from transformers import pipeline


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
                username=signup_data['username'],
                password=signup_data['password'],
                theme_preference=signup_data['theme_preference'],
                mode=signup_data['mode'],
                description=signup_data['description'],
                cart=Cart.objects.create()
            )
            Address.objects.create(
                first_line=address_data['first_line'],
                second_line=address_data['second_line'],
                city=address_data['city'],
                postcode=address_data['postcode'],
                user=user
            )
            # log in user
            authenticated_user: User | None = authenticate(request, username=signup_data['username'], password=signup_data['password'])
            if authenticated_user:
                auth.login(request, authenticated_user)
            return redirect('http://localhost:5173/')
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
                return redirect('http://localhost:5173/')
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

def currency_conversion(request: HttpRequest, id: int, from_currency: str, to_currency: float) -> JsonResponse:
    resource: Resource = get_object_or_404(Resource, id=id)
    initial_value: Money = Money(resource.price, to_currency)
    return JsonResponse({'new_price': str(convert_money(initial_value, from_currency))})


def user(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        return JsonResponse({'user' : User.objects.get(username=request.user.username).as_dict()})
    return JsonResponse({'user' : 'unauthenticated'})


def users(request: HttpRequest) -> JsonResponse:
    return JsonResponse([user.as_dict() for user in User.objects.all()], safe=False)


def set_resource_rating(resource_id: int) -> float:
    average_rating = Review.objects.filter(resource=resource_id).aggregate(Avg('rating'))['rating__avg']
    return average_rating if average_rating else 0.0


def update_seller_rating(user: User) -> None:
    """Ensuring seller rating is defined based on sentiment of reviews"""
    reviews = list(Review.objects.filter(resource__user__id=user.id).values_list('review', flat=True))
    # https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment
    bert = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
    stars = list(int(review['label'][0]) for review in bert(reviews))
    if len(stars) == 0:
        user.rating = 0
    else:
        average = round(sum(stars) / len(stars), 1)
        user.rating = average
    user.save()


def review(request: HttpRequest, user: int, resource: int) -> JsonResponse:
    if request.method == 'POST':
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


def resources(request: HttpRequest) -> JsonResponse:
    return JsonResponse([resource.as_dict() for resource in Resource.objects.all()], safe=False)


def user_details(request: HttpRequest, id: int, attribute: str) -> JsonResponse | Http404:
    """Defining PUT request handling"""
    if request.method == 'PUT':
        user: User | Http404 = get_object_or_404(User, id=id)
        address: Address | Http404 = get_object_or_404(Address, user=user)
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
        user.save()
        address.save()
        if attribute == 'password':
            user: User | None = authenticate(request, username=user.username, password=json.loads(request.body))
            if user:
                auth.login(request, user)
        return JsonResponse(user.as_dict())
    return JsonResponse('no user', safe=False)


def check_details(request: HttpRequest, id: int, attribute: str) -> JsonResponse:
    """Defining PUT request handling"""
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
    """Defining POST, PUT and DELETE request handling"""
    data: dict[str, any] = request.POST
    media_data: dict[str, any] = request.FILES
    user: User = get_object_or_404(User, id=id)
    if request.method == 'DELETE':
        resource: Resource = get_object_or_404(Resource, id=json.loads(request.body))
        resource.delete()
    if request.method == 'POST' and not data.get('id'):
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
    resources = Resource.objects.filter(name=resource)
    reviews = list(Review.objects.filter(resource__in=resources).values_list('review', flat=True))
    reviews_ids = list(Review.objects.filter(resource__in=resources).values_list('id', flat=True))
    # https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment
    bert = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
    scores = list(review['score'] for review in bert(reviews))
    reviews_scores = dict(zip(reviews_ids, scores))
    return JsonResponse(reviews_scores, safe=False)


def update_cart(request: HttpRequest, user: int, cart: int, resource: int) -> JsonResponse:
    user: User = get_object_or_404(User, id=user)
    if request.method == 'POST':
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
        cartResource: CartResource = get_object_or_404(CartResource, id=cart)
        if cartResource.resource.id != int(resource):
            cartResource.resource = Resource.objects.get(id=resource)
        cartResource.number = json.loads(request.body)
        cartResource.save()
        user.cart.items += json.loads(request.body)
        return JsonResponse({'resource': cartResource.as_dict(), 'cart': user.cart.as_dict(), 'wishlist': user.wishlist.as_dict()})
    elif request.method == 'DELETE':
        resource: CartResource = get_object_or_404(CartResource, id=cart)
        user.cart.items -= 1
        user.cart.save()
        resource.delete()
        return JsonResponse({'resource': [], 'cart': user.cart.as_dict(), 'wishlist': user.wishlist.as_dict()})
    return JsonResponse({})


def get_cart(request: HttpRequest, user: int) -> JsonResponse:
    user: User = get_object_or_404(User, id=user)
    return JsonResponse(user.cart.as_dict())


def update_wishlist(request: HttpRequest, user: int) -> JsonResponse:
    """Defining POST, PUT and DELETE handling"""
    resource_id = json.loads(request.body)
    if request.method == 'POST':
        user: User = User.objects.get(id=user)
        WishlistResource.objects.create(
            resource = Resource.objects.get(id=resource_id),
            wishlist=user.wishlist
        )
        user.wishlist.items +=1
        user.wishlist.save()
        return JsonResponse({ 'wishlist': user.wishlist.as_dict() }) 
    elif request.method == 'DELETE':
        user: User = User.objects.get(id=user)
        resource: WishlistResource = get_object_or_404(WishlistResource, resource=Resource.objects.get(id=resource_id))
        user.wishlist.items -= 1
        user.wishlist.save()
        resource.delete()
        return JsonResponse({ 'wishlist': user.wishlist.as_dict() }) 
    elif request.method == 'PUT':
        """Defining move from cart to wishlist"""
        user: User = User.objects.get(id=user)
        wishlist_resource: WishlistResource = get_object_or_404(WishlistResource, id=resource_id)
        cartResource: CartResource = CartResource.objects.create(
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
        cart_resource: CartResource = get_object_or_404(CartResource, id=json.loads(request.body))
        wishlist_resource: WishlistResource = WishlistResource.objects.create(
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
    """Defining order creation"""
    if request.method == 'GET':
        """Creating and returning order"""
        user: User = get_object_or_404(User, id=user)
        all_cart_resources = user.cart.cart_resource.all()
        # Order is between one buyer and one seller, so there may be multiple 
        seller_ids = {}
        for cart_resource in all_cart_resources:
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
    return JsonResponse({})


def messages(request: HttpRequest, user1: int, user2: int) -> JsonResponse:
    if request.method == 'POST':
        user1: User = get_object_or_404(User, id=user1)
        user2: User = get_object_or_404(User, id=user2)
        messages: Messages = Messages.objects.create(
            user1=user1,
            user2=user2,
        )
        return users(request)
    return JsonResponse({})


def message(request: HttpRequest, id: int, sender: int) -> JsonResponse:
    if request.method == 'POST':
        messages: Messages = get_object_or_404(Messages, id=id)
        Message.objects.create(
            messages=messages,
            user=get_object_or_404(User, id=sender),
            message=json.loads(request.body)
        )
        return users(request)
    return JsonResponse({})