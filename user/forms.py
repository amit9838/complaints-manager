from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import CharField, PasswordInput, TextInput, EmailInput, NumberInput ,ModelForm

class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center', 'placeholder':'New Password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center', 'placeholder':'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']

        widgets = {
            'username':TextInput(attrs={
                'class': "form-control",
                'placeholder':"Username"
            }),

            'first_name':TextInput(attrs={
                'class': "form-control",
                'placeholder':"First Name"
            }),

            'last_name':TextInput(attrs={
                'class': "form-control",
                'placeholder':"Last Name"
            }),

            'email':EmailInput(attrs={
                'class': "form-control",
                'placeholder':"Email"
            }),
        }



class CompleteEmployeeProfile(ModelForm):

    mob = forms.CharField(
        label="Mobile Number",
        widget=forms.TextInput(attrs = {'class':'form-control','type':'text','placeholder':'Mobile Number'})
    )

    address = forms.CharField(
        label="Address",
        widget=forms.TextInput(attrs = {'class':'form-control','type':'text','placeholder':'Address'})
    )


    class Meta:
        model = Employee
        fields = ['mob','address']





class CompleteEngineerProfile(ModelForm):

    expertise = forms.CharField(
        label="Expertise",
        widget=forms.TextInput(attrs = {'class':'form-control','type':'text','placeholder':'Expertise'})
    )
    mob = forms.CharField(
        label="Mobile Number",
        widget=forms.TextInput(attrs = {'class':'form-control','type':'text','placeholder':'Mobile Number'})
    )

    address = forms.CharField(
        label="Address",
        widget=forms.TextInput(attrs = {'class':'form-control','type':'text','placeholder':'Address'})
    )


    class Meta:
        model = Engineer
        fields = ['expertise','mob','address']


