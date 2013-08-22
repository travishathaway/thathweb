from django.contrib import admin
from models import *

#class PictureAdmin(admin.ModelAdmin):
#    pass
admin.site.register(Picture)
admin.site.register(PictureTag)
