from django.urls import path
from . import views

app_name = 'App_shop'

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('', views.all_product, name='home'),
    path('product_details/<pk>/', views.product_details, name='product_details'),
    path('sellar_product/',views.view_sellar_product,name='sellar_product')
]
