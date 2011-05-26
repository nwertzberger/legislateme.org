"""
This is the script used to populate and update the database with all bills
and whatnot currently going through congress.
"""
from xml.dom.minidom import parseString
import urllib2

def get_xml(url):
    response = urllib2.urlopen(url)
    return parseString(response.read())

def get_bills():
    new_bills = []
    # Get the active congress as XML
    dom = get_xml('http://www.senate.gov/reference/active_bill_type/112.xml')

    # figure out the last time this information was updated.
    date = dom.getElementsByTagName("date")[0].childNodes[0].data

    # figure out which congress this is.
    congress = int(dom.getElementsByTagName("congress")[0].childNodes[0].data)

    # Show active legislation
    active = dom.getElementsByTagName("active_legislation")[0]
    for item in active.getElementsByTagName("item"):
        # Ok i thought i'd try my hand at a terse line.  This one returns the
        # names of the senate bills.
        articles = lambda branch: map(lambda x: x.childNodes[0].data, item
                    .getElementsByTagName(branch)[0]
                    .getElementsByTagName("article"))

        new_bills.append({ 
            'name'  : item.getElementsByTagName("name")[0].childNodes[0].data,
            'senate': articles("senate"),
            'house' : articles("house"),
        })
    return new_bills

def get_senators():
    dom = get_xml(
        'http://www.senate.gov/general/contact_information/senators_cfm.xml',
    )





