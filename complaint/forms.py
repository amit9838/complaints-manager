from django import forms
from django.contrib.auth.models import User

import complaint
from .models import *
from django.forms import CharField, ChoiceField, ModelForm, PasswordInput, TextInput, EmailInput, NumberInput

class ComplaintRegisterForm(ModelForm):

    customer_name = forms.CharField(
        label="Customer Name",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    customer_mob = forms.CharField(
        label="Mobile Number",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm','type':'Number','placeholder':''})
    )
    customer_email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm','type':'email','placeholder':''})
    )

    customer_address = forms.CharField(
        label="Address",
        widget=forms.Textarea(attrs = {'class':'form-control form-control-sm','type':'text','placeholder':'' ,'rows':'3'})
    )

    class Meta:
        model = Complaint
        fields = ['customer_name','customer_mob','customer_email', 'customer_address']



class ComplaintProductForm(ModelForm):
    brand = forms.CharField(
        label="Brand",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm','type':'text','placeholder':''})
    )

    model_no = forms.CharField(
        label="Model",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm','type':'text','placeholder':''})
    )

    serial_no = forms.CharField(
        label="Serial No.",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    
    physical_condition = forms.CharField(
        label="Physical Conadition",
        widget=forms.TextInput(attrs = {'class':'form-control form-control-sm','type':'text','placeholder':''})
    )

    problem = forms.CharField(
        label="Problem",
        widget=forms.Textarea(attrs = {'class':'form-control form-control-sm','type':'text','placeholder':' ','rows':'5'})
    )

    class Meta:
        model = Complaint
        fields = ['brand','model_no','serial_no', 'physical_condition', 'problem']


class AddComponentForm(ModelForm):
    item_name = forms.CharField(
        label="Item Name",
        widget=forms.TextInput(attrs={'class':'form-control', 'type':'text','placeholder':'Item Name'})
        , max_length=120, required=True
        )
    item_description = forms.CharField(
        label="Item Description",
        widget=forms.Textarea(attrs={'class':'form-control', 'type':'text','placeholder':'Item Description'})
        , max_length=120, required=False
        )
    unit_price = forms.CharField(
        label="Unit Price",
        widget=forms.NumberInput(attrs={'class':'form-control', 'type':'number','placeholder':'Unit Price'})
        , max_length=120, required=True
        )

    quantity = forms.CharField(
        label="Qunatity",
        widget=forms.NumberInput(attrs={'class':'form-control', 'type':'number','placeholder':'Qunatity'})
        , max_length=120, required=True
        )

    class Meta:
        model = Item
        fields = ['item_name','item_description','unit_price', 'quantity']



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

