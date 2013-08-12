from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    #url(r'^pictures/(?P<pk>\d+)/$', PostsDetail.as_view(), name="thathweb.pictures.page"),
    url(r'^$', Pictures.as_view(), name="thathweb.pictures"),
)

