import json

from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from pure_pagination import Paginator, PageNotAnInteger
import os

from posts.models import Post, SoundCloudSongs
from models import IncidentReport
from settings import STATIC_ROOT, STATIC_URL

def get_menu():

    return {
        'home' : {
            'url': '/',
            'title': 'Home',
            'active': False,
            'display': True,
        },
        'lab': {
            'url': '/lab/',
            'title': 'Lab',
            'active': False,
            'display': True,
        },
        'pictures': {
            'url': '/pictures/',
            'title': 'Pictures',
            'active': False,
            'display' : True,
        },
        'downloads': {
            'url': '/downloads/',
            'title': 'Downloads',
            'active': False,
            'display': True,
        },
       'nacha': {
            'url': '/nacha/',
            'active': False,
            'title': 'Nacha',
            'display': False,
            'submenu': {
                'settings': {
                    'url': reverse('thathweb.nacha_creator.settings'),
                    'active': False,
                    'title': 'Settings',
                },
                'generate': {
                    'url': reverse('thathweb.nacha_creator.gen'),
                    'active': False,
                    'title': 'Generate',
                },
                'batches': {
                    'url': reverse('thathweb.nacha_creator.batches'),
                    'active': False,
                    'title': 'Batches',
                },
            },
        },
    }


class ThathwebBaseView(TemplateView):
    '''
    Base view for the site. Everything on the site
    requires you to be logged in to do anything
    '''

    template_name = "base.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThathwebBaseView, self).dispatch(*args, **kwargs)


class ThathwebBaseViewNoAuth(TemplateView):
    '''
    Base view for the site. Everything on the site
    requires you to be logged in to do anything
    '''

    template_name = "base.html"

    def dispatch(self, *args, **kwargs):
        return super(ThathwebBaseViewNoAuth, self).dispatch(*args, **kwargs)


class HomePage(ThathwebBaseViewNoAuth):
    """
    Home page view.  Recent posts and songs are shown here
    """

    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-date')[:5]
        songs = SoundCloudSongs.objects.all()[:3]
        return self.render_to_response({'posts': posts, 'songs': songs})


class LabPage(ThathwebBaseViewNoAuth):
    """
    Page to show all the various "Lab" items.  Like my nacha generator
    """

    template_name = "lab.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class DownloadsPage(ThathwebBaseViewNoAuth):
    """
    Page that shows all the current downloads
    """

    template_name = "downloads.html"
    download_file_exts = ['.mp3', 'flac']

    def get(self, request, *args, **kwargs):
        try:
            download_files = []
            files = os.listdir(STATIC_ROOT + 'kmhd/')

            for file in files:
                if file[-4:] in self.download_file_exts:
                    download_files.append({
                        'name': file,
                        'link': STATIC_URL + 'kmhd/' + file,
                    })

        except(OSError, IndexError):
            download_files = []

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        pager = Paginator(download_files, 20, request=request)
        download_files = pager.page(page)

        page_data = {
            'files': download_files
        }

        return self.render_to_response(page_data)


class IncidentReportPage(ThathwebBaseViewNoAuth):
    """
    Page that shows all the current downloads
    """
    template_name = "incident_report.html"

    def get(self, request, *args, **kwargs):
        incident_reports = IncidentReport.objects.filter(
            description__contains='WOODSTOCK'
        ).filter(
            description__contains='TRAFFIC'
        ).order_by('-date_time')

        page_data = {
            'incident_reports': incident_reports,
        }

        return self.render_to_response(page_data)


class NoSmokingPage(ThathwebBaseViewNoAuth):
    """
    Page that shows number of days since my last cigarette
    """
    template_name = "no_smoking.html"

    def get(self, request, *args, **kwargs):

        return self.render_to_response()
