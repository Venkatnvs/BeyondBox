from django.urls import path,include
from .views import *
from .contacts_views import *

urlpatterns = [
    path("", Main, name="ctm_admin-main"),

    # User Type
    path('usertypes/', UserTypeListView.as_view(), name='ctm_admin-usertype_list'),
    path('usertypes/create/', UserTypeCreateView.as_view(), name='ctm_admin-usertype_create'),
    path('usertypes/<int:pk>/', UserTypeDetailView.as_view(), name='ctm_admin-usertype_detail'),
    path('usertypes/<int:pk>/edit/', UserTypeUpdateView.as_view(), name='ctm_admin-usertype_edit'),
    path('usertypes/<int:pk>/delete/', UserTypeDeleteView.as_view(), name='ctm_admin-usertype_delete'),

    # Users
    path("create-users/", CreateUser.as_view(), name="ctm_admin-create-users"),
    path("all-users/", UsersListview.as_view(), name="ctm_admin-all-users"),
    path("users/<int:pk>/", UsersDetailsview.as_view(), name="ctm_admin-users-details"),

    # Staff Users
    path("staff-users/", StaffUserList.as_view(), name="ctm_admin-staff-users"),
    path('staff-users/<int:pk>/', StaffUserDetails.as_view(), name='ctm_admin-staff-users-detail'),
    path('staff-users/<int:pk>/edit/', StaffUserUpdateView.as_view(), name='ctm_admin-staff-users-edit'),
    path('staff-users/<int:pk>/delete/', StaffUserDeleteView.as_view(), name='ctm_admin-staff-users-delete'),
    path('staff-users/<int:pk>/change_password/', StaffUserChangePassword.as_view(), name='ctm_admin-staff-users-change_password'),

    # Contact Messages
    path("contactus/", ContactUsListview.as_view(), name="ctm_admin-contactus_list"),
    path('contactus/<int:pk>/', ContactUsDetailView.as_view(), name='ctm_admin-contactus_detail'),
    path('contactus/<int:pk>/edit/', ContactUsUpdateView.as_view(), name='ctm_admin-contactus_edit'),
    path('contactus/<int:pk>/delete/', ContactUsDeleteView.as_view(), name='ctm_admin-contactus_delete'),

    # Data Export
    path("export-excel-all-users/", UserDataExportExcel, name="ctm_admin-export-excel-all-users"),
    path("export-csv-all-users/", UserDataExportCsv, name="ctm_admin-export-csv-all-users"),

    # ADS System
    path("ads/",include('ctm_admin.subapps.ads.urls')),
]