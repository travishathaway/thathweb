import json
from pprint import pprint

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
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
        self.page = kwargs.get('page')

        #set the tags
        self.get_tags()

        try:
            self.pictures = paginator.page(self.page)
        except PageNotAnInteger:
            self.pictures = paginator.page(1)
        except EmptyPage:
            self.pictures = paginator.page(paginator.num_pages)

        if request.is_ajax():
            response = self.get_ajax()
        else:
            response = self.render_to_response( { 
                'pictures' : self.pictures,
                'tags'     : self.tags
            } )

        return response

    def get_ajax(self):
        # Build all our templates
        pictures_html = render_to_string(
            'pictures/list_partial.html', 
            {'pictures' : self.pictures, 'STATIC_URL' : settings.STATIC_URL}
        )

        paginator_html = render_to_string(
            'pictures/pagination.html',
            { 'pictures' : self.pictures }
        )

        tags_html = render_to_string(
            'pictures/tags.html',
            {'tags' : self.tags }
        )

        ret_json = json.dumps({
            'pictures_html' : pictures_html,
            'paginator_html' : paginator_html,
            'page': self.page
        })

        response = HttpResponse(ret_json, mimetype="application/json" )

        return response

    def get_regular(self, request):
        return

    def post(self, request, *args, **kwargs):
        self.pictures  = models.Picture.objects.all()
        self.filter_pictures(request)
        paginator = Paginator(self.pictures, 20)
        self.page = kwargs.get('page')

        #set the tags
        self.get_tags()

        try:
            self.pictures = paginator.page(self.page)
        except PageNotAnInteger:
            self.pictures = paginator.page(1)
        except EmptyPage:
            self.pictures = paginator.page(paginator.num_pages)

        return self.get_ajax()

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Pictures, self).dispatch(*args, **kwargs)

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

    def filter_pictures(self, request):
        if request.raw_post_data != '':
            req_json = json.loads(request.raw_post_data)
            if req_json != []:
                self.pictures = self.pictures.filter(picture_tag__name__in=req_json);
