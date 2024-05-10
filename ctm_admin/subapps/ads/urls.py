from django.urls import path
from .views import *

urlpatterns = [
    # Ad Base
    path('ads-list-view/', AdminADS.as_view(), name='ctm_admin-ads-list-view'),
    path('create/', AdsCreateView.as_view(), name='ctm_admin-ads_create'),
    path('<uuid:uuid>/', AdsDetailView.as_view(), name='ctm_admin-ads_detail'),
    path('<uuid:uuid>/edit/', AdsEditView.as_view(), name='ctm_admin-ads_edit'),
    path('<uuid:uuid>/delete/', AdsDeleteView.as_view(), name='ctm_admin-ads_delete'),

    # Ad Size
    path('ads_sizes/', AdsSize_List_Create.as_view(), name='ctm_admin-ads_size_list_create'),
    path('ads_sizes/<int:pk>/delete/', AdsSizeDeleteView.as_view(), name='ctm_admin-ads_size_delete'),
]