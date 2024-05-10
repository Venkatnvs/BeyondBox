from django import forms
from .models import AdsBase,AdsSize

class AdsBaseForm(forms.ModelForm):
    class Meta:
        model = AdsBase
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(AdsBaseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Enter Title'
        self.fields['url'].widget.attrs['placeholder'] = 'Enter Ad Image URL'
        self.fields['forward_url'].widget.attrs['placeholder'] = 'Enter Forward URL'

class AdsSizeForm(forms.ModelForm):
    class Meta:
        model = AdsSize
        fields = ['width', 'height']

    def __init__(self, *args, **kwargs):
        super(AdsSizeForm, self).__init__(*args, **kwargs)
        self.fields['width'].widget.attrs['placeholder'] = 'Enter Width of New Ads'
        self.fields['height'].widget.attrs['placeholder'] = 'Enter Height of New Ads'
