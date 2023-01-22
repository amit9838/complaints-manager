from typing import final
from django.contrib import admin

from user.models import Engineer
from .models import CheckList, Complaint, Item
# Register your models here.

# admin.site.register(Complaint)
# admin.site.register(CheckList)
admin.site.register(Item)

admin.site.site_header = "Marca Admin"
admin.site.site_title = "Marca Admin Area"
admin.site.index_title = "Welcome to the Marca Admin Area"

# class ItemInline(admin.TabularInline):
#     model = Item
#     extra = 1

class ComplaintAdmin(admin.ModelAdmin):
    model = Complaint
    list_display=['product', 'id', 'registred_By','assigned_To', 'complaint_status']
    # inlines= [ItemInline]

    def product(self,obj):
        return obj.brand.upper()+ "-" +obj.model_no  +" (" +obj.customer_name+")"


    def registred_By(self, obj):
        return str(obj.registred_by) + "  (" + str(obj.registred_date) + ")"

    def assigned_To(self, obj):
        if str(obj.assigned_to) != "None" and  str(obj.assigned_date) != "None":
            return str(obj.assigned_to) + " (" + str(obj.assigned_date) + ")"
        else:
            return "-"

admin.site.register(Complaint, ComplaintAdmin)