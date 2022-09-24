from django.contrib import admin
from .models import Product, Category
# Register your models here.

admin.site.register(Category)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display=['name', 'brand','category','quantity', 'unit_price','registred_on', 'registred_by']

admin.site.register(Product,ProductAdmin)