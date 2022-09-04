from itertools import product
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import *



# Create your views here.

def store(request):
    user = request.user
    product = Product.objects.all()
    if(not user.is_superuser):
        return  HttpResponse("You can't access this page",{'product':product})

    return render(request, 'store/store.html')
