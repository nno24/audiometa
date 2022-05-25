from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, sessions
from django.conf import settings
from django.http import HttpResponse, Http404
import requests
import os
import magic
from .models import Audio
from .forms import AudioForm, AudioEditForm
from mutagen.id3 import ID3, TIT2, TALB, TOWN, TORY, TOPE
from mutagen.id3 import TBPM, TCON, TCOM, TCOP, TIPL


tags_dict = {
    'TIT2': 'Song Title',
    'TALB': 'Song Album',
    'TOWN': 'Song Owner',
    'TORY': 'Release Year',
    'TOPE': 'Artist',
    'TBPM': 'BPM/Beats per minute',
    'TSSE': 'Encoder Settings',
    'TCON': 'Genre',
    'TCOM': 'Composer',
    'TCOP': 'Copyright',
    'TIPL': 'Involved Persons'
}


def get_home(request):
    """ Main view of the application"""
    
# Delete the previous audio file if any in db
    try:
        audio = Audio.objects.get(id=request.session['user_id'])
        audio.delete()
        print("Deleted audio file from db")
        messages.warning(request, "Deleted audio file - upload a new one")
    except:
        print("No audio files in db")

# Render the audio file input form
    audioform = AudioForm()
    context = {
        'audioform': audioform,
    }

    return render(request, 'home/home.html', context)


def upload_media(request):
    """A view to handle file uploads"""
    print(request.session['user_id'])
    print("this is upload media", request.FILES)
    if request.POST:
        audioform = AudioForm(request.POST, request.FILES)
        if audioform.is_valid():
            audioform.save()
#Get the uploaded audio and grab the uuid
            audio = Audio.objects.last()
            request.session['user_id']=str(audio.uuid)
            messages.success(request, "Successfully uploaded..")
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
    print(request.session['user_id'])
    audio = Audio.objects.get(id=request.session['user_id'])
    tags = ID3(audio.media)
# Update if any existing fields from the audio track to model
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
            elif key == 'TCON':
                audio.TCON = value
            elif key == 'TCOM':
                audio.TCOM = value
            elif key == 'TCOP':
                audio.TCOP = value
            elif key == 'TIPL':
                audio.TIPL = value
            audio.save()

# Fetch the audio file again
    audio = Audio.objects.get(id=request.session['user_id'])
    audio_editform = AudioEditForm(instance=audio)

    context = {
        'audio_editform': audio_editform,
        'audio': audio,
    }
    return render(request, 'home/view_media.html', context)


def save_media(request):
    """A view to save media"""
    print(request.session['user_id'])
    if request.POST:
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('value: %s' % (value))

        audio = Audio.objects.get(id=request.session['user_id'])
        form = AudioEditForm(request.POST, instance=audio)
        if form.is_valid():
            print("Form saved and valid")
            form.save()
            messages.success(request, "Saved")
        else:
            print("Form not valid")
            messages.error(request, "Form not valid...not saved")
    context = {
        'form': form,
        'audio': audio,
    }

    return render(request, 'home/save_media.html', context)

def download(request):
    """ A view to append saved tags to audio file
    stored in db - and download file
    """

#1 Get the saved audio object from form input
    audio = Audio.objects.get(id=request.session['user_id'])
#2 Set the ID3 attributes / metadata to file
    audio_path = 'media/'+str(audio.media)
    tags = ID3(audio_path)
    if audio.TIT2:
        tags.add(TIT2(text=audio.TIT2))
    if audio.TALB:
        tags.add(TALB(text=audio.TALB))
    if audio.TOWN:
        tags.add(TOWN(text=audio.TOWN))
    if audio.TOPE:
        tags.add(TOPE(text=audio.TOPE))
    if audio.TBPM:
        tags.add(TBPM(text=audio.TBPM))
    if audio.TCON:
        tags.add(TCON(text=audio.TCON))
    if audio.TCOM:
        tags.add(TCOM(text=audio.TCOM))
    if audio.TCOP:
        tags.add(TCOP(text=audio.TCOP))
    if audio.TIPL:
        tags.add(TIPL(text=audio.TIPL))
    
    tags.save()
  
    context = {
        'tags': tags,
        'audio': audio,
    }

# Get mime type / or  media type
    mime = magic.Magic(mime=True)
    audio_mime = mime.from_file(audio_path)
    print("the mime type is: ", audio_mime)

# Start the download
    if os.path.exists(audio_path):
        with open(audio_path, 'rb') as ap:
            response = HttpResponse(ap.read(), content_type=audio_mime)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(audio_path)
            return response
    raise Http404
    messages.error(request, "Download failed")
    return render(request, 'home/download.html', context)
    