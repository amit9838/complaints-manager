from django.db import models
from django.contrib.auth.models import User
from user.models import *
import datetime


# Includes list of items and service charge

class Item(models.Model):
    complaint = models.ForeignKey("complaint.Complaint", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=125)
    item_description = models.CharField(max_length=255, blank=True)
    unit_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

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

    closed_by = models.ForeignKey(User, db_column="closed_by",blank=True,null=True,on_delete=models.SET_NULL,related_name = "closed_by" ,verbose_name = "Closed_By")
    closed_date = models.DateField(null=True, blank=True)


    # Product Info
    category = models.CharField(max_length=256,null=True, blank=True) # Select category   
    brand = models.CharField(max_length=256,null=True, blank=True)
    model_no = models.CharField(max_length=256,null=True, blank=True)
    serial_no = models.CharField(max_length=256, null=True,  blank=True)
    physical_condition = models.CharField(max_length=2048 ,null=True, blank=True)
    problem = models.CharField(max_length=5000)



    # def __str__(self):
    #     return self.category + "-" + self.brand + "("+ self.customer_name + ")"
        


class CheckList(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    c_list_key = models.CharField(max_length=255)
    c_list_val = models.CharField(max_length=255)

    def __str__(self):
        return self.complaint.customer_name +"-"+ self.c_list_key