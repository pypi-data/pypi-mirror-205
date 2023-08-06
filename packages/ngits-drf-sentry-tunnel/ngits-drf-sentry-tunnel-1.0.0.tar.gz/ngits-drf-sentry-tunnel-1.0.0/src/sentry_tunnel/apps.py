from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class SentryTunnelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sentry_tunnel"

    def ready(self):
        if not hasattr(settings, "SENTRY_HOST"):
            raise ImproperlyConfigured("no SENTRY_HOST")
        if not hasattr(settings, "SENTRY_PROJECT_IDS"):
            raise ImproperlyConfigured("no SENTRY_PROJECT_IDS")

        return super().ready()
