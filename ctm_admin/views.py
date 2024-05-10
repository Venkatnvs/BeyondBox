from django.shortcuts import render,HttpResponse,get_object_or_404
from django.http import Http404
from .mixins import CheckAdminMixin
from .decorators import check_admin_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView,DeleteView
from accounts.models import UserProfile,CustomUser,UserType
import xlwt
import csv
import datetime
from django.db.models import F,Value, CharField
from django.db.models.functions import Cast, Coalesce, Concat
from .dashboard import chart_view
import json
from django.core.serializers.json import DjangoJSONEncoder
from utils.models import ContactUs
from .forms import UserForm,UserTypeForm,UserUpdateForm
from django.contrib.auth import get_user_model
from django.urls import reverse,reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .subapps.ads.models import AdsBase

User = get_user_model()

# DashBoard
model_permissions_main = {
    'ctm_admin': ['view_dashboard'],
}

@check_admin_required(model_permissions=model_permissions_main)
def Main(request):
    users = CustomUser.objects.filter(is_superuser=False,is_staff=False)
    staffusers = CustomUser.objects.filter(is_superuser=False,is_staff=True)
    ads = AdsBase.objects.filter(is_active=True)
    ads_count = ads.count()
    user_count = users.count()
    staffuser_count = staffusers.count()
    contact_msg_count = ContactUs.objects.filter(is_replyed=False).count()
    a,b= chart_view()
    context = {
        "user_count":user_count,
        "ads_count":ads_count,
        "staffuser_count":staffuser_count,
        "contact_msg_count":contact_msg_count,
        "graphs_1":json.dumps(a,cls=DjangoJSONEncoder),
        "graphs_2":json.dumps(b,cls=DjangoJSONEncoder),
    }
    return render(request,'ctm_admin/index.html',context)

# Users
class UsersListview(CheckAdminMixin,ListView):
    model = UserProfile
    context_object_name = 'users'
    template_name = 'ctm_admin/users/allusers_list.html'
    model_permissions = {
        'accounts': ['view_customuser','view_userprofile']
    }

    def get_queryset(self):
        return UserProfile.objects.filter(user__is_superuser=False,user__is_staff=False).order_by('created_at')

class UsersDetailsview(CheckAdminMixin,DetailView):
    model = UserProfile
    template_name = 'ctm_admin/users/users_details.html'
    context_object_name = 'users'
    model_permissions = {
        'accounts': ['view_customuser','view_userprofile']
    }

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.user.is_superuser:
            return HttpResponse('403 Something went Wrong!.')
        if user.user.is_staff:
            return HttpResponse('User is a Staff user.')
        return super().dispatch(request, *args, **kwargs)
    
# Staff Users

class StaffUserList(CheckAdminMixin,ListView):
    model = CustomUser
    template_name = "ctm_admin/users/staff/staff_user_list.html"
    context_object_name = "users"
    model_permissions = {
        'accounts': ['view_customuser']
    }
    def get_queryset(self):
        return CustomUser.objects.filter(is_superuser=False,is_staff=True).order_by('date_joined')

class StaffUserDetails(CheckAdminMixin,DetailView):
    model = CustomUser
    template_name = "ctm_admin/users/staff/staff_user_details.html"
    context_object_name = "users"
    model_permissions = {
        'accounts': ['view_customuser']
    }
    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser:
            return HttpResponse('User is Not a Staff user.')
        if not user.is_staff:
            return HttpResponse('User is Not a Staff user.')
        return super().dispatch(request, *args, **kwargs)

class StaffUserUpdateView(CheckAdminMixin,UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'ctm_admin/users/staff/staff_user_update.html'
    context_object_name = 'users'
    success_url = reverse_lazy('ctm_admin-staff-users')
    model_permissions = {
        'accounts': ['change_customuser']
    }
    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser:
            return HttpResponse('User is Not a Staff user.')
        if not user.is_staff:
            return HttpResponse('User is Not a Staff user.')
        return super().dispatch(request, *args, **kwargs)
    
class StaffUserDeleteView(CheckAdminMixin,DeleteView):
    model = CustomUser
    template_name = 'ctm_admin/users/staff/staff_user_conform_delete.html'
    context_object_name = "users"
    success_url = reverse_lazy('ctm_admin-staff-users')
    model_permissions = {
        'accounts': ['delete_customuser']
    }
    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser:
            return HttpResponse('User is Not a Staff user.')
        if not user.is_staff:
            return HttpResponse('User is Not a Staff user.')
        return super().dispatch(request, *args, **kwargs)
    
class StaffUserChangePassword(CheckAdminMixin,PasswordChangeView):
    template_name = 'ctm_admin/users/staff/staff_user_change_password.html'
    context_object_name = "users"
    success_url = reverse_lazy('ctm_admin-staff-users')
    form_class = PasswordChangeForm
    model_permissions = {
        'accounts': ['change_userpassword']
    }
    def dispatch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(CustomUser, pk=user_id)
        if user.is_superuser or not user.is_staff:
            raise Http404("User is not a Staff user.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password was successfully changed.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error. Please try again.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(CustomUser, pk=user_id)
        context['users'] = user
        return context

class CreateUser(CheckAdminMixin,CreateView):
    model = User
    form_class = UserForm
    template_name = 'ctm_admin/users/create_new_user.html'
    success_url = reverse_lazy('ctm_admin-all-users')
    model_permissions = {
        'accounts': ['add_customuser']
    }

# User Type
class UserTypeListView(CheckAdminMixin,ListView):
    model = UserType
    template_name = 'ctm_admin/users/usertype_list.html'
    context_object_name = 'usertypes'
    model_permissions = {
        'accounts': ['view_usertype']
    }

class UserTypeCreateView(CheckAdminMixin,CreateView):
    model = UserType
    form_class = UserTypeForm
    template_name = 'ctm_admin/users/usertype_create.html'
    success_url = reverse_lazy('ctm_admin-usertype_list')
    model_permissions = {
        'accounts': ['add_usertype']
    }

class UserTypeDetailView(CheckAdminMixin,DetailView):
    model = UserType
    template_name = 'ctm_admin/users/usertype_detail.html'
    context_object_name = 'usertype'
    model_permissions = {
        'accounts': ['view_usertype']
    }

class UserTypeUpdateView(CheckAdminMixin,UpdateView):
    model = UserType
    form_class = UserTypeForm
    template_name = 'ctm_admin/users/usertype_update.html'
    context_object_name = 'usertype'
    success_url = reverse_lazy('ctm_admin-usertype_list')
    model_permissions = {
        'accounts': ['change_usertype']
    }

class UserTypeDeleteView(CheckAdminMixin,DeleteView):
    model = UserType
    template_name = 'ctm_admin/users/usertype_confirm_delete.html'
    context_object_name = 'usertype'
    success_url = reverse_lazy('ctm_admin-usertype_list')
    model_permissions = {
        'accounts': ['delete_usertype']
    }

# Export Data Users

@check_admin_required
def UserDataExportExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=UserData'+str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('UserInfo')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Email','Full Name','Gender','Mobile No.','Verification Status','Usn','College','Graduation Year','Abroad Country','Abroad Course','Abroad Preferred Country','Abroad Year','Abroad Season','Created at']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style =  xlwt.XFStyle()
    rows = UserProfile.objects.filter(user__is_superuser=False).annotate(
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        full_name=Coalesce(Concat(Cast('first_name', CharField()), Value(' '), Cast('last_name', CharField())), 'first_name')
        ).values_list(
            'user__email',
            'full_name',
            'gender',
            'mobile_no',
            'user__is_active',
            'usn','college',
            'graduation_year','country',
            'course','preferred_college',
            'abroad_year','abroad_season',
            'created_at')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response

@check_admin_required
def UserDataExportCsv(request):
    response = HttpResponse(content_type='text/csv')
    file_name = f'UserData{str(datetime.datetime.now())}.csv'
    response['Content-Disposition'] = 'attachment; filename='+file_name
    writer = csv.writer(response)
    writer.writerow(['Email','Full Name','Gender','Mobile No.','Verification Status','Usn','College','Graduation Year','Abroad Country','Abroad Course','Abroad Preferred Country','Abroad Year','Abroad Season','Created at'])

    rows = UserProfile.objects.filter(user__is_superuser=False).annotate(
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        full_name=Coalesce(Concat(Cast('first_name', CharField()), Value(' '), Cast('last_name', CharField())), 'first_name')
        ).values_list(
            'user__email',
            'full_name',
            'gender',
            'mobile_no',
            'user__is_active',
            'usn','college',
            'graduation_year','country',
            'course','preferred_college',
            'abroad_year','abroad_season',
            'created_at')

    for row in rows:
        writer.writerow(row)

    return response