from django.urls import path
from . import views

app_name = 'App_login'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('sellar/', views.create_sellar, name='sellar'),
    path('password_change/', views.password_change, name='password_change')
]
