from datetime import datetime
from math import prod
from socket import J1939_PGN_ADDRESS_COMMANDED
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from store.forms import NewProductFrom
from django.core.paginator import Paginator
from .models import *
from django.db.models import Count
from django.contrib import messages
import json


# Store Page (Start) ---------------------------------------------
def store(request):
    user = request.user
    if(not user.is_superuser):
        return  HttpResponse("You can't access this page")

    product = Product.objects.all()
    low_stock = Product.objects.filter(quantity__lte=10).count()
    mock_stock = Product.objects.filter(quantity__gte=30).count()
    zero_stock = Product.objects.filter(quantity=0).count()
    products_count=0
    total_value=0
    for i in product:
        products_count+=i.quantity
        total_value+=i.quantity*i.unit_price
    recent_products = product.order_by('-registred_on')[0:5]
    all_items_group = product.count()
    category_cnt = Product.objects.values('category').annotate(count = Count('id'))
    cat_lst = []
    for i in category_cnt:
        cat_lst.append(i)

    cat_list_json = json.dumps(cat_lst)
    context = {
        'recent_product':recent_products,
        'zero_stock':zero_stock,
        'low_stock':low_stock,
        'mock_stock':mock_stock,
        'all_items_group':all_items_group,
        'products_count':products_count,
        'total_value':total_value,
        'category_cnt':category_cnt.count(),
        'cat_list':cat_list_json
    }
    return render(request, 'store/store.html',context)


def search_product(request):
    # if(request.method=='GET'):
    #     res = Product.objects.all();
    #     data = res.values();
    #     return JsonResponse(list(data),safe=False)

    if (request.method =='POST'):
        search_str = json.loads(request.body).get('searchText')
        with_p_name = Product.objects.filter(name__icontains = search_str)
        with_p_brand = Product.objects.filter(brand__icontains = search_str)
        with_p_cat = Product.objects.filter(category__istartswith = search_str)
        with_p_desc = Product.objects.filter(desc__icontains = search_str)
        res = with_p_name | with_p_brand | with_p_cat | with_p_desc
        data = res.values();
        return JsonResponse(list(data),safe=False)

# Store Page (end) ---------------------------------------------


# Register New Product -------------------------------------------------
def new_product(request):
    # product = Product.objects.all()
    user = request.user
    if(not user.is_superuser):
        return  HttpResponse("You can't access this page")
    
    cat = Category.objects.all()
    categories = []
    for item in cat:
        categories.append(item.name)
    cats = json.dumps(categories)

    if request.method=='GET':
        form = NewProductFrom()
        
        context = {
            'form':form,
            'categories':cats
        }
        return render(request, 'store/new_product.html',context)
    if request.method=='POST':
        formObj = NewProductFrom(request.POST)
        cat = request.POST['category']
        if formObj.is_valid():
            form_staging = formObj.save(commit=False)
            form_staging.category = cat
            form_staging.registred_by = user
            form_staging.registred_on = datetime.now()
            form_staging.save()
            messages.success(request,'Product added successfully')
            return redirect('all_products')
        else:
            context = {
            'form':formObj,
            'categories':cats
            }
            messages.error(request,'Invalid Input!')
            return render(request, 'store/new_product.html',context)


def update_product(request,pk):
    # product = Product.objects.all()
    user = request.user
    product = Product.objects.get(id = pk)
    p_cat = product.category

    if(not user.is_superuser):
        return  HttpResponse("You can't access this page")
    
    cat = Category.objects.all()
    categories = []
    for item in cat:
        categories.append(item.name)
    cats = json.dumps(categories)

    form = NewProductFrom(instance=product)
    if request.method=='GET':
        context = {
            'form':form,
            'categories':cats,
            'product':product,
            'p_cat':p_cat
        }
        return render(request, 'store/update_product.html',context)
    if request.method=='POST':
        formObj = NewProductFrom(request.POST,instance=product)
        cat = request.POST['category']
        if formObj.is_valid():
            form_staging = formObj.save(commit=False)
            form_staging.category = cat
            form_staging.registred_by = user
            form_staging.registred_on = datetime.now()
            form_staging.save()
            messages.success(request,'Product updated successfully')
            return redirect('view_product',pk)
        else:
            context = {
            'form':formObj,
            'categories':cats,
            'product':product,
            'p_cat':p_cat
            }
            messages.error(request,'Invalid Input!')
            return render(request, 'store/update_product.html',context)



def delete_product(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    messages.success(request,f'{product.name} deleted successfully!')
    return redirect('all_products')
# View All Products -------------------------------------------------
def all_products(request):
    user = request.user
    if(not user.is_superuser):
        return  HttpResponse("You can't access this page")
    all_product = Product.objects.all().order_by('-registred_on')
    paginator = Paginator(all_product,50)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'product':all_product,
        'page_obj':page_obj
    }
    return render(request, 'store/all_products.html',context)

def view_product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'store/view_product.html',{'product':product})


def low_stock_products(request):
    user = request.user
    if(not user.is_superuser):
        return HttpResponse("You can't access this page.")

    low_stock_p = Product.objects.filter(quantity__lte=10)
    return render(request, 'store/low_stock.html',{'low_stock_p':low_stock_p})

def zero_stock_products(request):
    user = request.user
    if(not user.is_superuser):
        return HttpResponse("You can't access this page.")

    zero_stock_p = Product.objects.filter(quantity__lte=1)
    return render(request, 'store/zero_stock.html',{'zero_stock_p':zero_stock_p})

# Settings Page (start) ----------------------------------------
def settings(request):
    user = request.user
    if(not user.is_superuser):
        return  HttpResponse("You can't access this page")
    
    categories = Category.objects.all()
    context = {
        'categories':categories
    }

    return render(request, 'store/settings.html',context)

def add_category(request):
    if request.POST:
        name = request.POST['cat_name']
        obj = Category(name=name)
        if(len(name.strip())>0):
            obj.save()
            return redirect('settings')
        else:
            messages.error(request,'Invalid input!')
            return redirect('settings')
    return redirect('settings')

def update_category(request,pk):
    if request.method == "POST":
        new_name = request.POST['cat_name']
        x = new_name
        obj = Category.objects.get(id=pk)
        if(len(x.strip())>0):
            obj.name = new_name
            obj.save()
            print('category updated')
            messages.success(request,'Category Updated successfully!')
            return redirect('settings')
        else:
            messages.error(request,'Invalid input!')
            return redirect('settings')
    return redirect('settings')


def delete_category(request,pk):
    if request.POST:
        cat = Category.objects.get(id=pk)
        cat.delete()
        return redirect('settings')
    return redirect('settings')
# Settings page (end) -------------------------------------------