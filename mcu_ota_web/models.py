from django.db import models

# Create your models here.
from django.utils import timezone
from django.conf import settings

class UserDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = password = models.CharField(max_length=64, null=True)
    email = models.EmailField(null=True, blank=True)  # Add email field
    password = models.CharField(max_length=64)
    device_key = models.CharField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=17)

    def __str__(self):
        return f"{self.user.username} - {self.device_key}"
    

class Firmware(models.Model):
    user_device = models.ForeignKey(UserDevice, on_delete=models.CASCADE)
    version = models.CharField(max_length=10)
    file = models.FileField(upload_to="")
    release_date = models.DateTimeField(default=timezone.now)  # Timestamp field

    def __str__(self):
        return f"Firmware {self.version} by {self.user_device.username}"