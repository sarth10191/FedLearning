from django.apps import AppConfig
from .signals import load_to_csv, data_loaded
from .views import registerToServer
from . import utils
from .signals import *
class ClientappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientapp'

    def ready(self):
        print("app started")
        #connect intermodular signal. i.e., signal sent from one module to another module.
        try:
            load_to_csv.send(sender=self.__class__)
            #other signal which works perfectly. Even when intermodular This is connected in utils.py file.
            print("signal sent from apps.py")
        except Exception as e:
            print("Cant send signal from apps.py", e)


