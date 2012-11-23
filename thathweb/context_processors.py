def site_name(request):
    from django.contrib.sites.models import Site
    return {'SITE_NAME' : Site.objects.get(id=1).name }
