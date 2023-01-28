from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
from .views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('employee_register/',views.employee_register,name='employee_register'),
    path('engineer_register/',views.engineer_register,name='engineer_register'),
    path('login/',LoginView.as_view(), name = "login"),
    path('logout/',LogoutView.as_view(), name = "logout"),
    path('profile/<int:pk>',views.profile, name = "profile"),
    path('update_profile/<int:pk>',views.update_profile, name = "update_profile"),
    path('complete_profile_emp/',views.complete_emp_profile, name = "complete_employee_profile"),
    path('complete_profile/',views.complete_engg_profile, name = "complete_engineer_profile"),
    path('staff/',views.list_staff, name = "list_staff"),

    # Password reset
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='user/password_reset.html'
        ),
        name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ),
         name='password_reset_complete'),    
]
