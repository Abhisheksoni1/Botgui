from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


@csrf_exempt
def email_subscribe(request):
    if request.method == "POST":
        pass