from django import views
from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('about/',views.about, name='about'),
    path('comments/<int:comp_pk>/', views.user_comment, name="user_comment"),
    path('delete_comment/<int:pk>/', views.delete_comment, name="delete_comment"),
    path('update_comment/<int:pk>/', views.update_comment, name="update_comment"),
    path('has_comments/<int:pk>/', views.has_comments, name="has_comments"),
    path('OTP_verification/<int:pk>/', views.OTP_verification, name="OTP_verification"),
]
