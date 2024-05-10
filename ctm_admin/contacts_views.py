from django.views.generic import ListView, DeleteView, UpdateView, DetailView
from utils.models import ContactUs
from .mixins import CheckAdminMixin
from django.urls import reverse_lazy
from .forms import ContactUs_Msg_Form

class ContactUsListview(CheckAdminMixin,ListView):
    model = ContactUs
    template_name = 'ctm_admin/contacts_msg/contacts_list.html'
    context_object_name = 'contacts'
    model_permissions = {
        'utils': ['view_contactus']
    }

class ContactUsDetailView(CheckAdminMixin,DetailView):
    model = ContactUs
    template_name = 'ctm_admin/contacts_msg/contactus_detail.html'
    context_object_name = 'contact'
    model_permissions = {
        'utils': ['view_contactus']
    }

class ContactUsUpdateView(CheckAdminMixin,UpdateView):
    model = ContactUs
    form_class = ContactUs_Msg_Form
    template_name = 'ctm_admin/contacts_msg/contactus_update_form.html'
    context_object_name = 'contact'
    model_permissions = {
        'utils': ['change_contactus']
    }

    def get_success_url(self):
        return reverse_lazy('ctm_admin-contactus_detail', kwargs={'pk': self.object.pk})

class ContactUsDeleteView(CheckAdminMixin,DeleteView):
    model = ContactUs
    template_name = 'ctm_admin/contacts_msg/contactus_confirm_delete.html'
    context_object_name = 'contact'
    success_url = reverse_lazy('ctm_admin-contactus_list')
    model_permissions = {
        'utils': ['delete_contactus']
    }