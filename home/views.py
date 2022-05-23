from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from .models import Audio
from .forms import AudioForm

# Create your views here.
def get_home(request):
    """ Main view of the application"""
    audioform = AudioForm()
    context = {
        'audioform': audioform,
    }

    return render(request, 'home/home.html', context)


def upload_media(request):
    """A view to handle file uploads"""
    print("this is upload media", request.FILES)
    if request.POST:
        audioform = AudioForm(request.POST, request.FILES)
        if audioform.is_valid():        
            audioform.save()
            messages.success(request, "Successfully uploaded to server..")
            return redirect('home')
        else:
            messages.error(request, "Failed to upload")
    else:
        audioform = AudioForm()
    
    context = {
        'audioform': audioform,
    }

    return render(request, 'home/home.html', context)