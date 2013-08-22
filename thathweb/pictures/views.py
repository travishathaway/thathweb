import json
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.conf import settings 
from thathweb.views import ThathwebBaseViewNoAuth
import models

class Pictures(ThathwebBaseViewNoAuth):
    template_name = "pictures/index2.html"

    def get(self, request, *args, **kwargs):
        if not kwargs.get('page'):
            page = 1
        else:
            page = kwargs.get('page')

        pictures  = models.Picture.objects.all()
        paginator = Paginator(pictures, 25)
        results   = paginator.page(page)

        if request.is_ajax():
            html = render_to_string('pictures/list_partial.html', {'pictures' : results})
            print settings.STATIC_URL
            ret_json = json.dumps({'html' : html, 'STATIC_URL' : settings.STATIC_URL})
            #ret_json = serializers.serialize('json', {'pictures' : results, 'html' : html})
            response = HttpResponse(ret_json, mimetype="application/json" )
        else:
            response = self.render_to_response( { 
                'pictures' : results,
                'pk' : kwargs.get('pk'),
                'paginator' : paginator 
            } )

        return response
