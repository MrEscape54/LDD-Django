from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    # To add the signal in the internal Django registry
    def ready(self):
        from . import signals
