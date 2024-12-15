from django.apps import AppConfig


class ClientIntrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_intr'

    def ready(self):
        from . import signals
