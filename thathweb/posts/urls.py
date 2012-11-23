from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^page/(?P<pk>\d+)/$', PostsDetail.as_view(), name="thathweb.posts.page"),
    url(r'^$', Posts.as_view(), name="thathweb.posts"),
)

