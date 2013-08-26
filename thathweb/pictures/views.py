import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.core import serializers
from django.template.loader import render_to_string
from thathweb import settings 
from thathweb.views import ThathwebBaseViewNoAuth
import models

class Pictures(ThathwebBaseViewNoAuth):
    template_name = "pictures/index2.html"

    def get(self, request, *args, **kwargs):
        self.pictures  = models.Picture.objects.all()
        paginator = Paginator(self.pictures, 20)
        page = kwargs.get('page')

        #set the tags
        self.get_tags()

        try:
            pictures = paginator.page(page)
        except PageNotAnInteger:
            pictures = paginator.page(1)
        except EmptyPage:
            pictures = paginator.page(paginator.num_pages)

        if request.is_ajax():
            pictures_html = render_to_string(
                'pictures/list_partial.html', 
                {'pictures' : pictures, 'STATIC_URL' : settings.STATIC_URL}
            )

            paginator_html = render_to_string(
                'pictures/pagination.html',
                { 'pictures' : pictures }
            )

            tags_html = render_to_string(
                'pictures/tags.html',
                {'tags' : self.tags }
            )

            ret_json = json.dumps({
                'pictures_html' : pictures_html,
                'paginator_html' : paginator_html,
                'page': page
            })

            response = HttpResponse(ret_json, mimetype="application/json" )
        else:
            response = self.render_to_response( { 
                'pictures' : pictures,
                'tags'     : self.tags
            } )

        return response

    def get_tags(self):
        pt = models.PictureTag.objects.all()
        tags = []

        for tag in pt:
            tags.append({
                'title' : tag.title,
                'name'  : tag.name,
                'count' : self.pictures.filter(picture_tag__name=tag.name).count()
            })

        self.tags = tags
