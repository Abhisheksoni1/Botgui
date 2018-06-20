import json

from django.contrib.auth import login, authenticate, logout
# import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
# from user.models import Profile

from bot.forms import *
from binance_feed.models import *
from binance_feed.api.binance import *


def index(request):
    return render(request, "index.html")


def dashboard(request):
    # print('1111')
    currency_pairs = History.objects.order_by('symbol').values_list('symbol', flat=True).distinct()
    # print(currency_pairs)
    # print(len(currency_pairs))

    return render(request, "dashboard.html", {'currency_pairs': currency_pairs})


def index3(request):
    return render(request, "index-3.html")


def services(request):
    return render(request, 'services.html')


def about(request):
    return render(request, 'about.html')


def error(request):
    return render(request, "404.html")


def blog_details(request):
    return render(request, 'blog-details.html')


def blog_list(request):
    return render(request, 'blog-list.html')


def cart(request):
    return render(request, 'cart.html')


def comming_soon(request):
    return render(request, 'comming-soon.html')


# def login_signup(request):
#     return render(request, 'login-signup.html')


def product_details(request):
    return render(request, 'product-details.html')


def product_grid(request):
    return render(request, 'product-grid.html')


def product_list(request):
    return render(request, 'product-list.html')


def support(request):
    return render(request, 'support.html')


def logout_view(request):
    logout(request)
    return login_signup(request)


def login_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # profile_form = ProfileInlineFormset(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                user.email = form.cleaned_data.get('email')
                user.save()
                login(request, user)
                # print(user)
                return redirect('dashboard')
        else:
            # print(form.errors)
            msg = 'Please check your details!'

            if 'username' in form.errors:
                msg = 'username already exist'

            if 'password2' in form.errors:
                msg = 'Password didn\'t match'

            return render(request, 'login-signup.html', {'registerErrorMsg': msg, 'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'login-signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login-signup.html', {'loginErrorMsg': 'username password not match', 'form': form})
    else:
        form = LoginForm()

    return render(request, 'login-signup.html', {'form': form})


@csrf_exempt
def email_subscribe(request):
    if request.method == "POST":
        form = EmailSubscribeForm(request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            return HttpResponseRedirect('/index/')
        # except Exception as e:
        # print(e)
        # else:
    # # print('')
    return render(request, 'index.html', {'form': form})


@csrf_exempt
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # print('valid')
            form.save()
            return HttpResponseRedirect('/index/')
        # except Exception as e:
        # print(e)
        # else:
    # # print('')
        return HttpResponseRedirect('/contact/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})



