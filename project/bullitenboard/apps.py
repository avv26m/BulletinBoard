from django.apps import AppConfig


class BullitenboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bullitenboard'

    def ready(self):
        from . import signals