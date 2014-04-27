import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from thathweb.utils import get_number_paginator
from models import MediaFile
from forms import MediaFileForm
from thathweb.settings import STATIC_URL


@login_required
def media_add(request):
    """
    This view just renders the add template. The files are uploaded
    view ajax and handled in a different view function (see media_add_ajax)
    """

    return render(request, 'media/media/add.html')


@login_required
def media_add_ajax_partial(request):
    """
    This renders the partial form of the add files page. We use
    this in order to place it on places in various pages.
    """

    return render(request, 'media/media/add_ajax_partial.html')


@login_required
def media_addexisting_ajax_partial(request):
    """
    This renders the partial template for adding files that are
    currently in the sites media library
    """
    current_file_pks = [int(x) for x in request.GET.getlist('files')]

    search_text = request.GET.get('search_text')

    if search_text:
        media_files = MediaFile.objects.filter(title__icontains=search_text)
    else:
        media_files = MediaFile.objects.all()

    media_files = media_files.exclude(
        pk__in=current_file_pks).order_by('-created')
    page = request.GET.get('page', 1)

    media_files = get_number_paginator(media_files, page=page, per_page=12)

    page_data = {
        'page': media_files,
    }

    return render(
        request,
        'media/media/addexisting_ajax_partial.html',
        page_data
    )


@login_required
def media_add_ajax(request):
    """
    This is the end point for the ajax file uploads. It will
    always return "application/json".
    """
    if request.method == 'POST':
        uploaded_files = []

        for key, upload in request.FILES.items():
            media_file = MediaFile()
            media_file.title = request.POST.get('title')
            media_file.slug = slugify(media_file.title)
            media_file.caption = request.POST.get('caption')
            media_file.created_by = request.user
            media_file.media_file = upload

            if upload.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                media_file.thumbnail = upload
                media_file.thumbnail_medium = upload

            media_file.save()

            if media_file.thumbnail == '':
                thumbnail_url = STATIC_URL + 'img/default_thumbnail.png'
            else:
                thumbnail_url = media_file.thumbnail.url

            uploaded_files.append({
                'file_name': media_file.media_file.name,
                'pk': media_file.pk,
                'thumbnail_url': thumbnail_url,
                'title': media_file.title,
            })

        # Remember, this has to be JSON serializable
        ret_json = {
            'files': uploaded_files,
            'success': True,
        }

        response = HttpResponse(
            json.dumps(ret_json),
            content_type="application/json"
        )
        response['Content-Disposition'] = 'inline; filename="files.json"'

        return response

    else:
        return HttpResponseRedirect(reverse('thathweb.media.views.media_add'))


@login_required
def media_view(request, pk):
    '''
    Provides a very simple view of the object. If it's a picture
    we show the picture. If that's not the case, we show a link
    to the file. Not meant to be public.
    '''

    media_file = get_object_or_404(MediaFile, pk=pk)

    page_data = {
        'media_file': media_file,
    }

    return render(request, 'media/media/view.html', page_data)


@login_required
def media_edit(request, pk):
    """
    Form used for editing a single file. It uses a traditional
    html form and not ajax
    """
    media_file = get_object_or_404(MediaFile, pk=pk)

    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES, instance=media_file)

        if form.is_valid():
            media_file = form.save(commit=False)
            incoming_file = request.FILES.get('media_file')

            if incoming_file:
                if incoming_file.content_type in [
                    'image/jpeg', 'image/png', 'image/gif'
                ]:
                    media_file.thumbnail = incoming_file
                    media_file.thumbnail_medium = incoming_file

            media_file.save()

            # Redirect the user to simple view upon successful update
            messages.success(request, "Media File saved successfully")
            return redirect(media_view, media_file.pk)
    else:
        form = MediaFileForm(instance=media_file)

    page_data = {
        'media_file': media_file,
        'form': form,
    }

    return render(request, 'media/media/edit.html', page_data)


@login_required
def media_list(request):
    '''
    Admin page for list of all media.
    '''
    page = request.GET.get('page', 1)
    search_text = request.GET.get('search_text')

    if request.GET.get('partial'):
        template = 'media/media/list_partial.html'
    else:
        template = 'media/media/list.html'

    if search_text:
        media_files = MediaFile.objects.filter(title__icontains=search_text)
    else:
        media_files = MediaFile.objects.all()

    media_files = media_files.order_by('-created')
    media_files = get_number_paginator(media_files, per_page=18, page=page)

    page_data = {
        'page': media_files,
    }

    return render(request, template, page_data)


@login_required
def image_gallery_list(request):
    '''
    Admin page for listing image galleries
    '''
    page = request.GET.get('page', 1)
    image_galleries = ImageGallery.objects.all()

    image_galleries = get_number_paginator(image_galleries, page=page)

    page_data = {
        'image_galleries': image_galleries,
    }

    return render(request, 'media/image_gallery/list.html', page_data)


@login_required
def image_gallery_add(request):
    '''
    Page for adding an image gallery
    '''
    if request.method == 'POST':
        form = ImageGalleryForm(request.POST)
        files_pk = [int(x) for x in request.POST.getlist('files[]', [])]

        if form.is_valid():
            image_gallery = form.save()
            image_gallery.media_files = files_pk
            image_gallery.save()

            messages.success(request, "Image gallery added successfully")
            return redirect(image_gallery_view, image_gallery.slug)
        else:
            media_files = MediaFile.objects.filter(id__in=files_pk)
    else:
        media_files = []
        form = ImageGalleryForm()

    page_data = {
        'form': form,
        'media_files': media_files,
    }

    return render(request, 'media/image_gallery/add.html', page_data)


@login_required
def image_gallery_edit(request, slug):
    '''
    Edit page for image galleries
    '''
    image_gallery = get_object_or_404(ImageGallery, slug=slug)

    if request.method == 'POST':
        form = ImageGalleryForm(request.POST, instance=image_gallery)
        files_pk = [int(x) for x in request.POST.getlist('files[]', [])]

        if form.is_valid():
            image_gallery = form.save()
            image_gallery.media_files = files_pk
            image_gallery.save()

            messages.success(request, "Image gallery added successfully")
            return redirect(image_gallery_view, image_gallery.slug)
        else:
            media_files = MediaFile.objects.filter(id__in=files_pk)
    else:
        form = ImageGalleryForm(instance=image_gallery)
        media_files = image_gallery.media_files.all()

    page_data = {
        'image_gallery': image_gallery,
        'form': form,
        'media_files': media_files,
    }

    return render(request, 'media/image_gallery/edit.html', page_data)


def image_gallery_view(request, slug):
    '''
    This is the public view for the image gallery.  If the image gallery is
    not published than we return a 404
    '''

    if request.user.is_staff:
        image_gallery = get_object_or_404(ImageGallery, slug=slug)
    else:
        image_gallery = get_object_or_404(ImageGallery, slug=slug,
                                          published=True)

    page_data = {
        'image_gallery': image_gallery,
    }

    return render(request, 'media/image_gallery/view.html', page_data)
