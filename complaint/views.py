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
        if complaint.assigned_to == request.user:
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
        else:
            return HttpResponse("You dont't have permission to access this page")
            
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
        status = request.POST['cmpStatus']
        complaint.complaint_status = status
        complaint.resolved_by = user
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
        complaint.assigned_to = None
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
def add_component_manual(request,pk_cmp):
    complaint_item =  Complaint.objects.get(id=pk_cmp)
    cat = Category.objects.all()
    categories = []
    for item in cat:
        categories.append(item.name)
    cats = json.dumps(categories)

    if request.method == "GET":
        form_component = AddComponentForm_manual()
        context = {
            'form':form_component,
            'categories':cats,
            "complaint":complaint_item
        }
        return render(request, 'complaint/add_component.html',context) 
    
    if request.method == "POST":
        form_component = AddComponentForm_manual(request.POST)
        context = {
            'form':form_component,
            'categories':cats,
            "complaint":complaint_item
        }
        if form_component.is_valid():
            formdata = form_component.save(commit=False)
            formdata.complaint = complaint_item
            formdata.save();
            messages.success(request, 'Component has been successfully added.')
            return redirect('list_components',pk_cmp)
        else:
            messages.error(request, 'Please provide valid input.')
            return render(request, 'complaint/list_components.html',context)     
        


@login_required
def update_component(request,pk):
    item = Item.objects.get(id=pk)

    form_component  = AddComponentForm_manual(instance=item)
    cat = Category.objects.all()
    complaint = item.complaint
    print(complaint.id)
    print(item.id)
    categories = []
    for i in cat:
        categories.append(i.name)
    cats = json.dumps(categories)

    if request.method == "GET":
        context = {
            'form':form_component,
            'categories':cats,
            "complaint":complaint,
            "item":item
        }
        return render(request, 'complaint/update_component.html',context) 
    
    if request.method == "POST":
        form_component = AddComponentForm_manual(request.POST,instance=item)
        context = {
            'form':form_component,
            'categories':cats,
            "complaint":complaint,
            "item":item

        }
        if form_component.is_valid():
            formdata = form_component.save(commit=False)
            formdata.complaint = complaint
            form_component.save();
            messages.success(request, 'Component has been successfully updated.')
            return redirect('list_components', complaint.id)
        else:
            messages.error(request, 'Please provide valid input.')
            return render(request, 'complaint/list_components.html',context)


def deleteComponent(request,pk):
    if request.method == 'POST':
        item = Item.objects.get(id = pk)
        cmp_id = item.complaint.id 
        if(item.product):
            product = Product.objects.get(id = item.product.id)
            product.quantity += item.quantity;
            complaint = item.complaint
            # print("deleting component...")
            product.save()
            item.delete()
        else:
            item.delete()

        
        messages.success(request, 'Item removed successfully.')
        if request.user.is_superuser:
            return redirect('list_components', cmp_id)
        else:
            return redirect('list_components', cmp_id)


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


# Export/Import Data ***********************************************

from tablib import Dataset
from .resources import ComplaintResource

def export_data(request):
    if request.method == 'POST':
        # Get selected option from the form
        file_foramt = request.POST['file-format']
        complaint_resource = ComplaintResource()
        dataset = complaint_resource.export()
        file_name = "complaint_"+str(datetime.datetime.now())

        if(file_foramt=='CSV'):
            response = HttpResponse(dataset.csv, content_type = 'text/csv')
            response['Content-Disposition'] = f'attachement; filename = "{file_name}.csv"'
            return response
        
        elif(file_foramt=='JSON'):
            response = HttpResponse(dataset.json, content_type = 'application/json')
            response['Content-Disposition'] = f'attachement; filename = "{file_name}.json"'
            return response
        
        elif(file_foramt=='XLS (Excel)'):
            response = HttpResponse(dataset.xls, content_type = 'application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachement; filename = "{file_name}.xls"'
            return response
    return render(request, 'complaint/export_import.html')


def import_data(request):
    if request.method == "POST":
        file_format = request.POST['file-format']
        complaint_resource = ComplaintResource()
        dataset = Dataset()
        new_compalaints = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_compalaints.read().decode('utf-8'),format='csv')
            result = complaint_resource.import_data(dataset, dry_run=True)  

            if not result.has_errors():
                # Import now
                complaint_resource.import_data(dataset, dry_run=False)
                messages.success(request, 'Imported Successfully!.')
            else:
                messages.error(request, 'Failed to Import!.')


        elif file_format == 'JSON':
            imported_data = dataset.load(new_compalaints.read().decode('utf-8'),format='json')
            # Testing data import
            result = complaint_resource.import_data(dataset, dry_run=True) 

            if not result.has_errors():
                # Import now
                complaint_resource.import_data(dataset, dry_run=False)
                messages.success(request, 'Imported Successfully!.')
            else:
                messages.error(request, 'Failed to Import!.')



    return render(request, 'complaint/export_import.html') 


# Generate Invoice ************************************************************************************



from reportlab.pdfgen import canvas
from django.http import FileResponse
import io


def generate_invoice(request,pk):
    
    complaint = Complaint.objects.get(id=pk)
    components = Item.objects.filter(complaint = pk)

    current_day = datetime.datetime.now().date()
    formatted_date_str = datetime.date.strftime(current_day,"%d/%m/%Y")


    # Sample Data 
    item = []
    warrenty=[]  # in months
    unit_price = []
    qty = []
    tax = []

    for i in components:
        item.append(i.brand+" - "+i.name)
        warrenty.append(i.warrenty)
        unit_price.append(i.unit_price)
        qty.append(i.quantity)
        tax.append(0)

    discount = 100  # If no disount is applicabe,  put 'discount = 0'
    service_charge = 500   # If no service charge is applicabe,  put 'discount = 0'

    # Store data in object for simplicity
    objects = []
    class Product:
        def __init__(self,item,warrenty,unit_price,tax,quantity):
            if len(item) > 28 :
                self.item = item[0:28]+"..."
            else:
                self.item = item
            self.unit_price = unit_price
            self.warrenty = warrenty
            self.tax = tax
            self.quantity = quantity
            self.t_price = unit_price*quantity
            
    # Append object containing data into objects array
    for x in range(len(item)):
        obj = Product(item[x],warrenty[x],unit_price[x],tax[x],qty[x])
        objects.append(obj);


    # Y offsets
    y_offset = 0   # Header section y-offset (above Invoice,company) 
    cust_offset = 50 #Customersection y-offset
    table_offset = 0   #Table section y-offset
    sub_total_y_offset = -5  # Subtotal/total section offset


    # initializing variables with values
    formatted_date_str_for_title = datetime.date.strftime(current_day,"%d-%m-%Y")
    fileName = f'Invoice-{str(pk)}__{formatted_date_str_for_title}.pdf'
    print(fileName)
    title = "Invoice-"+str(pk) + "-" +formatted_date_str

    # Create pdf canvas 
    buffer = io.BytesIO()  # buffer
    pdf = canvas.Canvas(buffer)
    pdf.setTitle(title)

    # Start font-formating  
    pdf.setFont("Helvetica-Bold", 36)
    pdf.setFillColorRGB(.3,.3,.3)  # Start Font Color 
    pdf.drawString(40,(735-y_offset), "INVOICE")
    pdf.setFont("Helvetica", 13)   # Now Resume Default Font-Formatting
    pdf.setFillColorRGB(0,0,0)  # Resume font color (black, zero-illumination) 

    pdf.drawRightString(550,(750-y_offset), "The New Square")
    pdf.drawRightString(550,(730-y_offset), "Delhi,India")
    pdf.drawRightString(550,(710-y_offset), "support@square.in")
    pdf.drawRightString(550,(690-y_offset), "+9180xxxxxxxx")

    # Offset between complany and customer section
    y_offset = y_offset + cust_offset

    # Customer Section - left
    left_offset_y = 0  # adds y offset to "Billed To" setion
    y_offset = y_offset + left_offset_y
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40,(680-y_offset), "Billed To:")
    pdf.setFont("Helvetica", 13)
    pdf.drawString(40,(660-y_offset), complaint.customer_name)
    # pdf.drawString(40,(640-y_offset), "amitchaudhary0539@gmail.com")
    pdf.drawString(40,(640-y_offset), "+91"+complaint.customer_mob)
    pdf.drawString(40,(620-y_offset), complaint.customer_address)
    y_offset = y_offset - left_offset_y

    # Customer Section - right
    right_offset_y = 0   # adds y offset to "Status/invoice" setion
    y_offset = y_offset + right_offset_y 
    pdf.drawRightString(550,(660-y_offset), "Invoice : #"+ str(pk))
    pdf.drawRightString(550,(640-y_offset), "Issued on : "+ formatted_date_str)
    pdf.drawRightString(550,(620-y_offset), "Payment Status : Paid")
    y_offset = y_offset - right_offset_y


    y_offset = y_offset + table_offset
    # Items list header

    unit_price_x_pos = 370  #Default 370
    warrenty_x_pos = 280  #Default 280
    qty_x_pos = 470  #Default 470
    price_x_pos = 550  #Default 550

    pdf.setFont("Helvetica-Bold", 12)
    pdf.setLineWidth(.2)
    pdf.line(40,(600-y_offset),550,(600-y_offset))
    pdf.drawString(40,585-y_offset, "Item")
    pdf.drawString(warrenty_x_pos,585-y_offset, "Warrenty")
    pdf.line(40,(580-y_offset),550,(580-y_offset))
    # pdf.drawString(100,585, "Description")
    pdf.drawString(unit_price_x_pos,(585-y_offset), "Unit Price")
    pdf.drawCentredString(qty_x_pos,(585-y_offset), "Qty")
    pdf.drawRightString(price_x_pos,(585-y_offset), "Price")
    pdf.setFont("Helvetica", 13)

    # Calculate total cost of a product -> Unit_price * quantity * tax_amt  
    i=0;
    for i in range(len(objects)):
        pdf.drawString(40,(565-y_offset-20*i), objects[i].item)
        if objects[i].warrenty: # If there is any warrenty of the product
            pdf.drawString(warrenty_x_pos,(565-y_offset-20*i), str(objects[i].warrenty))
            pdf.setFont("Helvetica", 10)
            pdf.drawString(warrenty_x_pos+18,(565-y_offset-20*i), "Months")
            pdf.setFont("Helvetica", 13)
    
        pdf.drawRightString(unit_price_x_pos+40,(565-y_offset-20*i), str(objects[i].unit_price)+".0")
        if(objects[i].tax):
            pdf.setFont("Helvetica", 10)
            pdf.drawString(unit_price_x_pos+45,(565-y_offset-20*i), "+Tax")
            pdf.setFont("Helvetica", 13)
        pdf.drawString(qty_x_pos,(565-y_offset-20*i), str(objects[i].quantity))
        pdf.drawRightString(price_x_pos,(565-y_offset-20*i), str(objects[i].t_price)+".0")

    pdf.line(40,(565-y_offset-20*i-5),556,(565-y_offset-20*i-5))

    # Calculate total tax
    total_tax=0;
    for i in range(len(objects)):
        try:
            if(objects[i].tax):
                total_tax += objects[i].t_price*objects[i].tax
        except IndexError:
            pass

    # Calculate Sub total
    sub_total = 0
    for i in range(len(objects)):
        sub_total += objects[i].t_price
        

    # Calculate Gross Total
    y_offset = y_offset+sub_total_y_offset #  Gross total offset

    labels_x_pos = 480  #default 480
    pdf.drawRightString(labels_x_pos,(565-y_offset-20*i-25),  "Sub Total : ")
    pdf.drawRightString(550,(565-y_offset-20*i-25),str(sub_total)+".0")

    pdf.drawRightString(labels_x_pos,(565-y_offset-20*i-40), "Tax : ")
    pdf.drawRightString(550,(565-y_offset-20*i-40),"+ "+str(total_tax))


    if(service_charge):  # If service charge is applicable
        y_offset = y_offset+10 # Service Charge offset
        pdf.drawRightString(labels_x_pos,(565-y_offset-20*i-45), "Service Charge : ")
        pdf.drawRightString(550,(565-y_offset-20*i-45), "+ "+str(service_charge)+".0")
        y_offset = y_offset+5 # Service Charge offset


    if(discount):  # I any discount is applicable 
        y_offset = y_offset+10 # discount Charge offset
        pdf.drawRightString(labels_x_pos,(565-y_offset-20*i-45), "Discount : ")
        pdf.drawRightString(550,(565-y_offset-20*i-45), "- "+str(discount)+".0")
        y_offset = y_offset+5 # Service Charge offset


    pdf.line(380,(565-y_offset-20*i-45),556,(565-y_offset-20*i-45))
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawRightString(labels_x_pos,(565-y_offset-20*i-63), "Total : ")
    pdf.drawRightString(550,(565-y_offset-20*i-63), str(sub_total+total_tax+service_charge-discount)+".0")
    pdf.line(380,(565-y_offset-20*i-70),556,(565-y_offset-20*i-70))
    pdf.setFont("Helvetica", 13)

    pdf.drawString(40,(505-y_offset-20*i), "Thanks for visiting")
    pdf.save()
    buffer.seek(0) # end buffer

    return FileResponse(buffer, as_attachment=True,filename=fileName)