from itertools import count
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from complaint.models import Complaint ,Item, ComplaintOTP
from user.models import *
from .models import *
from django. contrib.auth. decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
import requests

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
            recent_complaints = Complaint.objects.filter(assigned_to = user).order_by('-registred_date')[:5]

            total_complaint_assigned = complaints_assigned.count()
            pending_complaints = Complaint.objects.filter(complaint_status = 2, assigned_to = user).count()

            context = {
                "user":user,
                "complaints_assigned":complaints_assigned,
                "total_comlaints_assigned":total_complaint_assigned,
                "pending_complaints":pending_complaints,

            }
        return render(request, 'home/dashboard.html', context)
    return redirect('login')


def analytics(request):
    if request.method == 'GET':
        pass
    
def about(request):
    return render(request, 'home/about.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

class Anylitics_API(APIView):
    def get(self,request,format=None):
        if(request.user_is_superuser):
            items = Item.objects.all()
            total_earning = 0
            for item in items:
                total_earning = total_earning + item.unit_price + item.quantity
                
            data = {
                'total_earning' : total_earning 
            }
            return Response(data)
            

@login_required
def user_comment(request,comp_pk):
    complaint = Complaint.objects.get(id=comp_pk)
    if request.method == 'GET':
        comments = Comment.objects.filter(complaint = complaint)
        context = {
            "complaint":complaint,
            "comments":comments
        }
        return render(request, 'complaint/comments.html',context);

    if request.method == 'POST':
        message = request.POST['message'];
        if message:
            Comment.objects.create(complaint = complaint, user = request.user, user_comment = message)
            messages.success(request, 'Comment added successfully!')
            return redirect('user_comment', comp_pk)
        messages.warning(request, 'Please write something!')
        return redirect('user_comment', comp_pk)
    return redirect('user_comment', comp_pk)
        

def delete_comment(request,pk):
    if request.method == 'POST':
        comment = Comment.objects.get(id=pk)
        cmp_id = request.POST['cmp_id'];
        comment.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('user_comment', cmp_id)
    return redirect('dashboard')

def update_comment(request,pk):
    if request.method == 'POST':
        comment = Comment.objects.get(id=pk)
        cmp_id = request.POST['cmp_id'];
        user_msg= request.POST['message'];
        if request.user == comment.user:
            if not user_msg:
                messages.error(request, 'Please write something!')
                return redirect('user_comment', cmp_id)
            else:
                comment.user_comment = user_msg
                comment.save()
                messages.success(request, 'Updated successfully!')
                return redirect('user_comment', cmp_id)
        else:
            messages.error(request, "You don't have permission to edit this comment.")
            return redirect('user_comment', cmp_id)
    return redirect('dashboard')

import json
def has_comments(request,pk):
    complaint = Complaint.objects.get(id=pk)
    comments = Comment.objects.filter(complaint = complaint)
    count_comments = json.dumps(len(comments))
    return JsonResponse(count_comments,safe=False)


# OTP varification
import random
import pytz
from decouple import config


def OTP_verification(request,pk):
    complaint = Complaint.objects.get(id=pk)
    all_otps = ComplaintOTP.objects.filter(complaint = complaint)
    number = "+91"+str(complaint.customer_mob)

    if request.method == 'GET':
        expires_in= 30  #calculate time in minutes
        otp = random.randint(1001,9999)
        expiry_time = datetime.datetime.utcnow() +  datetime.timedelta(minutes=expires_in)
        expiry_time = expiry_time.replace(tzinfo=pytz.UTC)
        if len(all_otps) > 0:
            otp_obj = all_otps[0]
            print(otp_obj)
            otp_obj.otp = str(otp)
            otp_obj.expires_at = expiry_time
            otp_obj.save()
            response_code = sendSMS(number,otp)
            if response_code == 200:
                print("otp sent successfully :", otp)
                return JsonResponse({"message":"otp sent successfully!", "statuss":"success"},safe=False)
        else:
            print("otp sending")
            response_code = sendSMS(number,otp)
            if response_code == 200:
                ComplaintOTP.objects.create(complaint = complaint,otp = otp,expires_at = expiry_time)
                print("otp sent successfully :", otp)
                return JsonResponse({"message":"otp sent successfully!", "statuss":"success"},safe=False)
    
    if request.method == 'POST':
        recived_otp = request.POST['recived_otp']
        otp_obj = all_otps[0]
        if recived_otp == otp_obj.otp:  
            print(datetime.datetime.utcnow().replace(tzinfo=pytz.UTC))
            if  datetime.datetime.utcnow().replace(tzinfo=pytz.UTC) < otp_obj.expires_at:
                complaint.is_verified = True;
                otp = random.randint(10011,99991)
                otp_obj.otp = str(otp)
                otp_obj.save()
                complaint.save()
                messages.success(request, "Verification Successful!")
                return redirect('view_complaint',pk)
            messages.error(request, "OTP Expired!")
            return redirect('view_complaint',pk)
        print("otp not matched")
        messages.error(request, "Invalid OTP!")
    messages.error(request, "Incorrect OTP!")
    return redirect('view_complaint',pk)

def sendSMS(number,otp):
    api_key = config('API_KEY')
    try:
        response = requests.get(f"https://2factor.in/API/V1/{api_key}/SMS/{number}/{otp}/OTP1")
        return response.status_code
    except requests.RequestException as e:
        print(str(e))
        return None