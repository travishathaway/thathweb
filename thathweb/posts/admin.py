from django.contrib import admin
from models import *

class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)

class SoundCloudSongsAdmin(admin.ModelAdmin):
    pass
admin.site.register(SoundCloudSongs, SoundCloudSongsAdmin)
