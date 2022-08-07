from itertools import count
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from complaint.models import Complaint
from user.models import *
from django. contrib.auth. decorators import login_required
from django.db.models import Count

def home(request):
    return redirect('dashboard')

@login_required()
def dashboard(request):
    if request.method == "GET":
        all_complaints = Complaint.objects.all()
        recent_complaints = Complaint.objects.all().order_by('-registred_date')[:5]
        tatal_complaints = Complaint.objects.all().count()
        pending_complaints = Complaint.objects.filter(complaint_status = 1).count()
        daily_complaints = Complaint.objects.values('registred_date').annotate(count=Count('id')).order_by('-registred_date')
        compLastMonth = Complaint.objects.values('registred_date').annotate(count=Count('id')).order_by('-registred_date')[0:30]
        for x in compLastMonth:
            print(x)
            
        user = request.user
        # print(daily_complaints)
        if user.is_superuser:
            last_emp = User.objects.last()
            no_of_emp = Employee.objects.count()

            engineers = Engineer.objects.all()
            no_of_engg = Engineer.objects.count()
            context = {
                "user":user,
                "recent_emp": last_emp,
                "tatal_complaints":tatal_complaints,
                "recent_complaints":recent_complaints,
                "engg": engineers,
                "no_of_emp":no_of_emp,
                "no_of_engg":no_of_engg,
                "pending_complaints":pending_complaints
            }
            
            

        elif user.is_staff:
            
            comp_registered_by_emp = Complaint.objects.filter(registred_by = user)
            total_components_registered_by_emp = Complaint.objects.filter(registred_by = user).count()
            
            context = {
                "user":user,
                "comp_registred":comp_registered_by_emp,
                "total_complaints":total_components_registered_by_emp,
                "recent_complaints":recent_complaints,
                "pending_complaints":pending_complaints,

            }

        else:
            complaints_assigned = Complaint.objects.filter(assigned_to = user)
            total_complaint_assigned = Complaint.objects.filter(assigned_to = user).count()
            context = {
                "user":user,
                "complaints_assigned":complaints_assigned,
                "total_comlaints_assigned":total_complaint_assigned,
                "pending_complaints":pending_complaints
            }
        return render(request, 'home/dashboard.html', context)


def analytics(request):
    pass