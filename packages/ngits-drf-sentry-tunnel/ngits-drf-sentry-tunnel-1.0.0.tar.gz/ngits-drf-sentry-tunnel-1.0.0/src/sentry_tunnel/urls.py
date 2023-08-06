from django.urls import path

from .views import SentryTunnelView

urlpatterns = [
    path(
        "tunnel/",
        SentryTunnelView,
        name="tunnel",
    ),
]
