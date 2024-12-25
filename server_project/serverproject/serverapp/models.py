from django.db import models

import os
from django.utils.timezone import now
# Create your models here.
class ClientInfo(models.Model):



    def upload_to(instance, filename):
        base, ext = os.path.splitext(filename)
        timestamp = now().strftime('%Y%m%d%H%M%S')
        return f'uploads/{base}_{timestamp}{ext}'
    class StatusChoices(models.TextChoices):
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"
        DEREGISTERED = "Deregistered", "Deregistered"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(protocol='both')
    port = models.PositiveIntegerField()
    status = models.CharField(max_length=20,choices=StatusChoices.choices, default=StatusChoices.ACTIVE )
    model_version = models.CharField(max_length=10,default=1.0)
    model_file = models.CharField(max_length=300, default="")
    # data_size = models.PositiveBigIntegerField()
    # capabilities = models.JSONField()
    # trusted = models.BooleanField(default=True)
    # last_active = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f"{self.name}, {self.ip}:{self.port}"