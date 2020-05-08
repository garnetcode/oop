from django.urls import path
from .views import home, addStory, check, writers


urlpatterns = [
    path('', home, name='home'),
    path('writers/', writers, name='writers'),
    path('check/', check, name='check'),
    path('publish/', addStory, name='publish'),

]