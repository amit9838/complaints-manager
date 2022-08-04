from django.contrib import admin

from user.models import Employee,Engineer

# Register your models here.
admin.site.register(Employee)
admin.site.register(Engineer)