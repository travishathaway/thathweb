from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', Pictures.as_view(), name="thathweb.pictures"),
    url(r'^page/(?P<page>\d+)/$', Pictures.as_view(), name="thathweb.pictures.page"),
    url(r'^tag/(?P<tag>[\w,-]+)/$', Pictures.as_view(), name="thathweb.pictures.tag"),
)

