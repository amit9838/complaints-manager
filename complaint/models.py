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
    
    # Product Info
    product_name = models.CharField(max_length=255)
    product_model = models.CharField(max_length=30)
    product_description = models.CharField(max_length=30)
    problem = models.CharField(max_length=3000)
    registred_date = models.DateField(default = datetime.datetime.now)
    
    # Relationship 
    registred_by = models.ForeignKey(User,db_column="employee", blank=True,null=True,on_delete=models.SET_NULL,related_name = "registred_by" ,verbose_name = "Registred By")
    assigned_to = models.ForeignKey(User, db_column="engineer",blank=True,null=True,on_delete=models.SET_NULL,related_name = "assigned_to" ,verbose_name = "Assigned To")
    resolved_by = models.ForeignKey(User, db_column="engineer",blank=True,null=True,on_delete=models.SET_NULL,related_name = "resolved_by" ,verbose_name = "Resolved_By")
    assigned_date = models.DateField(null=True, blank=True)
    resolved_date = models.DateField(null=True, blank=True)

    

    def add_component(self,new_item):
        return self.components_used.add(new_item)

    def set_registred_by(self, user):
        self.registred_by = user
        return self.registred_by

    def resolved_by(self, user):
        return self.resolved_by.add(user)

    def set_resolved_date(self):
        self.set_resolved_date.datetime.datetime.now()

    def set_status(self, status):
        self.complaint_status = status
        return self.complaint_status

    def __str__(self):
        return self.product_name + "-" + self.product_model + "("+ self.customer_name + ")"
        