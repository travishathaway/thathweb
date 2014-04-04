from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^page/(?P<pk>\d+)/$', PostsDetail.as_view(), name="thathweb.posts.page"),
    url(r'^$', Posts.as_view(), name="thathweb.posts.posts"),
)

