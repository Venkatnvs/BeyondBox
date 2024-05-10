from django import forms
from utils.models import ContactUs
from accounts.models import UserType
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import Permission

User = get_user_model()

class ContactUs_Msg_Form(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone_no', 'message', 'by_login_user','is_replyed','is_ignored']

    def __init__(self, *args, **kwargs):
        super(ContactUs_Msg_Form, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['phone_no'].widget.attrs['readonly'] = True
        self.fields['message'].widget.attrs['readonly'] = True

    def clean_name(self):
        if self.instance and self.cleaned_data['name'] != self.instance.name:
            raise forms.ValidationError("Name cannot be edited.")
        return self.cleaned_data['name']

    def clean_email(self):
        if self.instance and self.cleaned_data['email'] != self.instance.email:
            raise forms.ValidationError("Email cannot be edited.")
        return self.cleaned_data['email']

    def clean_phone_no(self):
        if self.instance and self.cleaned_data['phone_no'] != self.instance.phone_no:
            raise forms.ValidationError("Phone number cannot be edited.")
        return self.cleaned_data['phone_no']
    
    def clean_message(self):
        if self.instance and self.cleaned_data['message'] != self.instance.message:
            raise forms.ValidationError("message cannot be edited.")
        return self.cleaned_data['message']

class UserTypeForm(forms.ModelForm):
    class Meta:
        model = UserType
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        super(UserTypeForm, self).__init__(*args, **kwargs)
        allowed_apps = ['accounts', 'ads','utils','ctm_admin','applies','dashboard']
        app_permissions = Permission.objects.filter(content_type__app_label__in=allowed_apps)
        permission_choices = [(perm.codename, f'{perm.content_type.app_label} - {perm.name} Data',perm.id) for perm in app_permissions]
        self.fields['permissions'].choices = permission_choices
        self.fields['permissions'].help_text = 'Select Multiple permissions to be Granted'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Name of UserType (ex: SubAdmin..)'
        self.fields['permissions'].widget.attrs['placeholder'] = 'Select all the permissions Granted'
    
class UserForm(UserCreationForm):
    user_type = forms.ModelChoiceField(queryset=UserType.objects.all(), required=False)
    class Meta:
        model = User
        fields = ['email','password1','password2','first_name','last_name','is_staff','user_type']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.user_type = self.cleaned_data['user_type']
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    user_type = forms.ModelChoiceField(queryset=UserType.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_staff', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.user_type = self.cleaned_data['user_type']
            user.save()
        return user