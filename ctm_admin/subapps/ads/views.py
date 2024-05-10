from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse,reverse_lazy
from ctm_admin.subapps.ads.utils import GetAds
from django.views import View
from django.views.generic import ListView,UpdateView,DetailView,DeleteView,CreateView
from ctm_admin.mixins import CheckAdminMixin
from .models import AdsBase,AdsSize
from .forms import AdsBaseForm,AdsSizeForm
from django.shortcuts import render,redirect

def get_new_ad_refresh(request):
    size = request.GET.get('size', '300x200')
    url, forward, H, W = GetAds(size)
    html_send = render_to_string('ads_snippets/ads_refresh.html', {'url': url, 'forward': forward, 'H': H, 'W': W, 'size':size})
    return JsonResponse({'new_ad_html': html_send})

# Ads Crud

class AdminADS(CheckAdminMixin,ListView):
    model = AdsBase
    template_name = 'ctm_admin/ads/ads_list-view.html'
    model_permissions = {
        'ads': ['view_adsbase']
    }

class AdsDetailView(CheckAdminMixin,DetailView):
    model = AdsBase
    template_name = 'ctm_admin/ads/ads_detail.html'
    context_object_name = 'ad'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    model_permissions = {
        'ads': ['view_adsbase']
    }

class AdsEditView(CheckAdminMixin,UpdateView):
    model = AdsBase
    form_class = AdsBaseForm
    template_name = 'ctm_admin/ads/ads_edit.html'
    context_object_name = 'ad'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    model_permissions = {
        'ads': ['change_adsbase']
    }

    def get_success_url(self):
        return reverse_lazy('ctm_admin-ads_detail', kwargs={'uuid': self.object.uuid})

class AdsDeleteView(CheckAdminMixin,DeleteView):
    model = AdsBase
    template_name = 'ctm_admin/ads/ads_confirm_delete.html'
    context_object_name = 'ad'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    success_url = reverse_lazy('ctm_admin-ads-list-view')
    model_permissions = {
        'ads': ['delete_adsbase']
    }

class AdsCreateView(CheckAdminMixin,CreateView):
    model = AdsBase
    form_class = AdsBaseForm
    template_name = 'ctm_admin/ads/ads_create.html'
    success_url = reverse_lazy('ctm_admin-ads-list-view')
    model_permissions = {
        'ads': ['add_adsbase']
    }

# Ad Size Crud views
class AdsSize_List_Create(CheckAdminMixin,View):
    template_name = 'ctm_admin/ads/ads_size_list_create.html'
    model_permissions = {
        'ads': ['add_adssize','view_adssize']
    }

    def get(self, request, *args, **kwargs):
        sizes = AdsSize.objects.all()
        form = AdsSizeForm()
        return render(request, self.template_name, {'sizes': sizes, 'form': form})

    def post(self, request, *args, **kwargs):
        form = AdsSizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ctm_admin-ads_size_list_create')
        else:
            sizes = AdsSize.objects.all()
            return render(request, self.template_name, {'sizes': sizes, 'form': form})

class AdsSizeDeleteView(CheckAdminMixin,DeleteView):
    model = AdsSize
    template_name = 'ctm_admin/ads/ads_size_confirm_delete.html'
    context_object_name = 'size'
    success_url = reverse_lazy('ctm_admin-ads_size_list_create')
    model_permissions = {
        'ads': ['delete_adssize']
    }