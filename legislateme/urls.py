from django.conf.urls.defaults import *
import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'legislateme.bills.views.index'),
    (r'^bills/', include('legislateme.bills.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if not settings.PROD:
    urlpatterns += patterns('django.views.static',
            (r'^media/(?P<path>.*)$',
                'serve', {
                    'document_root':settings.MEDIA_ROOT,
                    'show_indexes': True,
                }
            ),
        )
