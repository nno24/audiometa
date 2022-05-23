from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_home, name='home'),
    path('upload_media/', views.upload_media, name='upload_media'),
]