"""
This is the script used to populate and update the database with all bills
and whatnot currently going through congress.
"""

from django.core.management import setup_environ
from xml.dom.minidom import parse, parseString
import urllib2
response = urllib2.urlopen(
    'http://www.senate.gov/reference/active_bill_type/112.xml')
dom1 = parseString(response.read())
print dir(dom1)



