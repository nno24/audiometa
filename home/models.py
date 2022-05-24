from django.db import models

# Create your models here.
class Audio(models.Model):
    media = models.FileField(null=True, blank=False, upload_to='uploads/')
    TIT2 = models.CharField(null=True, blank=True, max_length=50) #TIT2 / Title
    TOPE = models.CharField(null=True, blank=True, max_length=50) #TOPE / Original Artist/performer
    TALB = models.CharField(null=True, blank=True, max_length=50) #TALB / Album
    TOWN = models.CharField(null=True, blank=True, max_length=50) #TOWN / Owner/Licencee
    TORY = models.CharField(null=True, blank=True, max_length=50) #TORY / Original Release year
    TBPM = models.CharField(null=True, blank=True, max_length=50) #TBPM / Beats per minute
    TSSE = models.CharField(null=True, blank=True, max_length=50) #TSSE / Encoder Settings
    TCON = models.CharField(null=True, blank=True, max_length=50) #TCON / Genre
    TCOM = models.CharField(null=True, blank=True, max_length=50) #TSSE / Composer
    TCOP = models.CharField(null=True, blank=True, max_length=50) #TCOP / Copyright
    TIPL = models.CharField(null=True, blank=True, max_length=50) #TIPL / Involved persons

    def delete(self, using=None, keep_parents=False):
        self.media.storage.delete(self.media.name)
        super().delete()


