from django import views
from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
]
