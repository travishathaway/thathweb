from django.forms import ModelForm
import models

class Post(ModelForm):

    class Meta:
        model = models.Post
        exclude = ('user',)
