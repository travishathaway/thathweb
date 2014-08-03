from django.conf.urls import patterns, url

urlpatterns = patterns('thathweb.media.views',
    # Media CRUD endpoints
    url(r'^add/$', 'media_add'),
    url(r'^add/ajax/$', 'media_add_ajax'),
    url(r'^add/ajax/partial/$', 'media_add_ajax_partial'),
    url(r'^addexisting/ajax/partial/$', 'media_addexisting_ajax_partial'),
    url(r'^list/$', 'media_list'),
    url(r'^(?P<pk>\d{1,10})/edit/$', 'media_edit'),
    url(r'^(?P<pk>\d{1,10})/$', 'media_view'),
)
