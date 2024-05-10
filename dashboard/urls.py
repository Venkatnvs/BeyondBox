from django.urls import path, include
from .views import *
from .life_skills import *

urlpatterns = [
    path('', Home, name='dashboard-home' ),
    path('profile/', ProfileUpdate.as_view(), name='dashboard-profile' ),
    path('update-password/', UpdatePassword.as_view(), name='dashboard-update-password' ),

    # ChatBot
    path('chat/', chat_view, name='chat_view'),

    # About Page
    path('about/',AboutPage,name="dashboard-about"),
    
    # Life Skills
    path("life-skills", LifeSkillsPage, name="dashboard-life-skills"),

    # Tests
    path("aptitude-test", AptitudeTest, name="dashboard-aptitude-test"),
    path("soft-skills-test", SoftSkillsTest, name="dashboard-soft-skills-test"),

    # Premium
    path("premium/", GetPremium, name="dashboard-get-premium"),
]