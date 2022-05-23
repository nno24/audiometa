from django.shortcuts import render, redirect
from django.contrib import messages
import requests

# Create your views here.
def get_home(request):
    """ Main view of the application"""

    context = {

    }
    
    return render(request, 'home/home.html', context)