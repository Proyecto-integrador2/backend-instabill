from django.apps import AppConfig


class AppinstabillConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "appinstabill"

    def ready(self):
        import appinstabill.signals  # Import signals to connect them
