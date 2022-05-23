from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_home, name='home'),
    path('upload_media/', views.upload_media, name='upload_media'),
    path('view_media/', views.view_media, name='view_media'),
]