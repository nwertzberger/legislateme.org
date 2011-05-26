"""
Bills is responsible for showing all the active bills in the Senate at any
given time as well as the history of bills.  It is the entire site.
"""
from django.http import HttpResponse
from django.template import Context, loader
from legislateme.bills.models import *
from legislateme.bills.updates import *
import logging

logger = logging.getLogger(__name__)

def index(r):
    """
    Shows the main page of the site.
    """
    try:
        bills = Bill.objects.filter(active = True)
    except Bill.DoesNotExist: 
        bills = None

    t = loader.get_template('bills/index.html')
    c = Context({ 'bills':bills, })
    return HttpResponse(t.render(c))

def update(r):
    """
    Updates the model with current legislature. This should be a script, but
    I suck, and can't figure out how to integrate that with django.
    """
    bills = get_bills()
    response = "<pre>\n"

    # Go through and populate the database
    for b in bills:
        try: 
            bill = Bill.objects.get(name=b['name'])
        except Bill.DoesNotExist:
            bill = Bill(name=b['name'], session=112)
            response += b['name'] + "\n"
            bill.save()

        bill.active = True
        # senate resolutions
        for r in b['senate']:
            try: 
                res = SenateRes.objects.get(title=r)
            except SenateRes.DoesNotExist:
                res = SenateRes(title=r, bill_id=bill.id)
                response += "    " + r + "\n"
            res.save()
        for r in b['house']:
            try: 
                res = HouseRes.objects.get(title=r)
            except HouseRes.DoesNotExist:
                res = HouseRes(title=r, bill_id=bill.id)
                response += "    " + r + "\n"
            res.save()
        bill.save()

    return HttpResponse(response + '</pre>')

