from django.db import models

# Create your models here.

class Bill(models.Model):
    session = models.IntegerField()
    name = models.CharField(max_length=128)
    active = models.BooleanField()

class SenateRes(models.Model):
    bill = models.ForeignKey(Bill)
    title = models.CharField(max_length=128)
    passed = models.BooleanField(help_text="Has this been passed?")

class HouseRes(models.Model):
    bill = models.ForeignKey(Bill)
    title = models.CharField(max_length=128)
    advanced = models.BooleanField(help_text="Has this passed the house?")
    
