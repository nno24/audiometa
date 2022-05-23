from django.db import models

# Create your models here.
class Audio(models.Model):
    org_file_name = models.CharField(max_length=50, null=True, blank=True)
    media = models.FileField(null=True, blank=False, upload_to='uploads/' )


