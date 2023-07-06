from django.urls import path
from . import views

app_name = 'App_order'

urlpatterns = [
    path('add_to_cart/<pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('increase/<pk>/', views.increase_quantity, name='increase'),
    path('decrease/<pk>/', views.decrease_quantity, name='decrease'),
    path('remove_item/<pk>/', views.remove_item, name='remove_item')
]
