from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from user.models import *
import json


# Requires Customer data to crate complaint id 
@login_required
def register_complaint(request):
    if(request.user.is_staff):
        form_cmp  = ComplaintRegisterForm()
        context = {
                
                'complaint_register_form':form_cmp,
            }
        if request.method == "GET":
            return render(request, 'complaint/new_complaint.html',context) 
        if request.method == "POST":
            form_cmp = ComplaintRegisterForm(request.POST)
            cat = request.POST['category']
            if form_cmp.is_valid():
                formdata = form_cmp.save(commit=False)
                formdata.registred_by = request.user
                formdata.complaint_status = 1;
                formdata.category = cat
                formdata.save()
                obj = form_cmp.instance
                messages.success(request, 'Complaint has been successfully registred.')
                return redirect('add_checklist',obj.id)
            messages.error(request, 'Complaint not registred! Please provide valid input.')
            return render(request, 'complaint/new_complaint.html',context)
    else:
        return HttpResponse("You dont't have permission to access this page")


# Using above complaint id to attach product checklist of  the the product.
def add_checklist(request, pk):
    complaint = Complaint.objects.get(id=pk)
    if request.method == 'GET':
        check_list = CheckList.objects.filter(complaint = complaint)
        # print(complaint.get_fields())
        return render(request, 'complaint/add_checklist.html', {'complaint':complaint, 'check_list':check_list})

    if request.method == 'POST':
        key = request.POST['key']
        val = request.POST['val']
        obj = CheckList(complaint = complaint, c_list_key = key, c_list_val = val)
        print("adding to list...")
        if obj:
            obj.save()
            print("Added successfully..")
            messages.success(request, 'Checklist Updated')
            return redirect('add_checklist',pk)
        messages.error(request, 'Could not add!')

def update_checklist(request, pk_cmp,pk_chk):
    complaint = Complaint.objects.get(id=pk_cmp)
    if request.method == 'GET':
        check_list= CheckList.objects.get(id = pk_chk)
        # print(check_list)
        return render(request, 'complaint/add_checklist.html', {'complaint':complaint, 'check_list':check_list})

    if request.method == 'POST':
        key = request.POST['key']
        val = request.POST['val']
        check_list_mod = CheckList.objects.get(id = pk_chk)
        if(key and val):
            check_list_mod.c_list_key = key
            check_list_mod.c_list_val = val   
            check_list_mod.save()     
            print("Updated successfully..")
            messages.success(request, 'Checklist Updated')
            return redirect('add_checklist',pk_cmp)
        messages.error(request, 'Could not add!')


def delete_checklist(request, pk_cmp,pk_chk):
    list_item = CheckList.objects.get(id=pk_chk)
    list_item.delete()
    print("Checklist item deleted successfully..")
    messages.error(request, 'Checklist item deleted successfully')
    return redirect('add_checklist',pk_cmp)


@login_required
def update_complaint(request,pk):
    if(request.user.is_staff):
        try:
            complaint = Complaint.objects.get(id=pk)
            form  = ComplaintRegisterForm(instance=complaint)
            context = {
                    
                    'complaint_register_form':form,
                    'complaint':complaint
                }
            if request.method == "GET":
                return render(request, 'complaint/update_complaint.html',context) 
            if request.method == "POST":
                form = ComplaintRegisterForm(request.POST, instance=complaint)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Complaint has been successfully updated.')
                    if request.user.is_superuser:
                        return redirect('view_complaint', complaint.id)
                    else:
                        return redirect('view_complaint_engg', complaint.id)
                
                messages.error(request, 'Complaint not Updated! Please provide valid input.')
                return render(request, 'complaint/update_complaint.html',context)
        except Complaint.DoesNotExist:
            return redirect('all_complaints')


    else:
        return HttpResponse("You dont't have permission to access this page")


@login_required
def list_complaints(request):
    if request.user.is_staff:
        all_complaints = Complaint.objects.all()
        paginator = Paginator(all_complaints, 3)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        return render(request, 'complaint/list_complaints.html', {'all_complaints':all_complaints, 'page_obj':page_obj})
    else:
        all_complaints = Complaint.objects.filter(assigned_to = request.user).order_by('-registred_date')
        paginator = Paginator(all_complaints, 3)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        return render(request, 'complaint/list_complaints.html', {'all_complaints':all_complaints, 'page_obj':page_obj})

@login_required
def view_complaint(request,pk):
    if(request.user.is_staff):
        try:
            complaint = Complaint.objects.get(id = pk)
            component_list = Item.objects.filter(complaint = complaint)
            # print(complaint.complaint_status)
            # print(component_list)
            complaint_status_form = ChangeComplaintStatusForm()
            engineers = Engineer.objects.all()
            # print(engineers)
            context = {
                'components':component_list,
                'complaint':complaint,
                'complaint_status_form':complaint_status_form,
                'engineers' : engineers,
            }
            return render(request, 'complaint/view_complaint.html', context)
        except Complaint.DoesNotExist:
            return redirect('all_complaints')
    else:
        return HttpResponse("You dont't have permission to access this page")

@login_required        
def view_complaint_engg(request,pk):
    try:
        complaint = Complaint.objects.get(id = pk)
        component_list = Item.objects.filter(complaint = complaint)

        # print(engineers)
        context = {
            'components':component_list,
            'complaint':complaint,
        }
        if request.method == 'GET':
            return render(request, 'complaint/view_complaint_e.html', context)

        if request.method == 'POST':
            stat = request.POST['cmpStatus']        
            complaint.complaint_status = stat
            complaint.resolved_date = datetime.datetime.now()
            complaint.save()
            messages.success(request, 'Status updated successfully.')
            return redirect('view_complaint_engg', pk)
    except Complaint.DoesNotExist:
        return redirect('all_complaints')

@login_required
def set_complaint_status(request,pk):
    complaint = Complaint.objects.get(id = pk)
    user = request.user
    if request.method == "POST":
        complaint_status_form = ChangeComplaintStatusForm(request.POST)
        if complaint_status_form.is_valid():
            status = complaint_status_form.cleaned_data.get('complaint_status')
            complaint.complaint_status = status
            
            # complaint.resolved_date = None
            complaint.save()
            messages.success(request, 'Status updated successfully.')
            return redirect('view_complaint', pk)
        messages.error(request, 'Something went wrong!')
        return redirect('view_complaint', pk)
    return redirect('view_complaint', pk)

@login_required
def assign_enineer(request,pk):
    complaint = Complaint.objects.get(id = pk)
    if request.method == "POST":
        engg_id = request.POST['assign_engineer']
        if engg_id == "-1":
            complaint.complaint_status = 2
            complaint.save()
            
            return redirect('view_complaint', pk)
        else:
            selected_engg = User.objects.get(id = engg_id)
            complaint.assigned_to = selected_engg
            complaint.assigned_date = datetime.datetime.now()
            complaint.complaint_status = 2
            messages.success(request, 'Engineer assigned successfully')
            complaint.save()
            return redirect('view_complaint', pk)

            
@login_required
def search_complaints_global(request):
    if(request.method == 'GET'):
        return HttpResponse("hello there")

    if(request.method == 'POST'):
        user = request.user
        search_str = json.loads(request.body).get('searchText')

        if user.is_staff:
            
            with_id = Complaint.objects.filter(id__istartswith = search_str) 
            with_c_name = Complaint.objects.filter(customer_name__istartswith = search_str) 
            with_c_mob = Complaint.objects.filter(customer_mob__istartswith = search_str) 
            with_c_email = Complaint.objects.filter(customer_email__istartswith = search_str) 
            with_c_add = Complaint.objects.filter(customer_address__istartswith = search_str) 
            with_p_name = Complaint.objects.filter(product_name__istartswith = search_str) 
            with_p_model = Complaint.objects.filter(product_model__icontains = search_str) 
            with_p_desc = Complaint.objects.filter(product_description__icontains = search_str) 
            with_p_prob = Complaint.objects.filter(problem__istartswith = search_str)
            results = with_id | with_c_name | with_c_email | with_c_mob | with_c_add | with_p_name | with_p_model | with_p_desc |with_p_prob
            data = results.values()
            return JsonResponse(list(data),safe=False)
        else:
            with_id = Complaint.objects.filter(id__istartswith = search_str ,assigned_to = user) 
            with_c_name = Complaint.objects.filter(customer_name__istartswith = search_str,assigned_to = user) 
            with_c_mob = Complaint.objects.filter(customer_mob__istartswith = search_str ,assigned_to = user) 
            with_c_email = Complaint.objects.filter(customer_email__istartswith = search_str ,assigned_to = user) 
            with_c_add = Complaint.objects.filter(customer_address__istartswith = search_str ,assigned_to = user) 
            with_p_name = Complaint.objects.filter(product_name__istartswith = search_str ,assigned_to = user) 
            with_p_model = Complaint.objects.filter(product_model__icontains = search_str ,assigned_to = user) 
            with_p_desc = Complaint.objects.filter(product_description__icontains = search_str ,assigned_to = user) 
            with_p_prob = Complaint.objects.filter(problem__istartswith = search_str ,assigned_to = user)
            results = with_id | with_c_name | with_c_email | with_c_mob | with_c_add | with_p_name | with_p_model | with_p_desc |with_p_prob
            data = results.values()
            return JsonResponse(list(data),safe=False)


@login_required
def add_component(request,pk):
    form  = AddComponentForm()
    context = {
            'form':form,
        }
    if request.method == "GET":
        complaint_item =  Complaint.objects.get(id=pk)
        context = {
            'form':form,
            'complaint':complaint_item
        }
        return render(request, 'complaint/add_component.html',context)
    if request.method == "POST":
        complaint_item =  Complaint.objects.get(id=pk)
        form  = AddComponentForm(request.POST)
        context = {
            'form':form,
            'complaint':complaint_item
        }
        if form.is_valid():
            form_items = form.save(commit=False)
            form_items.complaint = complaint_item
            form_items.save()
            messages.success(request, 'Component added successfully.')
            if request.user.is_superuser:
                return redirect('view_complaint', pk)
            else:
                return redirect('view_complaint_engg', pk)
        messages.error(request, 'Could not add component! Plese provide valid input.')
        return render(request, 'complaint/add_component.html',context)

@login_required
def update_component(request,pk):
    item = Item.objects.get(id=pk)

    form  = AddComponentForm(instance=item)
    complaint = Complaint.objects.get(id = item.complaint.id)
    c_id = complaint.id
    context = {
            'form':form,
            'complaint':complaint
        }
    if request.method == "GET":
        return render(request, 'complaint/update_component.html',context)
    if request.method == "POST":

        form  = AddComponentForm(request.POST,instance=item)
        context = {
            'form':form,
            'complaint':complaint
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Component updated successfully.')
            if request.user.is_superuser:
                return redirect('view_complaint', c_id)
            else:
                return redirect('view_complaint_engg', c_id)
        messages.error(request, 'Could not update component! Plese provide valid input.')
        return render(request, 'complaint/update_component.html',context)






@login_required
def inProgress_complaints(request):
    complaints = Complaint.objects.filter(complaint_status = 2)
    return render(request, 'complaint/in_progress_complaints.html',{'in_progress_complains':complaints})

@login_required
def closing_complaints(request):
    if(request.user.is_staff):
        closing_complaints1 = Complaint.objects.filter(complaint_status=3)
        closing_complaints2 = Complaint.objects.filter(complaint_status = 4)
        closing_complaints = closing_complaints1 | closing_complaints2
        return render(request, 'complaint/closing_complaints.html', {'closing_complaints':closing_complaints})
    else:
        return HttpResponse("You dont't have permission to access this page")

@login_required
def closed_complaints(request):
    if(request.user.is_staff):
        closed_complaints1 = Complaint.objects.filter(complaint_status=5)
        closed_complaints2 = Complaint.objects.filter(complaint_status = 6)
        closed_complaints = closed_complaints1 | closed_complaints2
        paginator = Paginator(closed_complaints, 3)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        return render(request, 'complaint/closed_complaints.html', {'closed_complaints':closed_complaints,'page_obj':page_obj})
    else:
        return HttpResponse("You dont't have permission to access this page")

# Engineer ---------------------------------

@login_required
def unresolved_complaints(request):
    user = request.user
    unresolved_complaints1 = Complaint.objects.filter(complaint_status = 2, assigned_to = user)

    unresolved_complaints = unresolved_complaints1
    # print(unresolved_complaints)
    return render(request, 'complaint/unresolved_complaints_e.html', {'unresolved_complaints':unresolved_complaints})


def resolved_complaints(request):
    user = request.user
    resolved_complaints1 = Complaint.objects.filter(complaint_status = 3, assigned_to = user)
    resolved_complaints2 = Complaint.objects.filter(complaint_status = 4, assigned_to = user)
    resolved_complaints3 = Complaint.objects.filter(complaint_status = 5, assigned_to = user)
    resolved_complaints4 = Complaint.objects.filter(complaint_status = 6, assigned_to = user)
    resolved_complaints = resolved_complaints1 | resolved_complaints2 |resolved_complaints3 |resolved_complaints4
    paginator = Paginator(resolved_complaints, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'complaint/resolved_complaints_e.html', {'resolved_complaints':resolved_complaints, 'page_obj':page_obj})


@login_required
def close_complaint(request,pk):
    # print("Status updated")
    if(request.user.is_staff):
        if request.method == "POST":
            complaint = Complaint.objects.get(id=pk)
            
            if complaint.complaint_status == 3:
                complaint.resolved_date = datetime.datetime.now()
                complaint.complaint_status = 5;
                # print(complaint.complaint_status)
                complaint.save()
                # return HttpResponse("Status changed")
                return redirect('print_record', pk)
            
            elif complaint.complaint_status == 4:
                complaint.resolved_date = datetime.datetime.now()
                complaint.complaint_status = 6;
                complaint.save()
                # print(complaint.complaint_status)
                # return HttpResponse("Status changed")
                return redirect('print_record', pk)
            return redirect('print_record', pk)
        return redirect('print_record', pk)
    else:
        return HttpResponse("You dont't have permission to access this page")

        

@login_required
def print_record(request,pk):
    if(request.user.is_staff):
        complaint = Complaint.objects.get(id=pk)
        complaint.resolved_date = datetime.datetime.today

        components = Item.objects.filter(complaint = complaint)
        subTotal = 0
        for item in components:
            item.total = item.unit_price * item.quantity
            subTotal = subTotal + item.total
        # print(components)

        tax_percent = 18
        tax_amount = (subTotal/100)*tax_percent
        total_amount = subTotal+tax_amount

        context = {
            'complaint':complaint,
            'components':components,
            # 'sub_total':subTotal,
            # 'tax_percent':tax_percent,
            # 'tax_amount':round(tax_amount,2),
            'total_amount':round(subTotal,2),
        }

        return render(request, 'home/print_record.html',context)
    else:
        return HttpResponse("You dont't have permission to access this page")



def check_complaint_status(request):
    if request.method == 'GET':
        return render(request,'home/check_status.html')
    if request.method == "POST":
        context = {

        }
        try:
            complaint_id = request.POST['complaint_id']
            complaint =  Complaint.objects.get(id = complaint_id) 
            stat = complaint.complaint_status
            stat_msg = ""
            stat_type = ""
            if(stat == 1):
                stat_msg = "Your camplaint have been successfully registred."
                stat_type = "warning"
                context = {
                    'complaint':complaint,
                    'status_msg':stat_msg,
                    'type':stat_type
                }
            elif(stat==2):
                stat_msg = "Hurrey! Service Initiated."
                stat_type = "info"
                context = {
                    'complaint':complaint,
                    'status_msg':stat_msg,
                    'type':stat_type
                }

            elif(stat>2 and stat<4):
                stat_msg = "W'll inform you when your device is ready!"
                stat_type = "success"
                context = {
                    'complaint':complaint,
                    'status_msg':stat_msg,
                    'type':stat_type
                }
            
            else:
                stat_msg = f"Sorry! No information available with this id."
                stat_type = "info"
                context = {
                    # 'complaint':complaint,
                    'status_msg':stat_msg,
                    'type':stat_type
                }
            # print(complaint)
            return render(request,'home/check_status.html',context)
        except Complaint.DoesNotExist:
            stat_msg = "Sorry! We couldn't find any querry. Please try again"
            stat_type = "danger"
            context = {
                # 'complaint':complaint,
                'status_msg':stat_msg,
                'type':stat_type
            }
            return render(request,'home/check_status.html',context)



def deleteComplaint(request,pk):
    if(request.user.is_staff):
        if request.method == 'POST':
            complaint = Complaint.objects.get(id=pk)
            c_id = complaint.id
            complaint.delete()
            print("deleting complaint...")
            messages.success(request, f'Complaint with #id {c_id} deleted successfully')
            return redirect('all_complaints')
    else:
        return HttpResponse("You dont't have permission to access this page")

def deleteComponent(request,pk):
    if request.method == 'POST':
        item = Item.objects.get(id = pk)
        complaint = item.complaint
        print("deleting component...")
        item.delete()
        messages.success(request, 'Item removed successfully ')
        if request.user.is_superuser:
            return redirect('view_complaint', complaint.id)
        else:
            return redirect('view_complaint_engg', complaint.id)




from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
# from django.contrib.auth.models import 
# For Graph
class Complaints_log_api(APIView):
    def get(self,request,format=None):
        complaints_reg = Complaint.objects.values('registred_date').annotate(count=Count('id'))[:30]
        complaints_rep = Complaint.objects.values('resolved_date').annotate(count=Count('id'))[0:30]
        # print(complaints_rep)
        data = {
            'registred':complaints_reg,
            'resolved':complaints_rep
        }
        return Response(data)
