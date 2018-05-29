from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


def index2(request):
    return render(request, "index-2.html")


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


def contact(request):
    return render(request, 'contact.html')


def login_signup(request):
    return render(request, 'login-signup.html')


def product_details(request):
    return render(request, 'product-details.html')


def product_grid(request):
    return render(request, 'product-grid.html')


def product_list(request):
    return render(request, 'product-list.html')


def support(request):
    return render(request, 'support.html')


@csrf_exempt
def email_subscribe(request):
    if request.method == "POST":
        pass