from django.contrib import admin
from models import MediaFile


class MediaFileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', ), }


admin.site.register(MediaFile, MediaFileAdmin)
