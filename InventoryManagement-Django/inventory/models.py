from django.db import models
import datetime

    
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30, unique=True)
    code = models.CharField(max_length=50,default="")
    units = models.CharField(max_length=30,default="")
    quantity = models.FloatField(default=1)
    value = models.DecimalField(decimal_places=2, max_digits=8, default=1)
    receive = models.CharField(max_length=50,default="")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name
    

class Accessories(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30, unique=True)
    size = models.CharField(max_length=30, default="")
    quantity = models.IntegerField(default=1)
    value = models.CharField(max_length=50, default="")
    receive = models.CharField(max_length=50, default="")


    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name