from django.http import Http404

from nacha.views import NachaBaseViewNoAuth
import models

class Posts(NachaBaseViewNoAuth):
    template_name = "posts/index.html"

    def __init__(self,**kwargs):
        super(Posts,self).__init__(**kwargs)
        self.menu['posts']['active'] = True;

    def get(self,request,*args,**kwargs):
        posts = models.Post.objects.all()
        return self.render_to_response({'menu' : self.menu, 'posts' : posts, 'pk' : kwargs.get('pk') })


class PostsDetail(NachaBaseViewNoAuth):

    template_name = "posts/detail.html"

    def get(self,request,*args, **kwargs):
        try:
            post = models.Post.objects.get(id=kwargs.get('pk'))
        except models.Post.DoesNotExist:
            raise Http404
        return self.render_to_response({'post' : post, 'menu' : self.menu})
