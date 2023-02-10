from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from .models import *

class Category(models.Model):
    name = models.CharField(max_length=256)
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=64 ,blank=True)
    category = models.CharField(max_length=32)
    desc = models.CharField(max_length=3000,blank=True)
    quantity = models.IntegerField()
    warrenty = models.PositiveIntegerField()  # In months
    unit_price = models.IntegerField()
    tax = models.FloatField(default=0)
    registred_on = models.DateField(null=True, blank=True)
    registred_by = models.ForeignKey(User,db_column="p_registred_by", blank=True,null=True,on_delete=models.SET_NULL,related_name = "p_registred_by" ,verbose_name = "Registred By")

    def __str__(self):
        return self.name