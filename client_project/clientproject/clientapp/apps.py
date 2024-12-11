from django.apps import AppConfig
from .signals import load_to_csv
from . import utils
class ClientappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientapp'

    def ready(self):
        print("app started")
        try:
            load_to_csv.send(sender=self.__class__)
            print("signal sent")
        except Exception as e:
            print("Cant send signal from apps.py")