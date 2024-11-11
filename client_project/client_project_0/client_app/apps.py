from django.apps import AppConfig


class ClientAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_app'

    def ready(self):
        from .views import register_with_server
        register_with_server()
