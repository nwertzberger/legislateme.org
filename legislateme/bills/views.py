"""
Bills is responsible for showing all the active bills in the Senate at any
given time as well as the history of bills.  It is the entire site.
"""
from django.http import HttpResponse
from django.template import Context, loader
from bills.models import *

def index(r):
    """
    Shows the main page of the site.
    """
    try:
        bills = Bill.objects.get(active = True)
    except Bill.DoesNotExist: 
        bills = None

    t = loader.get_template('bills/index.html')
    c = Context({ 'bills':bills, })
    return HttpResponse(t.render(c))

