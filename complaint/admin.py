from dataclasses import fields
from django.contrib import admin

from user.models import Engineer
from .models import CheckList, Complaint, Item
# Register your models here.

admin.site.register(Complaint)
admin.site.register(CheckList)
admin.site.register(Item)

admin.site.site_header = "Marca Admin"
admin.site.site_title = "Marca Admin Area"
admin.site.index_title = "Welcome to the Marca Admin Area"

# class ItemInline(admin.TabularInline):
#     model = Item
#     extra = 1

# class ComplaintAdmin(admin.ModelAdmin):
#     model = Complaint
#     list_display=['get_product','registred_date', 'registred_by','assigned_to', 'complaint_status']
#     inlines= [ItemInline]

#     def get_product(self,obj):
#         return obj.product_name +"-"+obj.product_model +"(" +obj.customer_name+")"



# admin.site.register(Complaint, ComplaintAdmin)
# admin.site.register(Item)