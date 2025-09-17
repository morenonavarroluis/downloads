# descargas/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.video, name='video'),
    path('download_video', views.download_video, name='download_page'),
]