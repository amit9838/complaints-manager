from django import views
from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [ 
    path('',views.store, name='store'),
    path('settings/',views.settings, name='settings'),
    path('add-category/',views.add_category, name='add_category'),
    path('search-product/',views.search_product, name='search_product'),
    path('delete-category/<int:pk>/',views.delete_category, name='delete_category'),
    path('update-category/<int:pk>/',views.update_category, name='update_category'),
    path('all-products/',views.all_products, name='all_products'),
    path('view-product/<int:pk>/',views.view_product, name='view_product'),
    path('low-stock-products/',views.low_stock_products, name='low_stock_products'),
    path('zero-stock-products/',views.zero_stock_products, name='zero_stock_products'),
    path('new-product/',views.new_product, name='new_product'),
]
