from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^page/(?P<pk>\d+)/$', PostsDetail.as_view(), name="nacha.posts.page"),
    url(r'^$', Posts.as_view(), name="nacha.posts"),
)

