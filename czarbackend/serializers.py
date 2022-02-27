from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =  fields = '__all__'

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    profile = VendorProfileSerializer()
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = User
        optional_fields = ['profile']
        fields = ('first_name', 'last_name', 'email', 'password', 'profile')
        extra_kwargs = {"profile": {"required": False, "allow_null": True}}

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =  fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields =  fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =  fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields =  fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'