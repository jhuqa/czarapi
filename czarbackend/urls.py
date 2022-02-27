from django.urls import path 
from . import views           

urlpatterns = [
    path('', views.index),
    path('product/', views.products_list),
    path('product/<int:pk>', views.product_detail),
    path('order/', views.orders_list),
    path('order/<int:pk>', views.order_detail),
    path('orderitem/', views.orderitem_list),
    path('orderitem/<int:pk>', views.orderitem_detail),
    path('cart/', views.cart_list),
    path('cart/<int:pk>', views.cart_detail),
    path('customer/', views.customer_list),
    path('customer/<int:pk>', views.customer_detail),
]