from django.conf.urls import patterns, url
from views import AddUser, AddToGroup, ManagementBase

urlpatterns = patterns('',
    url(r'^$',ManagementBase.as_view(),name="thathweb.management"),
    url(r'^user/add/$', AddUser.as_view(),name="thathweb.user.add"),
    url(r'^group/add/$', AddToGroup.as_view(),name="thathweb.usertogroup.add"),
)
