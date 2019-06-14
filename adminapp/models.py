from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique = True)
    account_type = models.CharField(max_length=20)
    is_phone_verified = models.BooleanField(default = False)
    is_email_verifiel = models.BooleanField(default = False)

class Products(models.Model):
    pname = models.CharField(max_length=15)
    pdescription = models.TextField(max_length=50)
    pcategory = models.CharField(max_length=10)
    punits = models.IntegerField()
    qrcode = models.IntegerField(blank=True,null=True)

class Employees(models.Model):
    ename = models.CharField(max_length=15)
    eage = models.IntegerField()

class AssignProducts(models.Model):
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)

class Otp(models.Model):
    user=models.OneToOneField(CustUser,on_delete=models.CASCADE)
    token=models.IntegerField()

class Check(models.Model):
    check=models.BooleanField(default=False)