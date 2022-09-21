from django import views
from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('',views.store, name='store'),
    path('all-products/',views.all_products, name='all_products')
]
