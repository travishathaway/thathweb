from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from django.contrib.auth.models import User

from models import NachaSettings

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get',]
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'username' : ALL,
        }

class NachaSettingsResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = NachaSettings.objects.all()
        resource_name = 'nacha-settings'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'user' : ALL_WITH_RELATIONS,
        }
