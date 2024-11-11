from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import connection


class ServerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server_app'

    def ready(self):
        # Clear all models on server restart
        
        from django.db.models import F
        from .models import ClientInfo, ClientFile
        # Optionally, you can clear specific models like ClientInfo and ClientFiles
        # Example: Remove all records from ClientInfo and ClientFiles
        ClientInfo.objects.all().delete()
        ClientFile.objects.all().delete()

        # You can use Django signals to clear the database after migrations as well
        post_migrate.connect(clear_data_on_migrate, sender=self)

def clear_data_on_migrate(sender, **kwargs):
    """Clear all models after migration"""
    from .models import ClientInfo, ClientFile
    ClientInfo.objects.all().delete()
    ClientFile.objects.all().delete()