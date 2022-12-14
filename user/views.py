from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django. contrib.auth. decorators import login_required


# Create your views here.
@login_required
def profile(request,pk):
    user_passed = User.objects.get(id=pk)
    user = request.user
    context = {
        "user_passed":user_passed,
        "user":user
    }
    if user_passed.is_superuser:
        return render(request, 'user/profile.html',context)

    if user_passed.is_staff and user_passed.is_superuser == False:
        emp = Employee.objects.get(user=user_passed)
        context = {
            "user_passed":user_passed,
            "emp":emp,
            "user":user
        }
        # print(vars(emp))
        # print(emp.joinDate)
        return render(request, 'user/profile.html',context)
    else:
        engg = Engineer.objects.get(user=user_passed)
        context = {
            "user_passed":user_passed,
            "engg":engg,
            "user":user
        }
        return render(request, 'user/profile.html',context)



def update_profile(request,pk):
    if request.method == "GET":
        user_passed = User.objects.get(id=pk)
        context = {
            "user_passed":user_passed
        }
        if user_passed.is_superuser:
            return render(request, 'user/update_profile.html',context)

        if user_passed.is_staff and user_passed.is_superuser == False:
            emp = Employee.objects.get(user=user_passed)
            context = {
                "user_passed":user_passed,
                "emp":emp
            }
            # print(vars(emp))
            # print(emp.joinDate)
            return render(request, 'user/update_profile.html',context)
        else:
            engg = Engineer.objects.get(user=user_passed)
            context = {
                "user_passed":user_passed,
                "engg":engg
            }
            return render(request,'user/update_profile.html',context)
    if request.method == "POST":
        user_passed = User.objects.get(id=pk)
        u_name = request.POST['username']
        u_email = request.POST['email']
        f_name = request.POST['firstname']
        l_name = request.POST['lastname']
        context = {
            "user_passed":user_passed
        }
        if user_passed.is_superuser:
            if u_name and u_email and f_name and l_name:
                user_passed.username = u_name
                user_passed.email = u_email
                user_passed.first_name = f_name
                user_passed.last_name = l_name
                user_passed.save()
            else:
                messages.error(request, "Please provide valid input!")
                return render(request, 'user/update_profile.html',context)
            messages.success(request, "Profile updated Successfully!")
            return render(request,'user/profile.html',context)

        if user_passed.is_staff and user_passed.is_superuser == False:
            emp = Employee.objects.get(user=user_passed)
            u_add = request.POST['address']
            mobile = request.POST['mobile']
            context = {
                    "user_passed":user_passed,
                    "emp":emp
                }
            if u_name and u_email and f_name and l_name and u_add:
                user_passed.username = u_name
                user_passed.email = u_email
                user_passed.first_name = f_name
                user_passed.last_name = l_name
                user_passed.save()
            if u_add and mobile:
                emp.address = u_add
                emp.mob = mobile
                emp.save()
            else:
                messages.error(request, "Please provide valid input!")
                return render(request, 'user/update_profile.html',context)
            messages.success(request, "Profile updated Successfully!")
            return render(request,'user/profile.html',context)
        if not user_passed.is_staff:
            engg = Engineer.objects.get(user=user_passed)
            u_add = request.POST['address']
            exp = request.POST['expertise']
            mobile = request.POST['mobile']
            context = {
                "user_passed":user_passed,
                "engg":engg
            }

            if u_name and u_email and f_name and l_name:
                user_passed.username = u_name
                user_passed.email = u_email
                user_passed.first_name = f_name
                user_passed.last_name = l_name
                user_passed.save()
            if u_add and exp and mobile:
                engg.address = u_add
                engg.expertise = exp
                engg.mob = mobile
                engg.save()
            else:
                messages.error(request, "Please provide valid input!")
                return render(request,'user/update_profile.html',context)
            messages.success(request, "Profile updated Successfully!")
            return render(request,'user/profile.html',context)
        

def employee_register(request):
    if request.method == "GET":
        return render(request, 'user/employee_register.html',{'form':UserRegisterForm})
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.is_staff = True
            form1.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(username = username, password = password)
            login(request,new_user)
            new_emp = Employee.objects.create(user = request.user)
            new_emp.save()
            return redirect('complete_employee_profile')
        return render(request, 'user/employee_register.html',{'form':form})
    

@login_required
def complete_emp_profile(request):
    user = request.user
    if request.method == "GET":
        form = CompleteEmployeeProfile()
        user = request.user
        return render(request,'user/complete_employee_profile.html',{"user":user, "form":form})

    if request.method == "POST":
        if user.is_staff and user.is_superuser == False:
            emp = Employee.objects.get(user=user)
            form = CompleteEmployeeProfile(request.POST, instance=emp)
            form.save()
            messages.success(request,f'Welcome {user.first_name}')
            return redirect('dashboard')
        else:
            return render(request,'user/complete_employee_profile.html',{"user":user, "form":form})
    else:
        return render(request,'user/complete_employee_profile.html',{"user":user, "form":form})




def engineer_register(request):
    if request.method == "GET":
        return render(request, 'user/engineer_register.html',{'form':UserRegisterForm})
    
        
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(username = username, password = password)
            login(request,new_user)
            new_engg = Engineer.objects.create(user = request.user)
            new_engg.save()
            return redirect('complete_engineer_profile')
        return render(request, 'user/engineer_register.html',{'form':form})

    
@login_required
def complete_engg_profile(request):
    user = request.user
    if request.method == "GET":
        form = CompleteEngineerProfile()
        user = request.user
        return render(request,'user/complete_engineer_profile.html',{"user":user, "form":form})

    if request.method == "POST":
        engg = Engineer.objects.get(user=user)
        form = CompleteEngineerProfile(request.POST, instance=engg)
        form.save()
        messages.success(request,f'Welcome {user.first_name}')
        return redirect('dashboard')
    else:
        return render(request,'user/complete_engineer_profile.html',{"user":user, "form":form})

@login_required
def list_staff(request):
    if request.user.is_superuser:
        all_users = User.objects.all()
        admins_id = [user.id for user in all_users if user.is_superuser]
        admins = all_users.filter(id__in = admins_id)

        employees  = Employee.objects.all()
        engineers = Engineer.objects.all()


        context = {
            'admins':admins,
            'employees':employees,
            'engineers':engineers
        }
        return render(request, 'user/staff.html',context)
    else:
        return HttpResponse("You don't have permission to view this page!")



class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('dashboard')

        else:
            return render(request,'user/login.html')


    def post(self,request):
        u_name = request.POST['username']
        u_pass = request.POST['password']

        if u_name and u_pass:
            user = authenticate(username = u_name, password = u_pass)
            print(user)

            if user:
                login(request,user)
                messages.success(request,f'Welcome {user.first_name}! Great to see you again')
                return redirect('dashboard')
                    
            messages.error(request,'Invalid credentials! please try again.')
            return render(request,'user/login.html')

        messages.error(request,'Invalid credentials! please try again.')
        return render(request,'user/login.html')


class LogoutView(View):
    def post(self,request):
        logout(request)
        return redirect('login')



       