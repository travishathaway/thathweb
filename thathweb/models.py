from django.db import models


class IncidentReport(models.Model):
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    caller_id = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'portland_incident_feed'
