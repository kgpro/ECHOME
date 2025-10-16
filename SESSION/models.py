from django.db import models
from django.utils import timezone

class sessions(models.Model):

    email = models.EmailField()

    login_password = models.CharField(max_length=255)

    session_id = models.CharField(max_length=255)

    session_expiry = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=50, default='expired')

    mobile_number = models.IntegerField(max_length=10, default=0)

    country_code = models.CharField(max_length=2, default=91)


    class Meta:
        db_table = 'sessions'