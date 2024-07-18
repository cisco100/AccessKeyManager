from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.



class AccessKey(models.Model):
    KEY_STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=KEY_STATUS_CHOICES, default='active')
    procurement_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    class Meta:
        ordering = ['status', '-procurement_date']

    def __str__(self):
        return f"{self.user.email} - {self.key}"


