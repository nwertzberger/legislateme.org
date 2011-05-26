from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'legislateme.bills.views.index'),
    (r'^update$', 'legislateme.bills.views.update'),
)

