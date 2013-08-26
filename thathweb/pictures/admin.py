from django.contrib import admin
from models import *

class PictureTagAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'name' : ('title',)}

class PictureAdmin(admin.ModelAdmin):
    exclude = ('path', 'thumbnail_path')

admin.site.register(Picture, PictureAdmin)
admin.site.register(PictureTag, PictureTagAdmin)
