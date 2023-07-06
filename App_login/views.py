from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import SignUpForm, ProfileForm, SellarForm
from .models import Profile, Sellar

# Create your views here.


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Account Created Successfully !')
            return HttpResponseRedirect(reverse('App_login:login'))

    return render(request, 'App_login/signup.html', context={'form': form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successfull !')
                return HttpResponseRedirect(reverse('App_shop:home'))

    return render(request, 'App_login/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_login:login'))


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=profile)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.user = request.user
            user_form.save()
            form = ProfileForm(instance=profile)
            messages.success(request, 'Information Save Successfully !')

    return render(request, 'App_login/profile.html', context={'form': form})


@login_required
def create_sellar(request):
    SellerProfile = Sellar.objects.filter(user=request.user)
    user_profile = Profile.objects.filter(user=request.user)
    form = SellarForm()
    if user_profile[0].is_fully_filled():
        if not SellerProfile:
            if request.method == 'POST':
                form = SellarForm(data=request.POST)
                if form.is_valid():
                    sellar_form = form.save(commit=False)
                    sellar_form.user = request.user
                    sellar_form.save()
                    messages.success(
                        request, 'Congratulations ! You Are Our Sellar Now')
                    return HttpResponseRedirect(reverse('App_shop:home'))
        else:
            messages.warning(request, 'You Already a Sellar !')
            return HttpResponseRedirect(reverse('App_shop:home'))

    else:
        messages.warning(request, 'Please fillup Your Profile Information !')
        return HttpResponseRedirect(reverse('App_login:profile'))

    return render(request, 'App_login/sellar.html', context={'form': form})


@login_required
def password_change(request):
    form = PasswordChangeForm(instance=request.user)

    return render(request, 'App_login/password_change.html', context={'form': form})
