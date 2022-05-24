from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, Http404
import requests, os, magic
from .models import Audio
from .forms import AudioForm, AudioEditForm
from mutagen.id3 import ID3, TIT2, TALB, TOWN, TORY, TOPE, TBPM


tags_dict = {
    'TIT2': 'Song Title',
    'TALB': 'Song Album',
    'TOWN': 'Song Owner',
    'TORY': 'Release Year',
    'TOPE': 'Artist',
    'TBPM': 'BPM/Beats per minute',
    'TSSE': 'Encoder Settings',
}

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
            return redirect('view_media')
        else:
            messages.error(request, "Failed to upload")
    else:
        audioform = AudioForm()
    
    context = {
        'audioform': audioform,
    }

    return render(request, 'home/home.html', context)


def view_media(request):
    """ A view to render the media file"""
    audio = Audio.objects.last()
    tags = ID3(audio.media)
    #Update if any existing fields from the audio track to model
    for key, value in tags.items():
        print(key, value)
        if key in tags_dict.keys():
            print('The key exists: ', key)
            if key == 'TIT2':
                audio.TSSE = value
            elif key == 'TALB':
                audio.TALB = value
            elif key == 'TOWN':
                audio.TOWN = value
            elif key == 'TORY':
                audio.TORY = value
            elif key == 'TBPM':
                audio.TBPM = value
            elif key == 'TSSE':
                audio.TSSE = value
            
            audio.save()

    #Fetch the audio file again
    audio = Audio.objects.last()
    audio_editform = AudioEditForm(instance=audio)

    context = {
        'audio_editform': audio_editform,
        'audio': audio,
    }
    return render(request, 'home/view_media.html', context)


def save_media(request):
    """A view to save media"""

    if request.POST:
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('value: %s' % (value))

        audio = Audio.objects.last()
        form = AudioEditForm(request.POST, instance=audio)
        if form.is_valid():
            print("Form saved and valid")
            form.save()
        else:
            print("Form not valid")

        
    context = {
        'form': form,
        'audio': audio,
    }

    return render(request, 'home/save_media.html', context)

def download(request):
    """ A view to append saved tags to audio file stored in db - and download file """

    #1 Get the saved audio object from form input
    audio = Audio.objects.last()
    #2 Set the ID3 attributes / metadata to file
    audio_path = 'media/'+str(audio.media)
    tags = ID3(audio_path)
    tags.add(TIT2(text=audio.TIT2))
    tags.add(TALB(text=audio.TALB))
    tags.add(TOWN(text=audio.TOWN))
    tags.add(TOPE(text=audio.TOPE))
    tags.add(TBPM(text=audio.TBPM))
    tags.save()
    
    context = {
        'tags': tags,
        'audio': audio,
    }

    #Get mime type / or  media type
    mime = magic.Magic(mime=True)
    audio_mime = mime.from_file(audio_path)
    print("the mime type is: ", audio_mime)

    #Start the download
    if os.path.exists(audio_path):
        with open(audio_path, 'rb') as ap:
            response = HttpResponse(ap.read(), content_type=audio_mime)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(audio_path)
            return response
        raise Http404

    return render(request, 'home/download.html', context)