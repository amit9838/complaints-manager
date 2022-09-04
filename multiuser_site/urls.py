from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('',include('home.urls')),
    path('user/',include('user.urls')),
    path('store/',include('store.urls')),
    path('complaint/',include('complaint.urls')),
]
