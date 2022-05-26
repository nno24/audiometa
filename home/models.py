from django.db import models


# Create your models here.
class Audio(models.Model):
    media = models.FileField(null=True, blank=False, upload_to='uploads/')
    TIT2 = models.CharField(null=True, blank=True, max_length=50)  # Title
    TOPE = models.CharField(null=True, blank=True, max_length=50)  # Artist
    TALB = models.CharField(null=True, blank=True, max_length=250)  # Album
    TOWN = models.CharField(null=True, blank=True, max_length=50)  # Owner
    TORY = models.CharField(null=True, blank=True, max_length=50)  # Release Year.
    TBPM = models.CharField(null=True, blank=True, max_length=50)  # Beats pr min.
    TSSE = models.CharField(null=True, blank=True, max_length=50)  # Encoder Sett.
    TCON = models.CharField(null=True, blank=True, max_length=50)  # Genre
    TCOM = models.CharField(null=True, blank=True, max_length=50)  # Composer
    TCOP = models.CharField(null=True, blank=True, max_length=50)  # Copyright
    TIPL = models.CharField(null=True, blank=True, max_length=250)  # Involved pers.

    def delete(self, using=None, keep_parents=False):
        self.media.storage.delete(self.media.name)
        super().delete()
