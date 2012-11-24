from django.contrib.auth.models import User
from thathweb.views import ThathwebBaseView

class UserProfile(ThathwebBaseView):

    template_name = "accounts/profile.html"

    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        return self.render_to_response({'user' : user })

class UserDashboard(ThathwebBaseView):

    template_name = "accounts/dashboard.html"

    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        return self.render_to_response({'user' : user })
