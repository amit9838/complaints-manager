from django import views
from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('about/',views.about, name='about'),
    path('comments/<int:pk>/', views.user_comment, name="user_comment"),
    path('delete_comment/<int:pk>/', views.delete_comment, name="delete_comment"),
]
