from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import forms
import models
from thathweb.views import ThathwebBaseView

class ThathwebBase(ThathwebBaseView):

    template_name = "nacha/index.html"

    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        self.menu['nacha']['active'] = True
        return self.render_to_response({'user' : user, 'menu' : self.menu })

class NachaSettings(ThathwebBaseView):

    template_name = 'nacha/settings.html'

    def __init__(self):
        super(NachaSettings, self).__init__()
        self.menu['nacha']['active'] = True
        self.menu['nacha']['submenu']['settings']['active'] = True

    def get(self, request, *args, **kwargs):
        nacha_settings = models.NachaSettings.objects.all().filter(user_id=request.user.id)

        if nacha_settings.count() == 0:
            form = forms.NachaSettings()
        else:
            form = forms.NachaSettings(instance=nacha_settings[0])

        return self.render_to_response({'menu' : self.menu, 'form' : form.as_p()})

    def post(self, request, *args, **kwargs):
        nacha_settings = models.NachaSettings.objects.all().filter(user_id=request.user.id)

        if nacha_settings.count() == 0:
            nacha_settings = models.NachaSettings(user=request.user)
            form = forms.NachaSettings(request.POST, instance=nacha_settings)
        else:
            form = forms.NachaSettings(request.POST, instance=nacha_settings[0])

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('thathweb.nacha_creator.settings'))
        else:
            return self.render_to_response({'menu' : self.menu, 'form' : form.as_p()})

class NachaCreate(ThathwebBaseView):

    template_name = "nacha/gen.html"

    def __init__(self):
        super(NachaCreate, self).__init__()
        self.menu['nacha']['active'] = True
        self.menu['nacha']['submenu']['gen']['active'] = True

    def get(self, request, *args, **kwargs):
        settings = models.NachaSettings.objects.get(user=request.user)

        header = models.NachaHeader()
        header.immediate_origin      = settings.origin_routing_number
        header.immediate_destination = settings.dest_routing_number
        header.file_id_mod           = 'A'
        header.immediate_origin_name = settings.origin_name
        header.immediate_dest_name   = settings.dest_name

        form = forms.NachaHeader(instance=header)
        return self.render_to_response({'menu' : self.menu, 'form' : form.visible_fields()})

class NachaCreateBatch(ThathwebBaseView):

    template_name = "nacha/batch.html"

    def get(self, request, *args, **kwargs):
        settings = models.NachaSettings.objects.get(user=request.user)

        batch_header = models.NachaBatchHeader()
        batch_header.orig_stat_code = '1'
        batch_header.company_name = settings.origin_name[:12]
        form = forms.NachaBatchHeader(instance=batch_header)

        return self.render_to_response({'form' : form.visible_fields()})

class NachaCreateRecordEntry(ThathwebBaseView):

    template_name = "nacha/entry.html"

    def get(self, request, *args, **kwargs):
        code = request.GET.get('std_ent_cls_code')
        form = forms.NachaRecordEntry()
        form = [ field for field in form.visible_fields() if field.name in form.entry_field_sets.get(code) ] 

        return self.render_to_response({'form' : form})

class NachaBatches(ThathwebBaseView):

    template_name = "nacha/batches.html"

    def get(self, request, *args, **kwargs):
        self.menu['nacha']['active'] = True
        self.menu['nacha']['submenu']['batches']['active'] = True
        return self.render_to_response({'menu' : self.menu})
