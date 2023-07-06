from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User Must Be an Email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.setdefault('is_staff') is not True:
            raise ValueError('Super user must be Staff !')
        if extra_fields.setdefault('is_active') is not True:
            raise ValueError('Superuser must be Active !')
        if extra_fields.setdefault('is_superuser') is not True:
            raise ValueError('super user must super user')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    fullname = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=10, blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fullname

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


class Sellar(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='sellar_profile')
    company_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.user_profile.fullname

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()
