from django.contrib import admin
from django.conf import settings
from .models import User, Profile, Sellar

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''Admin View for User'''

    list_display = ['id','email']
    list_per_page = 10


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for Profile'''

    list_display = ('id', 'user', 'fullname', 'phone',
                    'zip_code', 'city', 'country')
    list_per_page = 10

@admin.register(Sellar)
class SellarAdmin(admin.ModelAdmin):
    '''Admin View for Sellar'''

    list_display = ('id','user','company_name')
    