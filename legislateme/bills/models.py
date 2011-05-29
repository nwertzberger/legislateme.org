from django.db import models
from django.contrib import admin

class Representative(models.Model):
    TITLE_CHOICES = {
        (0, 'Senator'),
        (1, 'Representative'),
    }
    # Unique info
    first_name = models.CharField(max_length = 64)
    last_name = models.CharField(max_length = 64)
    title = models.IntegerField(choices = TITLE_CHOICES)
    party = models.CharField(max_length = 64,
                help_text="Democrat, Republican, etc.")
    state = models.CharField(max_length = 2)
    # Contact info
    address = models.CharField(max_length = 256)
    phone   = models.CharField(max_length = 32)
    site    = models.URLField()
    email   = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.last_name + u', ' + self.first_name


class Bill(models.Model):
    title           = models.CharField(max_length=128)
    description     = models.TextField(help_text="One-line description of bill")
    last_floored    = models.DateField(help_text="Last time on the floor")
    summary         = models.TextField(help_text="Summary of bill")
    link            = models.URLField()
    passed_house    = models.BooleanField()
    passed_senate   = models.BooleanField()
    passed_president = models.BooleanField()
    # Who started the bill
    sponsor = models.ForeignKey(Representative,
            related_name = 'sponsored_bill_set')
    # Who thought this bill was a good idea.
    cosponsors = models.ManyToManyField(Representative,
            related_name = 'cosponsored_bill_set')
    related = models.OneToOneField('Bill')

    def __unicode__(self):
        return self.title

admin.site.register(Representative)
admin.site.register(Bill)

