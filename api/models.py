from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.db.models import Q


class Cart(models.Model):
    """Defining attributes and methods for Cart model"""
    items = models.IntegerField(null=False, blank=False, default=0, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0)])

    def as_dict(self) -> str:
        """Defining dictionary representation of Cart object"""
        cart_resources = CartResource.objects.filter(cart=self.id)
        return {
            'id' : self.id,
            'resources': [resource.as_dict() for resource in cart_resources],
            'items' : self.items,
            'total' : self.total
        }


class Wishlist(models.Model):
    """Defining attributes and methods for Wishlist model"""
    items = models.IntegerField(null=False, blank=False, default=0, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0)])

    def as_dict(self) -> str:
        """Defining dictionary representation of Wishlist object"""
        wishlist_resources = WishlistResource.objects.filter(wishlist=self.id)
        return {
            'id' : self.id,
            'resources': [resource.as_dict() for resource in wishlist_resources],
            'items' : self.items,
            'total' : self.total
        }


class User(AbstractUser):
    """Defining attrbiutes and methods for User model"""
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150, null=False, blank=False, validators=[RegexValidator(r'^[a-zA-Z ]+$', message='No special characters allowed'), RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    last_name = models.CharField(max_length=150, null=False, blank=False, validators=[RegexValidator(r'^[a-zA-Z ]+$', message='No special characters allowed'), RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    phone_number = models.CharField(max_length=11 ,unique=True, null=False, blank=False, validators=[RegexValidator(r'^07(\d{8,9})$', message='Must be 10 or 11 digit number starting with 07')])
    rating = models.DecimalField(null=False, blank=True, default=0.0, max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    description = models.TextField(null=False, blank=True, validators=[RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    THEMES: list [tuple[str, str]] = [('light', 'light'), ('dark', 'dark')]
    cart = models.OneToOneField(Cart, null=True, on_delete=models.CASCADE, related_name='user')
    wishlist = models.OneToOneField(Wishlist, null=True, on_delete=models.CASCADE, related_name='user')
    theme_preference = models.CharField(max_length=5, choices=THEMES, default='light', null=False, blank=False)
    
    MODES: list [tuple[str, str]] = [('buyer', 'buyer'), ('seller', 'seller')]
    mode = models.CharField(max_length=6, choices=MODES, default='buyer', null=False, blank=False)
    
    CURRENCIES: list [tuple[str, str]] = [('USD', 'USD'), ('GBP', 'GBP'), ('EUR', 'EUR')]
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='GBP', null=False, blank=False)

    groups = models.ManyToManyField(Group, blank=True, related_name='new_user_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='new_user_permissions_set')

    def __str__(self) -> str:
        """Defining string representation of User model"""
        return f"{self.first_name} {self.last_name}: {self.email}"
    
    def as_dict(self) -> dict[str, int | float | str]:
        """Defining dictionary representation of User object"""
        try:
            address: Address = Address.objects.get(user=self)
        except:
            address: Address = Address.objects.create(
                first_line='test',
                city='test',
                postcode='edusrc',
                user=self
            )
        try:
            search_history: SearchHistory = SearchHistory.objects.get(user=self)
        except:
            self.search_history=SearchHistory.objects.create(user=self)
            self.save()
            search_history: SearchHistory = SearchHistory.objects.get(user=self)
        if self.cart == None:
            self.cart = Cart.objects.create()
        if self.wishlist == None:
            self.wishlist = Wishlist.objects.create()
        self.save()
        placed_orders = Order.objects.filter(buyer=self)
        sold_orders = Order.objects.filter(seller=self)
        messages = Messages.objects.filter(Q(user1=self) | Q(user2=self))
        subjects = Subject.objects.filter(user=self)
        exchanges = Exchange.objects.filter(Q(user1=self) | Q(user2=self))
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'rating': self.rating,
            'description': self.description,
            'theme_preference': self.theme_preference,
            'mode': self.mode,
            'currency': self.currency,
            'address_line_one': address.first_line,
            'address_second_line': address.second_line,
            'city': address.city,
            'postcode': address.postcode,
            'listings': [listing.as_dict() for listing in self.listing.all()],
            'placed_orders': [order.as_dict() for order in placed_orders],
            'sold_orders': [order.as_dict() for order in sold_orders],
            'messages': [message.as_dict() for message in messages],
            'subjects': [subject.as_dict() for subject in subjects],
            'cart': self.cart.as_dict(),
            'wishlist': self.wishlist.as_dict(),
            'exchanges': [exchange.as_dict() for exchange in exchanges],
            'search_history': search_history.as_dict()
        }


class Subject(models.Model):
    """Defining attributes and methods for Subject model"""
    name = models.CharField(max_length=150, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject')
    
    def as_dict(self) -> str:
        """Defining dictionary representation of Subject object"""
        return {
            'id' : self.id,
            'name' : self.name,
        }

class Address(models.Model):
    """Defining attributes and methods for Address model"""
    first_line = models.CharField(max_length=255, null=False, blank=False)
    second_line = models.CharField(max_length=255, null=False, blank=True)
    city = models.CharField(max_length=255, null=False, blank=False)
    postcode = models.CharField(max_length=7, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    
    def __str__(self) -> str:
        """Defining string representation of Address model"""
        return f"{self.first_line} {self.city} {self.postcode}"
    

class Resource(models.Model):
    """Defining attributes and methods for Resource model"""
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    height = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2)
    width = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2)
    weight = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2)
    price = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2)
    stock = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2)
    estimated_delivery_time = models.DecimalField(max_digits=6, null=False, blank=False, decimal_places=2)
    subject = models.CharField(max_length=150, null=False, blank=False)
    author = models.CharField(max_length=150, null=False, blank=False)
    self_made = models.BooleanField(null=False, blank=False)
    is_draft = models.BooleanField(null=False, blank=False)
    unique = models.BooleanField(null=False, blank=False, default=True)
    allow_delivery = models.BooleanField(null=False, blank=False, default=False)
    allow_collection = models.BooleanField(null=False, blank=False, default=False)
    allow_return = models.BooleanField(null=False, blank=False, default=False)
    page_start = models.IntegerField(null=False, blank=True)
    page_end = models.IntegerField(null=False, blank=True)
    HEIGHT_UNITS: list [tuple[str, str]] = [('cm', 'cm'), ('m', 'm'), ('in', 'in')]
    height_unit = models.CharField(max_length=2, choices=HEIGHT_UNITS, null=False, blank=False)
    width_unit = models.CharField(max_length=2, choices=HEIGHT_UNITS, null=False, blank=False)
    image1 = models.ImageField(null=False, blank=False, upload_to='resource_images/')
    image2 = models.ImageField(null=False, blank=False, upload_to='resource_images/')
    video = models.FileField(upload_to='resource_videos/')
    upload_date = models.DateTimeField(default=timezone.now)
    last_edited = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(null=False, blank=True, default=0.0, max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing')

    WEIGHT_UNITS: list [tuple[str, str]] = [('lb', 'lb'), ('kg', 'kg'), ('ml', 'ml'), ('L', 'L'), ('mg', 'mg'), ('oz', 'oz')]
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNITS, null=False, blank=False)
    
    def clean(self) -> None | ValidationError:
        """Ensuring equal height and width units"""
        super().clean()
        if self.height_unit != self.width_unit:
            raise ValidationError('Height and width units must be the same')
   
    CURRENCIES: list [tuple[str, str]] = [('USD', 'USD'), ('GBP', 'GBP'), ('EUR', 'EUR')]
    price_currency = models.CharField(max_length=3, choices=CURRENCIES, default='GBP', null=False, blank=False)
    
    DELIVERY_UNITS: list [tuple[str, str]] = [('day', 'day'), ('minute', 'minute'),  
                                          ('hour', 'hour'), ('week', 'week'), 
                                          ('month', 'month')]
    estimated_delivery_units = models.CharField(max_length=7, choices=DELIVERY_UNITS, null=False, blank=False)
    
    TYPES: list [tuple[str, str]] = [('Textbook', 'Textbook'), ('Notes', 'Notes'), ('Stationery', 'Stationery')]
    type = models.CharField(max_length=10, choices=TYPES, null=False, blank=False)
    
    COLOURS: list [tuple[str, str]] = [('Black', 'Black'), ('Red', 'Red'), ('Yellow', 'Yellow'), 
                                       ('Pink', 'Pink'), ('Purple', 'Purple'), ('Green', 'Green'), 
                                       ('Blue', 'Blue'), ('White', 'White'), ('Orange', 'Orange'), 
                                       ('Brown', 'Brown'), ('Grey', 'Grey')]
    colour = models.CharField(max_length=6, choices=COLOURS, null=False, blank=False)
    
    SOURCES: list [tuple[str, str]] = [('AI', 'AI'), ('Internet', 'Internet'), ('None', 'None')]
    source = models.CharField(max_length=8, choices=SOURCES, null=False, blank=True)

    CONDITIONS: list [tuple[str, str]] = [('New', 'New'), ('Used', 'Used')]
    condition = models.CharField(max_length=4, choices=CONDITIONS, null=False, blank=False)

    MEDIUM: list [tuple[str, str]] = [('Online', 'Online'), ('Paper', 'Paper')]
    media = models.CharField(max_length=6, choices=MEDIUM, null=False, blank=True)

    def as_dict(self) -> str:
        """Defining dictionary representation of Resource object"""
        reviews = Review.objects.filter(resource=self.id)
        return {
            'id' : self.id,
            'name': self.name,
            'description': self.description,
            'height': self.height,
            'width': self.width,
            'weight': self.weight,
            'price': self.price,
            'stock': self.stock,
            'estimated_delivery_time': self.estimated_delivery_time,
            'subject': self.subject,
            'author': self.author,
            'self_made': self.self_made,
            'is_draft': self.is_draft,
            'page_start': self.page_start,
            'page_end': self.page_end,
            'height_unit': self.height_unit,
            'width_unit': self.width_unit,
            'image1': self.image1.url,
            'image2': self.image2.url,
            'video': self.video.url,
            'last_edited': self.last_edited,
            'weight_unit': self.weight_unit,
            'price_currency': self.price_currency,
            'estimated_delivery_units': self.estimated_delivery_units,
            'type': self.type,
            'rating': self.rating,
            'colour': self.colour,
            'source': self.source,
            'condition': self.condition,
            'media': self.media,
            'allow_delivery': self.allow_delivery,
            'allow_collection': self.allow_collection,
            'allow_return': self.allow_return,
            'user': self.user.id,
            'reviews': [review.as_dict() for review in reviews],
            'upload': self.upload_date,
            'unique': self.unique
        }    


class WishlistResource(models.Model):
    """Defining attributes and methods for WishlistResource model"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='wishlist_resource')
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_resource')
    
    def as_dict(self) -> str:
        """Defining dictionary representation of WishlistResource object"""
        return {
            'id' : self.id,
            'resource' : self.resource.id,
        }
    
    
class CartResource(models.Model):
    """Defining attributes and methods for CartResource model"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='cart_resource')
    number = models.IntegerField(null=False, blank=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_resource')
    
    def as_dict(self) -> str:
        """Defining dictionary representation of CartResource object"""
        return {
            'id' : self.id,
            'resource' : self.resource.id,
            'number' : self.number,
        }


class Review(models.Model):
    """Defining attributes and methods for Review model"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    rating = models.DecimalField(null=False, blank=True, default=0.0, max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    title = models.CharField(max_length=150, null=False, blank=False)
    review = models.TextField(null=False, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=False, blank=True, upload_to='review_images/')
    video = models.FileField(null=False, blank=True, upload_to='review_videos/')

    def as_dict(self) -> str:
        """Defining dicionary representation of Review object"""
        return {
            'id': self.id,
            'resource': self.resource.id,
            'user': self.user.id,
            'title' : self.title,
            'review': self.review,
            'rating': self.rating,
            'upload_date': self.upload_date,
            'image': self.image.url if self.image else None,
            'video': self.video.url if self.video else None,
        }
    

class Order(models.Model):
    """Defining attributes and methods for Order model"""
    STATUSES: list [tuple[str, str]] = [('Placed', 'Placed'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled'), ('Dispatched', 'Dispatched'), ('Complete', 'Complete'), ('Return Started', 'Return Started'), ('Return Received', 'Return Received'), ('Refunded', 'Refunded')]
    status = models.CharField(max_length=16, choices=STATUSES, default='Placed', null=False, blank=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    estimated_delivery_date = models.DateField(null=False, blank=False)
    date = models.DateField(null=False, blank=False, default=timezone.now)
    delivery_image = models.ImageField(null=False, blank=True, upload_to='delivery_images/')
    RETURN_METHODS: list [tuple[str, str]] = [('Delivery', 'Delivery'), ('Collection', 'Collection')]
    return_method = models.CharField(max_length=10, choices=RETURN_METHODS, default='Delivery', null=False, blank=False)
    is_exchange = models.BooleanField(null=False, blank=False, default=False)
    return_reason = models.TextField(null=False, blank=True)


    def as_dict(self) -> str:
        """Defining dictionary representation of Order object"""
        resources = OrderResource.objects.filter(order=self.id)
        return {
            'id': self.id,
            'status': self.status,
            'buyer': self.buyer.id,
            'seller': self.seller.id,
            'resources': [resource.as_dict() for resource in resources],
            'estimated_delivery_date': self.estimated_delivery_date,
            'date': self.date,
            'delivery_image': self.delivery_image.url if self.delivery_image else None,
            'return_method': self.return_method,
            'return_reason': self.return_reason,
            'is_exchange': self.is_exchange,
        }
    

class OrderResource(models.Model):
    """Defining attributes and methods for OrderResource model"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='resource')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_resource')
    number = models.IntegerField(null=False, blank=False)
    for_return = models.BooleanField(null=False, blank=False, default=False)
    number_for_return = models.IntegerField(null=False, blank=False, default=0)

    def as_dict(self) -> str:
        """Defining dictionary representation of OrderResource object"""
        return {
            'id': self.id,
            'resource': self.resource.id,
            'number_for_return': self.number_for_return,
            'for_return': self.for_return,
            'number': self.number,
        }


class Messages(models.Model):
    """Defining attributes and methods for Messages model"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    user1_seen = models.DateTimeField(default=timezone.now)
    user2_seen = models.DateTimeField(default=timezone.now)
    last_edited = models.DateTimeField(default=timezone.now)

    def as_dict(self) -> str:
        """Defining dictionary representation of Messages object"""
        messages = self.message.all()
        return {
            'id': self.id,
            'user1': self.user1.id,
            'user2': self.user2.id,
            'user1_seen': self.user1_seen,
            'user2_seen': self.user2_seen,
            'last_edited': self.last_edited,
            'messages': [message.as_dict() for message in messages],
        }


class Message(models.Model):
    """Defining attributes and methods for Message model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    message = models.TextField(null=False, blank=True)
    messages = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='message')
    sent = models.DateTimeField(default=timezone.now)

    def as_dict(self) -> str:
        """Defining dictionary representation of Message object"""
        return {
            'id': self.id,
            'user': self.user.id,
            'message': self.message,
            'sent': self.sent,
        }
    

class Exchange(models.Model):
    """Defining attributes and methods for Exchange model"""
    STATUSES: list [tuple[str, str]] = [('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')]
    status1 = models.CharField(max_length=10, choices=STATUSES, default='Pending', null=False, blank=False)
    status2 = models.CharField(max_length=10, choices=STATUSES, default='Pending', null=False, blank=False)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_user2')
    resource1 = models.ForeignKey(Resource, null=True, blank=False, on_delete=models.CASCADE, related_name='resource1')
    resource2 = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='resource2')
    resource1_number = models.IntegerField(null=False, blank=False, default=0)
    resource2_number = models.IntegerField(null=False, blank=False, default=0)

    def as_dict(self) -> str:
        """Defining dictionary representation of Exchange object"""
        return {
            'id': self.id,
            'status1': self.status1,
            'status2': self.status2,
            'user1': self.user1.id,
            'user2': self.user2.id,
            'resource1': self.resource1.id if self.resource1 else -1,
            'resource2': self.resource2.id,
            'resource1_number': self.resource1_number,
            'resource2_number': self.resource2_number,
        }
    

class SearchHistory(models.Model):
    """Defining model to store search history, aiding personalised recommendation and chatbot"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='search_history')

    def as_dict(self) -> str:
        """Defining dictionary representation of SearchHistory object"""
        search_history = SearchHistoryItem.objects.filter(search_history=self)
        return {
            'id': self.id,
            'user': self.user.id,
            'search_history': [search_history_item.as_dict() for search_history_item in search_history]
        }
    

class SearchHistoryItem(models.Model):
    """Defining single search"""
    search = models.TextField(null=False, blank=False)
    search_history = models.ForeignKey(SearchHistory, on_delete=models.CASCADE, related_name='search_item')

    def as_dict(self) -> str:
        """Defining dictionary representation of SearchHistoryItem object"""
        return {
            'id': self.id,
            'search': self.search,
            'search_history': self.search_history.id
        }
