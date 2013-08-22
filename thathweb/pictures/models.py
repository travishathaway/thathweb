from django.db import models

class PictureTag(models.Model):
    title   = models.CharField(max_length=255)
    name    = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class Picture(models.Model):
    title       = models.CharField(max_length=255)
    path        = models.FilePathField(max_length=255)
    thumbnail_path = models.FilePathField(max_length=255)
    date_time   = models.DateTimeField(auto_now=True)
    picture_tag = models.ForeignKey(PictureTag, null=True, blank=True)

    def __unicode__(self):
        return self.title
