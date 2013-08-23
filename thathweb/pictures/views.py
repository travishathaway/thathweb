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
        pictures  = models.Picture.objects.all()
        paginator = Paginator(pictures, 5)
        page = kwargs.get('page')

        try:
            pictures = paginator.page(page)
        except PageNotAnInteger:
            pictures = paginator.page(1)
        except EmptyPage:
            pictures = paginator.page(paginator.num_pages)

        if request.is_ajax():
            html = render_to_string(
                'pictures/list_partial.html', 
                {'pictures' : pictures, 'STATIC_URL' : settings.STATIC_URL}
            )
            #ret_json = json.dumps({'html' : html, 'page': page, 'pictures': pictures})
            ret_json = serializers.serialize('json', pictures)
            ret_json += json.dumps({'html' : html, 'page': page})
            response = HttpResponse(ret_json, mimetype="application/json" )
        else:
            response = self.render_to_response( { 
                'pictures' : pictures,
            } )

        return response
