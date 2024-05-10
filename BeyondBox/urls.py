from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from ctm_admin.subapps.ads.views import get_new_ad_refresh

fav_icon = RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)

urlpatterns = [
    path('db-admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('dashboard.urls')),
    path('analysis/', include('analysis.urls')),
    path('admin/', include('ctm_admin.urls')),
    path('ads/get_new_refresh',get_new_ad_refresh,name="ads-refresh"),
    path('utils/', include('utils.urls')),
    re_path(r'^favicon\.ico$', fav_icon),
]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)