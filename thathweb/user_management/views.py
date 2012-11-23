from thathweb.views import ThathwebBaseView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

class ManagementBase(ThathwebBaseView):

    template_name = "user_management/user_management_base.html"

    def get(self,request,*args,**kwargs):
        context = {}
        context['menu'] = self.menu
        context['menu']['manage']['active'] = True

        return self.render_to_response(context)

class AddUser(ThathwebBaseView):

    template_name = 'user_management/add.html'

    def get(self,request,*args,**kwargs):
        context = {}
        context['form'] = UserCreationForm()
        context['menu'] = self.menu
        context['menu']['manage']['active'] = True
        context['menu']['manage']['submenu']['user']['active'] = True

        return self.render_to_response(context)

    def post(self,request,*args,**kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            menu = self.menu
            menu['manage']['active'] = True
            menu['manage']['submenu']['user']['active'] = True
            return self.render_to_response({'form' : form, 'menu' : menu})

class ListUser(ThathwebBaseView):

    template_name = "user_management/list.html" 

class AddToGroup(ThathwebBaseView):

    template_name = "user_management/add_user_to_group.html"

    def get(self,request,*args,**kwargs):
        context = {}
        context['users'] = User.objects.all()
        context['groups'] = Group.objects.all()
        context['menu'] = self.menu
        context['menu']['manage']['active'] = True
        context['menu']['manage']['submenu']['group']['active'] = True

        return self.render_to_response(context)

    def post(self,request,*args,**kwargs):
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                continue
            else:
                new_user = request.POST[key].split(',')
                new_user.pop()

                new_user = [ User.objects.get(username=user).id for user in new_user ]

                g = Group.objects.get(id=key)
                g.user_set = new_user
                g.save()

        return HttpResponse(simplejson.dumps({'status' : 'hai'}),content_type='application/javascript')
