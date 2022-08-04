from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from complaint.models import *

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,auto_created=True, related_name='employee')
    joinDate = models.DateField(auto_now=True)
    mob = models.CharField(max_length=15, blank=True,null=True);
    address = models.CharField(max_length=512,blank=True,null=True)

    def add_complaint_to_emp(self,complaint):
        self.registred_complaints.add(complaint.id)


    def __str__(self):
        return self.user.first_name +" " + self.user.last_name

class Engineer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,auto_created=True, related_name='engineer')
    joinDate = models.DateField(auto_now=True)
    expertise = models.CharField(max_length=32)
    mob = models.CharField(max_length=15, blank=True,null=True);
    address = models.CharField(max_length=512,blank=True,null=True)


    def add_complaint_to_engg(self,complaint):
        self.assigined_complaints.add(complaint.id)

    def add_resolved_complaint_to_engg(self,complaint):
        self.complaints_resolved.add(complaint.id)

    def __str__(self):
        return self.user.first_name