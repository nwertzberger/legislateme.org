from django.db import models

# Create your models here.

class Bill(models.Model):
    passed = models.BooleanField(help_text="Has the bill been passed?")
    session = models.IntegerField()
    name = models.CharField(max_length=128)

class SenateRes(models.Model):
    bill = models.ForeignKey(Bill)
    title = models.CharField(max_length=128)

class HouseRes(models.Model):
    bill = models.ForeignKey(Bill)
    title = models.CharField(max_length=128)
    
