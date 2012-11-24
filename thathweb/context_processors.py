from views import get_menu

def site_name(request):
    from django.contrib.sites.models import Site
    return {'SITE_NAME' : Site.objects.get(id=1).name }

def site_menu(request):
    url = request.path.split('/')
    menu = get_menu()

    try:
        if url[1] == '':
            menu['home']['active'] = True
        else:
            menu[url[1]]['active'] = True

        if len(url) >= 4:
            menu[url[1]]['submenu'][url[2]]['active'] = True

    except (KeyError, IndexError):
        pass

    return {'MENU' : menu }
