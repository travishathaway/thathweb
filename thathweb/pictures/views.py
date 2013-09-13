import json
from pprint import pprint

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.db.models import Count

from thathweb import settings 
from thathweb.views import ThathwebBaseViewNoAuth
import models

class Pictures(ThathwebBaseViewNoAuth):
    template_name = "pictures/index.html"
    picture_per_page = 35

    def __init__(self,*args,**kwargs):
        self.filter_tags = []
        self.tags = {}
        self.pictures = models.Picture.objects.all().filter(published=True)
        super(ThathwebBaseViewNoAuth, self).__init__(*args,**kwargs)

    def get(self, request, *args, **kwargs):
        self.page = kwargs.get('page',1)
        self.current_tag = kwargs.get('tag','')

        if self.current_tag != '':
            self.filter_tags.append(self.current_tag)
            self.pictures = self.pictures.filter(picture_tag__name=self.current_tag)

        #set the tags
        self.get_tags()

        # set up paginator
        paginator = Paginator(self.pictures, self.picture_per_page)
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
                'tags'     : self.tags,
                'active_tag_count' : self.active_tag_count,
                'current_tag' : self.current_tag,
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
            { 'tags' : self.tags,
              'active_tag_count' : self.active_tag_count, }
        )

        ret_json = json.dumps({
            'pictures_html' : pictures_html,
            'paginator_html' : paginator_html,
            'tags_html' : tags_html,
            'page': self.page,
        })

        response = HttpResponse(ret_json, mimetype="application/json" )

        return response

    def get_regular(self, request):
        return

    def post(self, request, *args, **kwargs):
        self.filter_pictures(request)
        paginator = Paginator(self.pictures, self.picture_per_page)
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
        tag_counts = {}

        for picture in self.pictures:
            for tag in picture.picture_tag.all():
                if tag_counts.get(tag.name) != None:
                    tag_counts[tag.name]['count'] += 1
                else:
                    tag_counts[tag.name] = {
                        'count' : 1,
                        'name'  : tag.name,
                        'title' : tag.title,
                        'active': ( tag.name in self.filter_tags),
                    }

        self.tags = tag_counts
        self.active_tag_count = len(
            [x for x in self.tags.itervalues() if x['active'] ]
        )

    def filter_pictures(self, request):
        if request.raw_post_data != '':
            self.filter_tags = json.loads(request.raw_post_data)
            for tag in self.filter_tags:
                self.pictures = self.pictures.filter(picture_tag__name=tag)
            self.pictures = self.pictures.distinct('id');
