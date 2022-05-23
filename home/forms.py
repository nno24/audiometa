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
    