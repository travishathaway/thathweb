from django.db import models

class Pictures(models.Model):
    title = models.CharField(max_length=255)
    path  = models.FilePathField(max_length=255)


