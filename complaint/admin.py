from django.contrib import admin

from user.models import Engineer
from .models import Complaint, Item
# Register your models here.
from django.contrib.admin import SimpleListFilter



class ComplaintAdmin(admin.ModelAdmin):
    model = Complaint
    list_display=['get_product','registred_date', 'registred_by','assigned_to', 'complaint_status']

    def get_product(self,obj):
        return obj.product_name +"-"+obj.product_model +"(" +obj.customer_name+")"



admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Item)