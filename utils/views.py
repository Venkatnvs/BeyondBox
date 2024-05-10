from django.shortcuts import render
from django.views import View
import json
from validate_email import validate_email
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import os
from django.conf import settings
from django.contrib import messages
from .models import ContactUs

User = get_user_model()

class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry email is already registered'})
        return JsonResponse({'email_valid':True})

class CollegeList(View):
    file_path = os.path.join(settings.BASE_DIR,'datasets/colleges.json')
    
    def get(self,request):
        term = request.GET.get('q', '')
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        filtered_colleges = [entry['college'] for entry in data if term.lower() in entry['college'].lower()]
        return JsonResponse(filtered_colleges, safe=False)

class CountryList(View):
    file_path = os.path.join(settings.BASE_DIR,'datasets/countries.json')
    
    def get(self,request):
        term = request.GET.get('q', '')
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        filtered_colleges = [entry['name'] for entry in data if term.lower() in entry['name'].lower()]
        return JsonResponse(filtered_colleges, safe=False)
    
class CollegeListWorld(View):
    file_path = os.path.join(settings.BASE_DIR,'datasets/world_universities.json')

    def get(self,request):
        term = request.GET.get('q', '')
        term2 = request.GET.get('c', '')
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        filtered_colleges = [entry['name'] for entry in data if ((term.lower() in entry['name'].lower()) and term2.lower() in entry['country'].lower())]
        return JsonResponse(filtered_colleges, safe=False)

def TermsConds(request):
    return render(request,'utils/terms_conds.html')

class ContactUsForm(View):
    def get(self,request):
        return render(request,"utils/contact_us.html")
    
    def post(self,request):
        email = request.POST['email']
        name = request.POST['name']
        mobile_no = request.POST['mobile_no']
        mobile_no_full = request.POST['mobile_no_full']
        message = request.POST['message']
        if request.user.is_authenticated:
            by_lgu = True
        else:
            by_lgu = False
        context = {
            "FieldValues":request.POST
        }
        if not validate_email(email):
            messages.error(request,"Email is invalid")
            return render(request,"utils/contact_us.html",context)
        if len(mobile_no)>10:
            messages.error(request,"Mobile Number is invalid")
            return render(request,"utils/contact_us.html",context)
        a = ContactUs.objects.create(
            name= name,
            email = email,
            phone_no = mobile_no_full,
            message = message,
            by_login_user = by_lgu,
        )
        a.save()
        messages.success(request,"We will get in touch soon.")
        return render(request,"utils/contact_us.html")
