from django.http import Http404

from thathweb.views import ThathwebBaseViewNoAuth
import models

class Posts(ThathwebBaseViewNoAuth):
    template_name = "posts/index.html"

    def get(self,request,*args,**kwargs):
        posts = models.Post.objects.all().order_by('-date')
        return self.render_to_response({'posts' : posts, 'pk' : kwargs.get('pk') })


class PostsDetail(ThathwebBaseViewNoAuth):

    template_name = "posts/detail.html"

    def get(self,request,*args, **kwargs):
        try:
            post = models.Post.objects.get(id=kwargs.get('pk'))
        except models.Post.DoesNotExist:
            raise Http404
        return self.render_to_response({'post' : post})
