from django.conf.urls import patterns, include, url
from tastypie.api import Api

from views import *
from api import NachaSettingsResource, UserResource

api_v1 = Api(api_name='v1')
api_v1.register(NachaSettingsResource())
api_v1.register(UserResource())

urlpatterns = patterns('',
    url(r'^$', ThathwebBase.as_view()),
    url(r'^settings/$', NachaSettings.as_view(), name='thathweb.nacha_creator.settings'),

    url(r'^generate/$', NachaCreate.as_view(), name='thathweb.nacha_creator.gen'),
    url(r'^generate/batch/$', NachaCreateBatch.as_view(), name='thathweb.nacha_creator.gen.batch'),
    url(r'^generate/entry/$', NachaCreateRecordEntry.as_view(), name='thathweb.nacha_creator.gen.entry'),

    url(r'^batches/$', NachaBatches.as_view(), name='thathweb.nacha_creator.batches'),
    url(r'^api/', include(api_v1.urls)),
)
