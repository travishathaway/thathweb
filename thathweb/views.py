from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from posts.models import Post, SoundCloudSongs

def get_menu():

    return {
        'home' : {
            'url' : '/',
            'title' : 'Home',
            'active': False,
            'display' : True,
        },
        'lab' : {
            'url' : '/lab/',
            'title' : 'Lab',
            'active': False,
            'display' : True,
        },
       'nacha'  : {
            'url' : '/nacha/',
            'active' : False,
            'title' : 'Nacha',
            'display' : False,
            'submenu' : {
                'settings' : {
                    'url' : reverse('thathweb.nacha_creator.settings'),
                    'active' : False,
                    'title'  : 'Settings',
                },
                'generate' : {
                    'url' : reverse('thathweb.nacha_creator.gen'),
                    'active' : False,
                    'title' : 'Generate',
                },
                'batches' : {
                    'url' : reverse('thathweb.nacha_creator.batches'),
                    'active' : False,
                    'title' : 'Batches',
                },
            },
        },
    }




class ThathwebBaseView(TemplateView):
    '''
    Base view for the site. Everything on the site
    requires you to be logged in to do anything 
    '''

    template_name = "base.html"

    @method_decorator(login_required)
    def dispatch(self,*args,**kwargs):
        return super(ThathwebBaseView, self).dispatch(*args,**kwargs)

class ThathwebBaseViewNoAuth(TemplateView):
    '''
    Base view for the site. Everything on the site
    requires you to be logged in to do anything 
    '''

    template_name = "base.html"

    def dispatch(self,*args,**kwargs):
        return super(ThathwebBaseViewNoAuth, self).dispatch(*args,**kwargs)


class HomePage(ThathwebBaseViewNoAuth):
    """
    Home page view.  Recent posts and songs are shown here
    """

    template_name = "index.html"

    def get(self,request,*args,**kwargs):
        posts = Post.objects.all().order_by('-date')[:5]
        songs = SoundCloudSongs.objects.all()[:3]
        return self.render_to_response({'posts' : posts, 'songs' : songs })

class LabPage(ThathwebBaseViewNoAuth):
    """
    Page to show all the various "Lab" items.  Like my nacha generator
    """

    template_name = "lab.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({});
