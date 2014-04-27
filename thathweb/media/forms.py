from django.forms import ModelForm
from models import MediaFile


class MediaFileForm(ModelForm):
    class Meta:
        model = MediaFile
        fields = ['title', 'caption', 'media_file']


