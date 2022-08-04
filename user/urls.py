from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
from .views import LoginView, LogoutView

urlpatterns = [
    path('employee_register/',views.employee_register,name='employee_register'),
    path('engineer_register/',views.engineer_register,name='engineer_register'),
    path('login/',LoginView.as_view(), name = "login"),
    path('logout/',LogoutView.as_view(), name = "logout"),
    path('profile/<int:pk>',views.profile, name = "profile"),
    path('complete_profile_emp/',views.complete_emp_profile, name = "complete_employee_profile"),
    path('complete_profile/',views.complete_engg_profile, name = "complete_engineer_profile"),
    path('staff/',views.list_staff, name = "list_staff"),
]
