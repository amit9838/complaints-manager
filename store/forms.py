from dataclasses import field
from django import forms
from .models import *
from django.forms import ModelForm

class NewProductFrom(ModelForm):
    name = forms.CharField(
        label="Product Name",
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    brand = forms.CharField(
        label="Brand",
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    desc = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'class':'form-control form-control-sm','type':'text','placeholder':'','rows':5})
    )
    category = forms.CharField(
        label="Category",
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm','type':'text','placeholder':''})
    )
    warrenty = forms.CharField(
        label='Warrenty (in months)',
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )
    quantity = forms.CharField(
        label='Quantity',
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )
    unit_price = forms.CharField(
        label='Unit Price',
        widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'type':'number','placeholder':''})
    )

    class Meta:
        model = Product
        fields = ['name','brand','desc','category','warrenty','quantity','unit_price']