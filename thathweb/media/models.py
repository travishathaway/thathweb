import os

from django.db import models
from django.contrib.auth.models import User

from easy_thumbnails.fields import ThumbnailerImageField

from thathweb.models import Tag
from thathweb.utils import unique_slugify


class MediaFile(models.Model):
    '''
    The MediaFile object contains images as well other types of media fiels
    (pdf, mp3, mov, etc.). If the file is an image we also store two sizes
    of thumbnail, medium and small. Thumbnails are stored using an
    `easy_thumbnail.fields.ThumbnailerImageField`.
    '''
    title = models.CharField(max_length=255, unique=True)
    caption = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_by = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)
    media_file = models.FileField(upload_to="uploads/", max_length=255)
    thumbnail = ThumbnailerImageField(
        upload_to="uploads/thumbnails/", blank=True,
        resize_source=dict(size=(100, 100), sharpen=True), max_length=255)
    thumbnail_medium = ThumbnailerImageField(
        upload_to="uploads/thumbnails_medium/",
        blank=True, resize_source=dict(size=(400, 400), sharpen=True),
        max_length=255)

    # Timestamp stuff
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # This is used in templates
    image_types = ['jpg', 'jpeg', 'png', 'gif']
    doc_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt']
    audio_types = ['mp3', 'ogg', 'flac', 'm4a', 'wma']
    video_types = ['mp4', 'ogg', 'webm', 'mov']

    @property
    def file_type(self):
        '''
        Returns the file type of `self.media_file`
        '''
        file_name, file_ext = os.path.splitext(str(self.media_file))

        if file_ext:
            return file_ext.replace('.', '').lower()
        else:
            return ''

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = self.title
            unique_slugify(self, slug_str)

        super(MediaFile, self).save(*args, **kwargs)
