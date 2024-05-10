from django.urls import path, include
from .views import *
from .life_skills import *

urlpatterns = [
    path('', Home, name='dashboard-home' ),
    path('profile/', ProfileUpdate.as_view(), name='dashboard-profile' ),
    path('update-password/', UpdatePassword.as_view(), name='dashboard-update-password' ),

    # Test
    path('test/dsu/1', Test, name='dashboard-test' ),
    path('test/dsu/2', Test3, name='dashboard-test' ),

    # ChatBot
    path('chat/', chat_view, name='chat_view'),

    # Cost Of Study
    path("cost-of-study/usa/", CostStudyUsa, name="cost-of-study-usa"),
    path("cost-of-study/australia/", CostStudyAustralia, name="cost-of-study-australia"),
    path("cost-of-study/uk/", CostStudyUk, name="cost-of-study-uk"),
    path("cost-of-study/canada/", CostStudyCanada, name="cost-of-study-canada"),
    path("cost-of-study/new-zealand/", CostStudyNewZealand, name="cost-of-study-new-zealand"),

    # About Page
    path('about/',AboutPage,name="dashboard-about"),
    
    # Life Skills
    path("life-skills", LifeSkillsPage, name="dashboard-life-skills"),

    # Tests
    path("aptitude-test", AptitudeTest, name="dashboard-aptitude-test"),
    path("soft-skills-test", SoftSkillsTest, name="dashboard-soft-skills-test"),
]