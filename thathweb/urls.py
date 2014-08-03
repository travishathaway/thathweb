from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from views import (
    HomePage, LabPage, DownloadsPage, IncidentReportPage,
    NoSmokingPage
)

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view()),
    url(r'^lab/$', LabPage.as_view(), name='thathweb.lab'),
    url(r'^pif/$', IncidentReportPage.as_view(), name='incident_report'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mediamanager/', include('thathweb.media.urls')),
    url(r'^accounts/', include('thathweb.accounts.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^posts/', include('thathweb.posts.urls')),
    url(r'^pictures/', include('thathweb.pictures.urls')),
    url(r'^nacha/',include('thathweb.nacha_creator.urls')),
    url(r'^downloads/', DownloadsPage.as_view() ),
    url(r'^days-since-last-cigarette/', NoSmokingPage.as_view() ),
    url(r'^admin_tools/', include('admin_tools.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
