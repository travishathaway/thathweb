from django.views.generic import TemplateView
from django.contrib.auth.models import User
from nacha.views import NachaBaseView

from pprint import pprint

class UserProfile(NachaBaseView):

    template_name = "accounts/profile.html"

    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        return self.render_to_response({'user' : user,'menu' : self.menu })

class UserDashboard(NachaBaseView):

    template_name = "accounts/dashboard.html"

    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        self.menu['dashboard']['active'] = True
        return self.render_to_response({'user' : user, 'menu' : self.menu })
