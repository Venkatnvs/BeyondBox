from django.urls import path
from .views import * 

urlpatterns = [
    path('', index, name='analysis-index'),
    path('upload/', upload, name='analysis-upload'),
    path('audio-analysis/', AudioAnalysis, name='analysis-audio-analysis'),
]
