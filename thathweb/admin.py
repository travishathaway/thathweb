from django.contrib import admin
from .models import Tag, IncidentReport


class TagAdmin(admin.ModelAdmin):
    pass


class IncidentReportAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
admin.site.register(IncidentReport, IncidentReportAdmin)
