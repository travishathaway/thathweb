from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from thathweb.accounts.views import UserProfile

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name':'accounts/logout.html'} ),
    url(r'^profile/$', UserProfile.as_view(), name='thathweb.accounts.profile'),
)
