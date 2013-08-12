from thathweb.views import ThathwebBaseViewNoAuth
import models

class Pictures(ThathwebBaseViewNoAuth):
    template_name = "pictures/index.html"

    def get(self, request, *args, **kwargs):
        pictures = models.Pictures.objects.all()
        return self.render_to_response({ 'pictures' : pictures, 'pk' : kwargs.get('pk') })
