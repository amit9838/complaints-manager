from django import views
from django.urls import path
from django.urls.conf import include
from django.views.decorators.csrf import csrf_exempt
from . import views
from .views import Complaints_log_api, print_record

urlpatterns = [
    path('', views.list_complaints, name="all_complaints"),
    path('in_progress/', views.inProgress_complaints, name="in_progress_compaints"), 
    path('closing_complaints/', views.closing_complaints, name="closing_compaints"), 
    path('closed_complaints/', views.closed_complaints, name="closed_compaints"),
    path('new_complaint/', views.register_complaint, name="register_complaint"),
    path('add_checklist/<int:pk>', views.add_checklist, name="add_checklist"),
    path('update_checklist/<int:pk_cmp>/<int:pk_chk>/', views.update_checklist, name="update_checklist"),
    path('delete_checklist/<int:pk_cmp>/<int:pk_chk>/', views.delete_checklist, name="delete_checklist"),
    path('update_complaint/<int:pk>', views.update_complaint, name="update_complaint"),
    path('unresolved_comlaints', views.unresolved_complaints, name="unresolved_complaints"),
    path('resolved_comlaints', views.resolved_complaints, name="resolved_complaints"),
    path('view_complaint/<int:pk>/', views.view_complaint, name="view_complaint"),
    path('view_complaint_e/<int:pk>/', views.view_complaint_engg, name="view_complaint_engg"),
    path('add_component/<int:pk>/', views.add_component, name="add_component"),
    path('update_component/<int:pk>/', views.update_component, name="update_component"),
    path('search-complaint/', csrf_exempt(views.search_complaints_global), name = 'search-complaint_global'),
    path('set_complaint_stat/<int:pk>', views.set_complaint_status, name="set_complaint_status"),
    path('assign_engineer/<int:pk>', views.assign_enineer , name="assign_engineer"),
    path('complaints_log/', Complaints_log_api.as_view(), name="complaints_log"),
    path('close_complaint/<int:pk>', views.close_complaint, name="close_complaint"),
    path('print_record/<int:pk>', views.print_record, name="print_record"),
    path('check_status/', views.check_complaint_status, name="check_complaint_status"),
    path('delete_complaint/<int:pk>', views.deleteComplaint, name="delete_complaint"),
    path('delete_component/<int:pk>', views.deleteComponent, name="delete_component"),
]
