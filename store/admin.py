from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display=['name', 'brand','quantity', 'unit_price','registred_on', 'registred_by']

admin.site.register(Product,ProductAdmin)