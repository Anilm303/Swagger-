from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        # Import schema extensions so drf-spectacular can discover custom auth.
        from . import schema  # noqa: F401
