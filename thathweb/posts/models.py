from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    text = HTMLField()
    date = models.DateField(auto_now=True)
    published = models.BooleanField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

class SoundCloudSongs(models.Model):
    title = models.CharField(max_length=255)
    body  = models.TextField()
    user  = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

