from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import AvaliableCourses,ApplyCourse
from django.views import View
from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import os
from django.conf import settings
import json

def CountryByApply(request):
    crs = AvaliableCourses.objects.filter(is_active=True)
    context = {
        'data':crs
    }
    return render(request,'applies/bycnt/index.html',context)

class ApplyForCourse(LoginRequiredMixin,View):
    file_path = os.path.join(settings.BASE_DIR,'datasets/countries.json')

    def check_url_id(self,id):
        av = get_object_or_404(AvaliableCourses,id=id)
        return av

    def get_cnt(self,c):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        country = ""
        for i in data:
            if c.lower() == i['code'].lower():
                country = i['name']
        return country

    def get(self,request,id):
        av = self.check_url_id(self.kwargs.get("id", None))
        if not request.user.is_authenticated:
            messages.info(request, "You need to be logged in to apply for this course.")
            return redirect('accounts-login')
        if av:
            acc = ApplyCourse.objects.filter(user=request.user, course=av)
            if acc.exists():
                messages.info(request, "Course Already Applied.")
                return redirect('applies-courses')
        context = {
            "av_course":av,
            "cnt_a":self.get_cnt(av.country_code)
        }
        return render(request, 'applies/bycnt/apply_form.html',context)
    
    def post(self,request,id):
        course = request.POST['course']
        av = self.check_url_id(self.kwargs.get("id", None))
        if not request.user.is_authenticated:
            messages.info(request, "You need to be logged in to apply for this course.")
            return redirect('accounts-login')
        if av:
            acc = ApplyCourse.objects.filter(user=request.user, course=av)
            if acc.exists():
                messages.info(request, "Course Already Applied.")
                return redirect('applies-courses')
        if not course:
            messages.error(request,"Course cannot be Empty")
            return redirect('applies-courses-apply',id=id)
        preferred_college = request.POST.getlist('preferred_college[]')
        if len(preferred_college)<=0:
            messages.error(request,"Preferred colleges cannot be Empty")
            return redirect('applies-courses-apply',id=id)
        abroad_year = request.POST['abroad_year']
        if not abroad_year:
            messages.error(request,"Year Of Study cannot be Empty")
            return redirect('applies-courses-apply',id=id)
        season = request.POST['season']
        preferred_college_list = '\r\n'.join([college for college in preferred_college])
        av = self.check_url_id(id)
        ac = ApplyCourse.objects.create(
            user = request.user,
            course = av,
            preferred_college = preferred_college_list,
            course_type = course,
            abroad_year = abroad_year,
            abroad_season = season,
            is_active = True
        )
        av.save()
        messages.success(request,f"Applied to Course in {av.country}.")
        return redirect('applies-courses')