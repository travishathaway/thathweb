from django.contrib import admin
from models import *

def publish(modeladmin, request, queryset):
    for obj in queryset:
        obj.published = True
        obj.save()

def unpublish(modeladmin, request, queryset):
    for obj in queryset:
        obj.published = False 
        obj.save()

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','date','published')
    list_filter = ('date','published')
    actions = [publish, unpublish]

admin.site.register(Post, PostAdmin)

class SoundCloudSongsAdmin(admin.ModelAdmin):
    pass
admin.site.register(SoundCloudSongs, SoundCloudSongsAdmin)
