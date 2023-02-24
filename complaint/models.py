from django.db import models
from django.contrib.auth.models import User
from user.models import *
from store.models import *
import datetime


# Includes list of items and service charge

class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank =True)
    complaint = models.ForeignKey("complaint.Complaint", on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=64 ,blank=True)
    category = models.CharField(max_length=32,blank=True)
    warrenty = models.PositiveIntegerField(blank=True)  # In months
    desc = models.CharField(max_length=3000,blank=True)
    unit_price = models.PositiveIntegerField(blank=True)
    tax = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(blank=True)

    def link_complaint(self,new_complaint):
        return self.complaint.cr(new_complaint)


STATUS_CHOICES = (
    (1,"Registred"), # Pending
    (2,"In Progress"), # In Progress
    (3,"Repaired"), # Success
    (4,"Failed"), # Fail
    (5,"Repaired and Closed"), # Success and Closed
    (6,"Failed and Closed"), # Fail and Closed
)


# Create your models here.
class Complaint(models.Model):
    # Customer Info
    customer_name = models.CharField(max_length=255)
    customer_mob = models.CharField(null=False, blank = False, max_length=15)
    customer_email = models.EmailField(null = True, blank =True)
    customer_address = models.CharField(max_length=255)
    complaint_status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    
    # Relationship 
    registred_by = models.ForeignKey(User,db_column="registred_by", blank=True,null=True,on_delete=models.SET_NULL,related_name = "registred_by" ,verbose_name = "Registred By")
    registred_date = models.DateField(default = datetime.datetime.now)

    assigned_to = models.ForeignKey(User, db_column="assigned_to",blank=True,null=True,on_delete=models.SET_NULL,related_name = "assigned_to" ,verbose_name = "Assigned To")
    assigned_by = models.ForeignKey(User, db_column="assigned_by",blank=True,null=True,on_delete=models.SET_NULL,related_name = "assigned_by" ,verbose_name = "Assigned By")
    assigned_date = models.DateField(null=True, blank=True)
    
    updated_by = models.ForeignKey(User, db_column="updated_by",blank=True,null=True,on_delete=models.SET_NULL,related_name = "updated_by" ,verbose_name = "Updated By")
    updated_date = models.DateField(null=True, blank=True)
    
    resolved_by = models.ForeignKey(User, db_column="resolved_by",blank=True,null=True,on_delete=models.SET_NULL,related_name = "resolved_by" ,verbose_name = "Resolved_By")
    resolved_date = models.DateField(null=True, blank=True)

    is_verified = models.BooleanField(default=False, db_column="is_verified_on_close")
    closed_by = models.ForeignKey(User, db_column="closed_by",blank=True,null=True,on_delete=models.SET_NULL,related_name = "closed_by" ,verbose_name = "Closed_By")
    closed_date = models.DateField(null=True, blank=True)


    # Product Info
    category = models.CharField(max_length=256,null=True, blank=True) # Select category   
    brand = models.CharField(max_length=256,null=True, blank=True)
    model_no = models.CharField(max_length=256,null=True, blank=True)
    serial_no = models.CharField(max_length=128, null=True,  blank=True)
    physical_condition = models.CharField(max_length=2048 ,null=True, blank=True)
    problem = models.CharField(max_length=5000,blank=True)
    details = models.CharField(max_length=5000,blank=True)



    def __str__(self):
        return   str(self.id)+"-"+ self.brand.upper() +"-" + self.model_no + "  ("+ self.customer_name + ")" + "  [" + self.category + "] " 
        

class ComplaintOTP(models.Model):
    complaint = models.ForeignKey(Complaint,null=True,blank=True,on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    expires_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return "OTP for "+ str(self.complaint) + "is: " + str(self.otp)


class CheckList(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    c_list_key = models.CharField(max_length=255)
    c_list_val = models.CharField(max_length=255)

    def __str__(self):
        return self.complaint.customer_name +"-"+ self.c_list_key