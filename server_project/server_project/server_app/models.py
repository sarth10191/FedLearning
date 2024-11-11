from django.db import models
from django.contrib.auth.models import User
from django.db import models

class ClientInfo(models.Model):
    username = models.CharField(max_length=20, default="client")
    ip_address = models.CharField(max_length=100)
    port = models.IntegerField()
    registered_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.username} ({self.ip_address}:{self.port})"


class ClientFile(models.Model):
    client = models.ForeignKey(ClientInfo, on_delete=models.CASCADE, related_name='files')
    # version_number = models.IntegerField()
    model_file = models.FileField(upload_to='modelfiles/')
    model_summary = models.FileField(upload_to='summaryfiles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Files for {self.client.username}"

