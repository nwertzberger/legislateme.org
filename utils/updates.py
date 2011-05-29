'''
This is the script used to populate and update the database with all bills
and whatnot currently going through congress.
'''
import sys, os
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ
from legislateme import settings

setup_environ(settings)

from xml.dom.minidom import parseString
import urllib2
from BeautifulSoup import BeautifulSoup
from legislateme.bills.models import *
import re
import datetime


SESSION = 112

def get_xml(url):
    response = urllib2.urlopen(url)
    return parseString(response.read())

def get_html(url):
    response = urllib2.urlopen(url)
    return BeautifulSoup(response.read())

def get_tag_text(dom, tag):
    '''
    It's common to just need the text in a tag.  This takes care of that.
    '''
    tag = dom.getElementsByTagName(tag)[0]
    lines = []
    for x in tag.childNodes:
        if x.nodeType == x.TEXT_NODE:
            lines.append(x.data)
    return ''.join(lines)

def get_rss_items(url):
    '''
    Gets items from the respective RSS feeds.  It also goes through and 
    gets supplimentary info from the URL provided.
    '''
    dom = get_xml(url)
    items = dom.getElementsByTagName("item")
    bills = []

    for i in items:
        b = Bill()
        b.title = get_tag_text(i, "title")
        b.description = get_tag_text(i, "description")
        b.link = get_tag_text(i, "link")
        b.last_floored = date.today()

        # There is so much crap that happens on a single day... We only want to
        # get worked up about the bills.
        if title.startswith('S.') or title.startswith('H.R.'):
            dom = get_html('http://thomas.loc.gov/cgi-bin/bdquery/z?d'
                    + session + ':' + title + ':@@@L&summ2=m&')
            # Now we need the summary, sponsor, and cosponsors
            # We know the titles are put in a <b>
            sections = dom.findAll('b')
            for s in sections:
                if s.string == 'Sponsor':
                    sponsor = s.nextSibling.string

            # Save it all
            bills.append(b)

def get_bills():
    '''
    Get all the bills shown off today.
    '''
    new_bills = []
    # Get the active congress as XML
    dom = get_xml('http://thomas.loc.gov/home/rss/housefloortoday.xml')

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

def get_representatives():
    '''
    Retrieves all Representatives.
    '''
    dom = get_html('http://www.house.gov/representatives/')

    states = dom.findAll('h2', attrs={'id' : re.compile('state_')})
    for s in states: 
        state = s.string.strip()
        s = s.findNext('tbody')
        for tr in [s.tr] + s.tr.findNextSiblings('tr'):
            col = 0
            for td in [tr.td] + tr.td.findNextSiblings('td'):
                if col == 1:
                    name = td.contents[0].string.strip()
                    site = td.contents[0]['href']
                if col == 2:
                    party = td.string.strip()
                if col == 4:
                    phone = td.string.strip()
                col += 1
            (ln, fn) = map(lambda s: s.strip(),
                    name.encode('utf-8').split(','))[:2]
            try:
                rep = Representative.objects.get(
                        last_name = ln,
                        first_name = fn
                )
            except Representative.DoesNotExist:
                rep = Representative( last_name = ln,
                        first_name = fn)
            rep.site = site.encode('utf-8')
            rep.state = state
            rep.party = party
            rep.phone = phone
            rep.title = 1
            print "Saving Rep " + ln
            rep.save()

def get_senators():
    '''
    Retrieve all the current senators.
    '''
    dom = get_xml(
        'http://www.senate.gov/general/contact_information/senators_cfm.xml',
    )
    members = dom.getElementsByTagName('member')

    for m in members:
        ln = get_tag_text(m, 'last_name')
        fn = get_tag_text(m, 'first_name')

        try:
            rep = Representative.objects.get(
                    last_name = ln,
                    first_name = fn
            )
        except Representative.DoesNotExist:
            rep = Representative( last_name = ln,
                    first_name = fn)

        rep.party   = get_tag_text(m, 'party')
        rep.state   = get_tag_text(m, 'state')
        rep.address = get_tag_text(m, 'address')
        rep.phone   = get_tag_text(m, 'phone')
        rep.email   = get_tag_text(m, 'email')
        rep.site    = get_tag_text(m, 'website')
        rep.title   = 0
        print "Saving Senator " + ln
        rep.save()
    
get_senators()
get_representatives()
