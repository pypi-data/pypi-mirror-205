ngits-drf-sentry-tunnel
=======================

Olá!

Setup
-----

1. Install using pip:
~~~~~~~~~~~~~~~~~~~~~

::

    pip install ngits-drf-sentry-tunnel

2. Change your ``settings`` file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    import os

    ...

    INSTALLED_APPS = [
        ...
        "rest_framework",
        "sentry_tunnel"
    ]

    ...

    SENTRY_HOST = "sentry.local"
    SENTRY_PROJECT_IDS = ["4"]

3. Add paths to your ``urls.py`` file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from django.urls import path, include

    urlpatterns = [
        ...
        path("", include("sentry_tunnel.urls"))
    ]

Above example results: ``http://127.0.0.1:8000/tunnel/`` API endpoint URL

