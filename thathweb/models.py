from django.db import models
from thathweb.utils import unique_slugify


class IncidentReport(models.Model):
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    caller_id = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = 'portland_incident_feed'


class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = self.title
            unique_slugify(self, slug_str)

        super(Tag, self).save(*args, **kwargs)
