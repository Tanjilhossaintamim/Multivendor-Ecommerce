from django.urls import path
from . import views

app_name = 'App_payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.payment, name='pay'),
    path('compleate/', views.compleat, name='compleate'),
    path('purchased/<tran_id>/<val_id>/',
         views.purchased, name='purchased'),
    path('order/', views.order, name='order')
]
