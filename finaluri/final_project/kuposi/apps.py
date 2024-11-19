from django.apps import AppConfig


class KuposiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kuposi'

    def ready(self):
        import kuposi.signals

