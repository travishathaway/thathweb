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

class PictureTagAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'name' : ('title',)}

class PictureAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_admin_view', 'title', 'picture_tag_admin_view', 'published')
    list_filter = ('picture_tag','date_time',)
    exclude = ('path', 'thumbnail_path')
    actions = [publish, unpublish]

admin.site.register(Picture, PictureAdmin)
admin.site.register(PictureTag, PictureTagAdmin)
