from django.conf.urls.defaults import *

from views import AddUser, AddToGroup, ManagementBase

urlpatterns = patterns('',
    url(r'^$',ManagementBase.as_view(),name="nacha.management"),
    url(r'^user/add/$', AddUser.as_view(),name="nacha.user.add"),
    url(r'^group/add/$', AddToGroup.as_view(),name="nacha.usertogroup.add"),
)
