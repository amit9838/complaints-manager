from django import forms
from django.contrib.auth.models import User

import complaint
from .models import *
from django.forms import CharField, ChoiceField, ModelForm, PasswordInput, TextInput, EmailInput, NumberInput

class ComplaintRegisterForm(ModelForm):

    customer_name = forms.CharField(
        label="Customer Name",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm rounded-2 ','type':'text','placeholder':''})
    )
    customer_mob = forms.CharField(
        label="Mobile Number",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm rounded-2 ','type':'Number','placeholder':'', 'id':'mob_input' })
    )
    customer_email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm rounded-2','type':'email','placeholder':''})
    )

    customer_address = forms.CharField(
        label="Address",
        widget=forms.Textarea(attrs = {'class':'form-control form-control-sm rounded-2','type':'text','placeholder':'' ,'rows':'3'})
    )

    brand = forms.CharField(
        label="Brand",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm rounded-2','type':'text','placeholder':''})
    )

    model_no = forms.CharField(
        label="Model",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm rounded-2','type':'text','placeholder':''})
    )

    physical_condition = forms.CharField(
        label="Physical Conadition",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm rounded-2','type':'text','placeholder':''})
    )
    serial_no = forms.CharField(
        label="Serial No.",
        required=False,
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm rounded-2','type':'text','placeholder':''})
    )
    details = forms.CharField(
        required=False,
        label="Details",
        widget=forms.Textarea(attrs = {'class':'form-control form-control-sm rounded-2','type':'text','placeholder':'Other details...','rows':'3'})
    )
    problem = forms.CharField(
        label="Problem",
        widget=forms.Textarea(attrs = {'class':'form-control form-control-sm rounded-2','type':'text','placeholder':'Describe the problem...','rows':'5'})
    )
    class Meta:
        model = Complaint
        fields = ['customer_name','customer_mob','customer_email', 'customer_address','brand','model_no','serial_no', 'details', 'physical_condition', 'problem']



class AddComponentForm(ModelForm):
    name = forms.CharField(
        label="Product Name",
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    brand = forms.CharField(
        label="Brand",
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    desc = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class':'form-control form-control-sm','type':'text','placeholder':'','rows':5})
    )
    category = forms.CharField(
        label="Category",
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    warrenty = forms.CharField(
        label='Warrenty (in months)',
        required=False,
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )
    quantity = forms.CharField(
        label='Quantity',
        required=False,
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )
    unit_price = forms.CharField(
        label='Unit Price',
        required=False,
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )
    tax = forms.CharField(
        label='Tax',
        required=False,
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':'Skip this if not applicable'})
    )
    class Meta:
        model = Product
        fields = ['name','brand','desc','category','warrenty', 'quantity','unit_price','tax']




class AddComponentForm_manual(ModelForm):
    name = forms.CharField(
        label="Component Name",
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    brand = forms.CharField(
        label="Brand",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    desc = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(attrs={'class':'form-control form-control-sm','type':'text','placeholder':'','rows':5})
    )
    category = forms.CharField(
        label="Category",
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    warrenty = forms.CharField(
        label='Warrenty (in months)',
        required=True,
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )
    quantity = forms.CharField(
        label='Quantity',
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )
    unit_price = forms.CharField(
        label='Unit Price',
        required=True,
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )
    tax = forms.CharField(
        label='Tax',
        required=True,
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':'Skip if not applicable'})
    )

    class Meta:
        model = Item
        fields = ['name','brand','desc','category','warrenty', 'quantity','unit_price','tax']


class ChangeComplaintStatusForm(ModelForm):
    STATUS_CHOICES = (
    (1,"Registred"), # Pending
    (2,"In Progress"), # In Progress
    (3,"Repaired"), # Success
    (4,"Failed"), # Fail
    (5,"Repaired and Closed"), # Success and Closed
    (6,"Failed and Closed"), # Fail and Closed
)

    complaint_status = forms.ChoiceField(choices = STATUS_CHOICES, label="", initial='', widget=forms.Select(attrs={'class':'form-control form-control-sm rounded'}), required=True)

    class Meta:
        model = Complaint
        fields = ['complaint_status']

