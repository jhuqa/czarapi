from django.contrib import admin

from django.contrib import admin
from czarbackend.models import Product

class ProductAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Product, ProductAdmin)
