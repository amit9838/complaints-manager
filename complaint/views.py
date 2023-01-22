from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from user.models import *
from store.models import Category
import json


# Register new Complaint ------------------------------------------
@login_required
def register_complaint(request):
    if(request.user.is_staff):
        form_cmp  = ComplaintRegisterForm()
        context = {
                'complaint_register_form':form_cmp,
            }
        if request.method == "GET":
            cat = Category.objects.all()
            categories = []
            for item in cat:
                categories.append(item.name)
            cats = json.dumps(categories)
            context = {
                'complaint_register_form':form_cmp,
                'categories':cats
            }
            return render(request, 'complaint/new_complaint.html',context) 
        if request.method == "POST":
            form_cmp = ComplaintRegisterForm(request.POST)
            cat = request.POST['category']
            if form_cmp.is_valid():
                formdata = form_cmp.save(commit=False)
                formdata.registred_by = request.user
                formdata.complaint_status = 1
                formdata.category = cat
                formdata.save()
                obj = form_cmp.instance
                messages.success(request, 'Complaint has been successfully registred.')
                return redirect('add_checklist',obj.id)
            messages.error(request, 'Complaint not registred! Please provide valid input.')
            return render(request, 'complaint/new_complaint.html',context)
    else:
        return HttpResponse("You dont't have permission to access this page")


@login_required
def update_complaint(request,pk):
    if(request.user.is_staff):
        try:
            complaint = Complaint.objects.get(id=pk)
            form  = ComplaintRegisterForm(instance=complaint)
            if not request.user.is_superuser:
                form.fields['customer_mob'].disabled = True
            context = {
                    
                    'complaint_register_form':form,
                    'complaint':complaint
                }
            if request.method == "GET":
                cat = Category.objects.all()
                categories = []
                for item in cat:
                    categories.append(item.name)
                cats = json.dumps(categories)
                context = {
                    
                    'complaint_register_form':form,
                    'complaint':complaint,
                    'categories':cats
                }
                return render(request, 'complaint/update_complaint.html',context) 
            if request.method == "POST":
                form = ComplaintRegisterForm(request.POST, instance=complaint)
                form.fields['customer_mob'].disabled = True
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Complaint has been successfully updated.')
                    return redirect('view_complaint', complaint.id)
                
                messages.error(request, 'Complaint not Updated! Please provide valid input.')
                return render(request, 'complaint/update_complaint.html',context)
        except Complaint.DoesNotExist:
            return redirect('all_complaints')


    else:
        return HttpResponse("You dont't have permission to access this page")

# Using above complaint id to attach product checklist of  the the product.
# Add Check List --------------------------------------------------------
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


def deleteComplaint(request,pk):
    if request.method == 'POST' and request.user.is_staff:
        usr = request.user
        complaint = Complaint.objects.get(id=pk)
        sent_password = request.POST['password']
        if usr.check_password(sent_password):
            complaint.delete()
            print("deleting complaint...")
            messages.success(request, f'Complaint with #id {pk} deleted successfully')
            return redirect('all_complaints')
        
        elif sent_password == "":
            messages.error(request, "Please enter password to delete complaint!")
            return redirect('complaint_settings',pk)

        else:
            messages.error(request, "Incorrect Password !")
            return redirect('complaint_settings',pk)


    else:
        return HttpResponse("You dont't have permission to access this page")

# List Complaints-----------------------------------------------------------------
@login_required
def list_complaints(request):
    if request.user.is_staff:
        all_complaints = Complaint.objects.all().order_by('-registred_date')
        paginator = Paginator(all_complaints, 50)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        return render(request, 'complaint/list_complaints.html', {'all_complaints':all_complaints, 'page_obj':page_obj})
    else:
        all_complaints = Complaint.objects.filter(assigned_to = request.user).order_by('-registred_date')
        paginator = Paginator(all_complaints, 3)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        return render(request, 'complaint/list_complaints.html', {'all_complaints':all_complaints, 'page_obj':page_obj})


# Complaints Settings
def settings(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {
            'categories':categories,
        }
        return render(request, 'complaint/settings.html',context)


@login_required
def unassigned_complaints(request):
    complaints = Complaint.objects.filter(complaint_status = 1)
    return render(request, 'complaint/unassigned_complaints.html',{'unassigned_complaints':complaints})

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


@login_required
def close_complaint(request,pk):
    if(request.user.is_staff):
        if request.method == "POST":
            complaint = Complaint.objects.get(id=pk)
            complaint.closed_by = request.user
            complaint.closed_date = datetime.datetime.now()
            
            if complaint.complaint_status == 3:
                complaint.complaint_status = 5;
                complaint.save()
                return redirect('print_record', pk)
            
            elif complaint.complaint_status == 4:
                complaint.complaint_status = 6;
                complaint.save()
                return redirect('print_record', pk)
            return redirect('print_record', pk)
        return redirect('print_record', pk)
    else:
        return HttpResponse("You dont't have permission to access this page")

# View Complaint -----------------------------------------------------------------
@login_required
def view_complaint(request,pk):
    if(request.user.is_staff):
        try:
            complaint = Complaint.objects.get(id = pk)
            check_list = CheckList.objects.filter(complaint = complaint)

            component_list = Item.objects.filter(complaint = complaint)
            complaint_status_form = ChangeComplaintStatusForm()
            engineers = Engineer.objects.all()
            # print(engineers)
            context = {
                'components':component_list,
                'check_list':check_list,
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
        check_list = CheckList.objects.filter(complaint = complaint)
 
        print(complaint.complaint_status)
        context = {
            'components':component_list,
            'check_list':check_list,
            'complaint':complaint,
        }
        if request.method == 'GET':
            return render(request, 'complaint/view_complaint_e.html', context)

        if request.method == 'POST':
            stat = request.POST['cmpStatus']        
            complaint.complaint_status = stat
            complaint.resolved_date = datetime.datetime.now()
            if int(stat) >= 4 and int(stat) <= 5:
                complaint.resolved_by = request.user
            complaint.save()
            messages.success(request, 'Status updated successfully.')
            return redirect('view_complaint_engg', pk)
    except Complaint.DoesNotExist:
        return redirect('all_complaints')

@login_required
def complaint_settings(request,pk):
    complaint = Complaint.objects.get(id=pk)
    
    if request.method == 'GET':
        context = {
            "complaint":complaint
        }
        return render(request,'complaint/complaint_settings.html',context)



@login_required
def set_complaint_status(request,pk):
    complaint = Complaint.objects.get(id = pk)
    user = request.user
    if request.method == "POST":
        complaint_status_form = ChangeComplaintStatusForm(request.POST)
        if complaint_status_form.is_valid():
            status = complaint_status_form.cleaned_data.get('complaint_status')
            complaint.complaint_status = status

            if status >=4 and status <=5:
                complaint.resolved_by = request.user
            
            # complaint.resolved_date = None
            complaint.save()
            messages.success(request, 'Status updated successfully.')
            if request.user.is_staff:
                return redirect('view_complaint', pk)
            else:
                return redirect('view_complaint_engg', pk)


        messages.error(request, 'Something went wrong!')
        if request.user.is_staff:
            return redirect('view_complaint', pk)
        else:
            return redirect('view_complaint_engg', pk)

    if request.user.is_staff:
        return redirect('view_complaint', pk)
    else:
        return redirect('view_complaint_engg', pk)


@login_required
def assign_engineer(request,pk):
    complaint = Complaint.objects.get(id = pk)
    if request.method == "POST":
        engg_id = request.POST['assign_engineer']
        if engg_id == "-1":
            messages.error(request, 'Please select a valid input.')
            return redirect('view_complaint', pk)
        else:
            selected_engg = User.objects.get(id = engg_id)
            complaint.assigned_to = selected_engg
            complaint.assigned_by = request.user
            complaint.assigned_date = datetime.datetime.now()
            complaint.complaint_status = 2
            messages.success(request, 'Engineer assigned successfully')
            complaint.save()
            return redirect('view_complaint', pk)

@login_required
def reset_complaint_progress(request,pk):
    complaint = Complaint.objects.get(id = pk)
    if request.method == "POST" and request.user.is_staff:
        complaint.complaint_status = 1
        complaint.assigned_by = None
        complaint.assigned_date = None
        complaint.updated_by = None
        complaint.updated_date = None
        complaint.resolved_by = None
        complaint.resolved_date = None
        complaint.closed_by = None
        complaint.closed_date = None
        complaint.updated_by = request.user
        complaint.updated_date = datetime.datetime.now()
        complaint.save()
        messages.success(request, 'Complaint progress has been reset successfully.')
        return redirect('complaint_settings', pk)




def list_components(request,pk):
    complaint = Complaint.objects.get(id=pk)
    components = Item.objects.filter(complaint = complaint)
    context = {
        "components" : components,
        "complaint":complaint
    }
    return render(request, 'complaint/list_components.html',context)

@login_required
def add_component(request,pk_cmp):
    if request.method == "POST":
        complaint_item =  Complaint.objects.get(id=pk_cmp)
        # print(pk_cmp)
        # print(vars(complaint_item))
        pk_pro = request.POST['pk_pro']
        print(pk_pro)
        product = Product.objects.get(id = pk_pro)
        # print(product)
        is_listed_pro1 = ""
        try:
            is_listed_pro1 = Item.objects.filter(product = product,complaint = complaint_item)
        except Item.DoesNotExist:
            pass
        if(is_listed_pro1):
            is_listed_pro1[0].quantity +=1
            product.quantity -= 1
            is_listed_pro1[0].save()
            product.save()
        else:
            Item.objects.create(product = product, complaint = complaint_item, brand=product.brand, name =product.name, category = product.category, desc = product.desc, warrenty = product.warrenty, unit_price = product.unit_price, quantity = 1)
            product.quantity -= 1
            product.save()
        messages.success(request, 'Component added successfully.')
        return redirect('list_components', pk_cmp)
    messages.error(request, 'Could not add component! Plese provide valid input.')
    return redirect('list_components', pk_cmp)


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


def deleteComponent(request,pk):
    if request.method == 'POST':
        item = Item.objects.get(id = pk)
        product = Product.objects.get(id = item.product.id)
        product.quantity += item.quantity;
        complaint = item.complaint
        # print("deleting component...")
        product.save()
        item.delete()
        
        messages.success(request, 'Item removed successfully ')
        if request.user.is_superuser:
            return redirect('list_components', complaint.id)
        else:
            return redirect('list_components', complaint.id)


# Search Compalints Global ------------------------------------------------------------
@login_required
def search_complaints_global(request):
    if(request.method == 'GET'):
        return HttpResponse("hello there")

    if(request.method == 'POST'):
        user = request.user
        search_str = json.loads(request.body).get('searchText')

        # For Admin, Employee --------------
        if user.is_staff:
            with_id = Complaint.objects.filter(id__istartswith = search_str) 
            with_c_name = Complaint.objects.filter(customer_name__istartswith = search_str) 
            with_c_mob = Complaint.objects.filter(customer_mob__istartswith = search_str) 
            with_c_email = Complaint.objects.filter(customer_email__istartswith = search_str) 
            with_c_add = Complaint.objects.filter(customer_address__icontains = search_str) 
            with_p_brand = Complaint.objects.filter(brand__icontains = search_str) 
            with_p_model = Complaint.objects.filter(model_no__icontains = search_str) 
            with_p_cond = Complaint.objects.filter(physical_condition__icontains = search_str) 
            with_p_prob = Complaint.objects.filter(problem__icontains = search_str)
            results = with_id | with_c_name | with_c_email | with_c_mob | with_c_add | with_p_brand | with_p_model | with_p_cond |with_p_prob
            data = results.values()
            return JsonResponse(list(data),safe=False)
            
        # For Engineer -------------
        else:
            with_id = Complaint.objects.filter(id__istartswith = search_str ,assigned_to = user) 
            with_c_name = Complaint.objects.filter(customer_name__istartswith = search_str,assigned_to = user) 
            with_c_mob = Complaint.objects.filter(customer_mob__istartswith = search_str ,assigned_to = user) 
            with_c_email = Complaint.objects.filter(customer_email__istartswith = search_str ,assigned_to = user) 
            with_c_add = Complaint.objects.filter(customer_address__icontains = search_str ,assigned_to = user) 
            with_p_brand = Complaint.objects.filter(brand__icontains = search_str,assigned_to = user) 
            with_p_model = Complaint.objects.filter(model_no__icontains = search_str ,assigned_to = user) 
            with_p_cond = Complaint.objects.filter(physical_condition__icontains = search_str,assigned_to = user) 
            with_p_prob = Complaint.objects.filter(problem__icontains = search_str ,assigned_to = user)
            results = with_id | with_c_name | with_c_email | with_c_mob | with_c_add | with_p_brand | with_p_model | with_p_cond |with_p_prob
            data = results.values()
            return JsonResponse(list(data),safe=False)


# For Engineer --------------------------------------------------------------------------
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



# Close Complaint ------------------------------------------------------------------------
@login_required
def print_record(request,pk):
    if(request.user.is_staff):
        complaint = Complaint.objects.get(id=pk)
        # complaint.resolved_date = datetime.datetime.today

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
            # 'tax_percent':tax_percent,
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

            elif(stat>2 and stat<=4):
                stat_msg = "Service in progress, you will be informed very soon."
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
                    'status_msg':stat_msg,
                    'type':stat_type
                }
            # print(complaint)
            return render(request,'home/check_status.html',context)
        except Complaint.DoesNotExist:
            stat_msg = "Sorry! We couldn't find any querry. Please try again"
            stat_type = "danger"
            context = {
                'status_msg':stat_msg,
                'type':stat_type
            }
            return render(request,'home/check_status.html',context)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

# from django.contrib.auth.models import
# For Graph
class Complaints_log_api(APIView):
    def get(self,request,format=None):
        complaints_reg = Complaint.objects.values('registred_date').annotate(count=Count('id'))[:30]
        complaints_rep = Complaint.objects.values('resolved_date').annotate(count=Count('id'))[0:30]
        data = {
            'registred':complaints_reg,
            'resolved':complaints_rep
        }
        return Response(data)