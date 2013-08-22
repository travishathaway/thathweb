from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^$', Pictures.as_view(), name="thathweb.pictures"),
    url(r'^page/(?P<page>\d+)/$', Pictures.as_view(), name="thathweb.pictures.page"),
)

