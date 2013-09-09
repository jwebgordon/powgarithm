from django.conf.urls import patterns, include, url
from powgarithm.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^powgarithm/$', page_one),
    url(r'^powgarithm/input_people_things/$', input_people_things),
    url(r'^powgarithm/rank_things/$', rank_things),
    url(r'^powgarithm/output_results/$', output_results),
    # Examples:
    # url(r'^$', 'powgarithm.views.home', name='home'),
    # url(r'^powgarithm/', include('powgarithm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
