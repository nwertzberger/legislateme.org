"""
Bills is responsible for showing all the active bills in the Senate at any
given time as well as the history of bills.  It is the entire site.
"""
from django.http import HttpResponse
from django.template import Context, loader
from legislateme.bills.models import *
import updates
import logging

logger = logging.getLogger(__name__)

def index(r):
    """
    The main page shows all bills active in congress for the given day.
    """
    try:
        bills = Bill.objects.filter(active = True)
    except Bill.DoesNotExist: 
        bills = None

    t = loader.get_template('bills/index.html')
    c = Context({ 'bills': bill, })
    return HttpResponse(t.render(c))

