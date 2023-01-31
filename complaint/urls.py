from django import views
from django.urls import path
from django.urls.conf import include
from django.views.decorators.csrf import csrf_exempt
from . import views
from .views import Complaints_log_api, print_record

urlpatterns = [
    # Sidebar
    path('', views.list_complaints, name="all_complaints"),
    path('in_progress/', views.inProgress_complaints, name="in_progress_complaints"), 
    path('unassigned/', views.unassigned_complaints, name="unassigned_complaints"), 
    path('closing_complaints/', views.closing_complaints, name="closing_complaints"), 
    path('closed_complaints/', views.closed_complaints, name="closed_complaints"),
    path('settings/', views.settings, name="c_settings"),
    
    # Engineer's Sidebar
    path('unresolved_comlaints', views.unresolved_complaints, name="unresolved_complaints"),
    path('resolved_comlaints', views.resolved_complaints, name="resolved_complaints"),

    # Pages
    path('new_complaint/', views.register_complaint, name="register_complaint"),
    path('update_complaint/<int:pk>', views.update_complaint, name="update_complaint"),
    path('view_complaint/<int:pk>/', views.view_complaint, name="view_complaint"),
    path('complaint_settings/<int:pk>/', views.complaint_settings, name="complaint_settings"),
    path('view_complaint_e/<int:pk>/', views.view_complaint_engg, name="view_complaint_engg"),

    path('add_checklist/<int:pk>', views.add_checklist, name="add_checklist"),
    path('update_checklist/<int:pk_cmp>/<int:pk_chk>/', views.update_checklist, name="update_checklist"),
    path('delete_checklist/<int:pk_cmp>/<int:pk_chk>/', views.delete_checklist, name="delete_checklist"),

    path('add_component/<int:pk_cmp>/', views.add_component, name="add_component"),
    path('add_component_manual/<int:pk_cmp>/', views.add_component_manual, name="add_component_manual"),
    path('update_component/<int:pk>/', views.update_component, name="update_component"),
    path('delete_component/<int:pk>', views.deleteComponent, name="delete_component"),
    path('list_components/<int:pk>/', views.list_components, name="list_components"),
    
    path('check_status/', views.check_complaint_status, name="check_complaint_status"),
    
    # Actions without pages
    path('search-complaint/', csrf_exempt(views.search_complaints_global), name = 'search-complaint_global'),
    path('set_complaint_stat/<int:pk>', views.set_complaint_status, name="set_complaint_status"),
    path('assign_engineer/<int:pk>', views.assign_engineer , name="assign_engineer"),
    path('delete_complaint/<int:pk>', views.deleteComplaint, name="delete_complaint"),
    path('reset_progress/<int:pk>', views.reset_complaint_progress , name="reset_complaint_progress"),
    path('complaints_log/', Complaints_log_api.as_view(), name="complaints_log"),
    path('close_complaint/<int:pk>', views.close_complaint, name="close_complaint"),
    path('print_record/<int:pk>', views.print_record, name="print_record"),
    #Export/Import
    path('export/', views.export_data, name="export_data"),
    path('import/', views.import_data, name="import_data"),

]
