import datetime
import json
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate
from django.db.models.query import QuerySet
from django.db.models import Avg
from django.contrib import auth
from .forms import SignupForm, AddressForm, LoginForm
from .models import Resource, Review, User, Address
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money


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
                description=signup_data['description']
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
    if request.method == 'POST':
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


def currency_conversion(request: HttpRequest, id: int, from_currency: str, to_currency: float) -> JsonResponse:
    resource: Resource = get_object_or_404(Resource, id=id)
    initial_value: Money = Money(resource.price, to_currency)
    return JsonResponse({'new_price': str(convert_money(initial_value, from_currency))})


def user(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        return JsonResponse({'user' : User.objects.get(username=request.user.username).as_dict()})
    return JsonResponse({'user' : 'unauthenticated'})


def set_resource_rating(resource_id: int) -> float:
    average_rating = Review.objects.filter(resource=resource_id).aggregate(Avg('rating'))['rating__avg']
    return average_rating if average_rating else 0.0


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
        return JsonResponse(resource.as_dict())
    if request.method == 'DELETE':
        review: Review = Review.objects.get(id=resource)
        resource: Resource = Resource.objects.get(id=review.resource.id)
        review.delete()
        resource.rating = set_resource_rating(resource.id)
        resource.save()
        return JsonResponse(resource.as_dict())
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
        review.upload_date = datetime.datetime.now()
        review.save()
        resource.rating = set_resource_rating(resource.id)
        resource.save()
        old_resource: Resource = Resource.objects.get(id=data.get('old_resource'))
        old_resource.rating = set_resource_rating(old_resource)
        old_resource.save()
        return JsonResponse({'old_resource' : old_resource.as_dict(),
                             'new_resource' : resource.as_dict()})
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
            delivery_option=data.get('delivery'),
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
        print(resource.image1, media_data.get('image1'))
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
        resource.user=user
        resource.save()
        print(resource.image1, media_data.get('image1'))
        return JsonResponse(resource.as_dict())
    return JsonResponse({})


def sentiment_analysis(request: HttpRequest, resource: str) -> JsonResponse:
    resources = Resource.objects.filter(name=resource)
    reviews = Review.objects.filter(resource__in=resources)
    print(reviews)
    return JsonResponse({})