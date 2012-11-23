from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from views import HomePage, LabPage

def bad_request(request):
    return HttpResponseBadRequest("poopy butt")

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view()),
    url(r'^lab/$', LabPage.as_view(), name='nacha.lab'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('nacha.accounts.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^posts/', include('nacha.posts.urls')),
    url(r'^nacha/',include('nacha.nacha_creator.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

