

from django.db import models
from django.utils import timezone

class TimeCapsule(models.Model):

    email = models.EmailField()

    cid = models.CharField(max_length=255)

    decryption_pass = models.CharField(max_length=255)

    storage_time = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=50, default='pending')

    unlock_time = models.IntegerField(default=0)  # in seconds

    file_ext = models.CharField(max_length=10, default='txt')

    file_mime = models.CharField(max_length=20, default='text/plain')
    class Meta:
        db_table = 'TimeCapsule'

