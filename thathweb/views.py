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
                    'url' : reverse('nacha.nacha_creator.settings'),
                    'active' : False,
                    'title'  : 'Settings',
                },
                'gen' : {
                    'url' : reverse('nacha.nacha_creator.gen'),
                    'active' : False,
                    'title' : 'Generator',
                },
                'batches' : {
                    'url' : reverse('nacha.nacha_creator.batches'),
                    'active' : False,
                    'title' : 'Batches',
                },
            },
        },
    }




class NachaBaseView(TemplateView):
    '''
    Base view for the site. Everything on the site
    requires you to be logged in to do anything 
    '''

    template_name = "base.html"

    def __init__(self,**kwargs):
        super(NachaBaseView,self).__init__(**kwargs)
        self.menu = get_menu()

    @method_decorator(login_required)
    def dispatch(self,*args,**kwargs):
        return super(NachaBaseView, self).dispatch(*args,**kwargs)

class NachaBaseViewNoAuth(TemplateView):
    '''
    Base view for the site. Everything on the site
    requires you to be logged in to do anything 
    '''

    template_name = "base.html"

    def __init__(self,**kwargs):
        super(NachaBaseViewNoAuth,self).__init__(**kwargs)
        self.menu = get_menu()

    def dispatch(self,*args,**kwargs):
        return super(NachaBaseViewNoAuth, self).dispatch(*args,**kwargs)


class HomePage(NachaBaseViewNoAuth):
    """
    Home page view.  Recent posts and songs are shown here
    """

    template_name = "index.html"

    def get(self,request,*args,**kwargs):
        posts = Post.objects.all()[:5]
        songs = SoundCloudSongs.objects.all()[:3]
        self.menu['home']['active'] = True
        return self.render_to_response({'menu' : self.menu, 'posts' : posts, 'songs' : songs })

class LabPage(NachaBaseViewNoAuth):
    """
    Page to show all the various "Lab" items.  Like my nacha generator
    """

    template_name = "lab.html"

    def get(self, request, *args, **kwargs):
        self.menu['lab']['active'] = True
        return self.render_to_response({'menu' : self.menu});
