from itertools import product
from math import prod
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import *
from django.db.models import Count



# Create your views here.

def store(request):
    user = request.user
    if(not user.is_superuser):
        return  HttpResponse("You can't access this page")

    product = Product.objects.all()
    low_stock = Product.objects.filter(quantity__lte=20).count()
    products_count=0
    total_value=0
    for i in product:
        products_count+=i.quantity
        total_value+=i.quantity*i.unit_price
    recent_products = product[0:5]
    all_items_group = product.count()
    category_cnt = Product.objects.values('category').annotate(count = Count('id'))
    print(category_cnt)
    context = {
        'product':recent_products,
        'low_stock':low_stock,
        'all_items_group':all_items_group,
        'products_count':products_count,
        'total_value':total_value,
        'category_cnt':category_cnt.count()
    }
    return render(request, 'store/store.html',context)


def all_products(request):
    product = Product.objects.all()
    user = request.user
    if(not user.is_superuser):
        return  HttpResponse("You can't access this page")
    return render(request, 'store/all_products.html',{'product':product})
