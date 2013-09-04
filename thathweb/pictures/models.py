import json
from django.db import models

class PictureTag(models.Model):
    title   = models.CharField(max_length=255)
    name    = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title

class Picture(models.Model):
    title       = models.CharField(max_length=255)
    path        = models.FilePathField(max_length=255)
    thumbnail_path = models.FilePathField(max_length=255)
    date_time   = models.DateTimeField(auto_now=True)
    annotation  = models.TextField(null=True)

    #Relationships
    picture_tag = models.ManyToManyField(PictureTag, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def json_safe(self):
        return {
            'title' : self.title,
            'path'  : self.path,
            'thumbnail_path' : self.thumbnail_path,
            'date_time' : self.date_time,
            'picture_tag' : [ {'name' : tag.name, 'title' : tag.title} for tag in self.picture_tag.all() ]
        }
