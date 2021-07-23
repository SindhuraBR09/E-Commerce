from django.apps import AppConfig


class UrbanityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Urbanity'

    def ready(self):
        import Urbanity.signals
