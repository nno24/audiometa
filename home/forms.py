from django import forms
from .models import Audio


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ['media']


class AudioEditForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = '__all__'
        exclude = ['media']
        labels = {
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
            'TIPL': 'Involved Persons',
        }
