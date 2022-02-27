from django.db import models
from django.contrib.auth.models import User
import uuid
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.conf import settings

CATEGORIES= (
    ('Arts and Craft','Arts & Craft'),
    ('Beauty and Wellness','Beauty & Wellness'),
    ('Books and Publishers','Books & Publishers'),
    ('Electronics','Electronics'),
    ('Fashion and Clothing','Fashion & Clothing'),
    ('Food and Drinks','Food & Drinks'),
    ('Jewelry and Accessories','Jewelry & Accessories'),
    ('Kids and Babies','Kids & Babies'),
    ('Pets and Animals','Pets & Animals'),
    ('Sports and Outdoors','Sports & Outdoors'),
    ('Hardware','Hardware'),
)

GENDER = (
    ('Male','MALE'),
    ('Female','FEMALE'),
    ('Other','OTHER'),
)


class Store(models.Model):
   name = models.CharField(max_length=254, default='')
   location = models.CharField(max_length=55)
   image = CloudinaryField('image')
   vendor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='location')
   category  = models.CharField(choices=CATEGORIES, max_length=55, default='')

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    business_name = models.CharField(max_length=150, null=True, blank=True)
    phone_number = PhoneNumberField(null = True, blank = True)
    gender = models.CharField(choices=GENDER, max_length=55)
    location = models.CharField(max_length=55)
    bio = models.TextField(max_length=120, null=True)
    avatar = CloudinaryField('image')
    youtube = models.URLField(max_length=250, null=True, blank=True)
    facebook = models.URLField(max_length=250, null=True, blank=True)
    linkedin = models.URLField(max_length=250, null=True, blank=True)
    twitter = models.URLField(max_length=250, null=True, blank=True)
    instagram = models.URLField(max_length=250, null=True, blank=True)
    website = models.URLField(max_length=250, null=True, blank=True)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def save_image(self):
        self.save()      
        
    def delete_image(self):
        self.delete()
        
    def get_product_no(self, username):
        user = get_object_or_404(User, username=username)
        return Product.objects.filter(user=user).count()
    
    def get_product(self, username):
        user = get_object_or_404(User, username=username)
        return Product.objects.filter(user=user)
    
    @classmethod
    def update(cls, id, value):
        cls.objects.filter(id=id).update(avatar=value)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=254, default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = CloudinaryField('image')
    # category_image = CloudinaryField('image')
    category  = models.CharField(choices=CATEGORIES, max_length=55, default='')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
    def save_image(self):
        self.save()
        
    @classmethod
    def search_products(cls,search_term):
        items = Product.objects.filter(product_name__icontains=search_term)
        return items
        
    def delete_image(self):
        self.delete()  
        
    def no_of_rating(self):
        ratings = Rating.objects.filter(project=self)
        return len(ratings)
    

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_details")
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    total = models.IntegerField(default=0)
    numincart = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="cart")

    def __str__(self):
        return self.username

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product 


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='rater_user')
    score = models.IntegerField(default=0, validators= [MaxValueValidator(5), MinValueValidator(1)])
    
    def __str__(self):
        return self.product.title

class Review(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='post_comment')
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='user_ratings')
    purchased = models.BooleanField(default=False)
    
    # class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='rater_user')
    score = models.IntegerField(default=0, validators= [MaxValueValidator(5), MinValueValidator(1)])
    
    def __str__(self):
        return self.product.title

class Review(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='post_comment')
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='user_ratings')
    purchased = models.BooleanField(default=False)
    
    

 