import json
from thathweb import settings 
from django.db import models
from django.utils.html import format_html

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
    published   = models.BooleanField(default=True)
    annotation  = models.TextField(null=True)

    #Relationships
    picture_tag = models.ManyToManyField(PictureTag, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def thumbnail_admin_view(self):
        return format_html('<img src="{0}{1}" title="{2}" height="40">',
                           settings.STATIC_URL,
                           self.thumbnail_path,
                           self.title)

    def picture_tag_admin_view(self):
        tag_string = ''
        for tag in self.picture_tag.all():
            tag_string += '<span style="background-color: #ccc">' +\
                    tag.title + '</span>&nbsp;'

        return format_html(tag_string)

    def json_safe(self):
        return {
            'title' : self.title,
            'path'  : self.path,
            'thumbnail_path' : self.thumbnail_path,
            'date_time' : self.date_time,
            'picture_tag' : [ {'name' : tag.name, 'title' : tag.title} for tag in self.picture_tag.all() ]
        }
