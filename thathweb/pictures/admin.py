from django.contrib import admin
from models import *

class PictureTagAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'name' : ('title',)}

class PictureAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_admin_view', 'title', 'picture_tag_admin_view')
    exclude = ('path', 'thumbnail_path')

admin.site.register(Picture, PictureAdmin)
admin.site.register(PictureTag, PictureTagAdmin)
