from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=64 ,blank=True)
    desc = models.CharField(max_length=3000,blank=True)
    category = models.CharField(max_length=32)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    registred_on = models.DateField(null=True, blank=True)
    registred_by = models.ForeignKey(User,db_column="p_registred_by", blank=True,null=True,on_delete=models.SET_NULL,related_name = "p_registred_by" ,verbose_name = "Registred By")

    def __str__(self):
        return self.name