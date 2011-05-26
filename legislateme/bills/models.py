from django.db import models
from django.contrib import admin

# Create your models here.

class Bill(models.Model):
    session = models.IntegerField()
    name = models.CharField(max_length=128)
    active = models.BooleanField()

    def __unicode__(self):
        return self.name

class SenateRes(models.Model):
    bill = models.ForeignKey(Bill)
    title = models.CharField(max_length=128)
    passed = models.BooleanField(help_text="Has this been passed?")

    def __unicode__(self):
        return self.title

class HouseRes(models.Model):
    bill = models.ForeignKey(Bill)
    title = models.CharField(max_length=128)
    advanced = models.BooleanField(help_text="Has this passed the house?")

    def __unicode__(self):
        return self.title

admin.site.register(Bill)
admin.site.register(HouseRes)
admin.site.register(SenateRes)
