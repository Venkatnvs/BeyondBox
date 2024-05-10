from django.urls import path
from .views import *

urlpatterns = [
    path("courses", CountryByApply, name="applies-courses"),
    path("courses/<int:id>/apply", ApplyForCourse.as_view(), name="applies-courses-apply"),
]