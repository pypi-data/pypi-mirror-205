import json
import urllib

import requests
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import BaseParser
from rest_framework.response import Response


class SentryParser(BaseParser):
    media_type = "text/plain"

    def parse(self, stream, media_type=None, parser_context=None):
        envelope = stream.read()
        piece = envelope.split(b"\n")[0].decode("utf-8")
        header = json.loads(piece)
        dsn_str = header.get("dsn", None)

        if not dsn_str:
            raise Exception("No dsn specified in header")

        dsn = urllib.parse.urlparse(dsn_str)
        return envelope, dsn


@api_view(["POST"])
@parser_classes([SentryParser])
def SentryTunnelView(request):
    SENTRY_HOST = settings.SENTRY_HOST
    SENTRY_PROJECT_IDS = settings.SENTRY_PROJECT_IDS

    envelope, dsn = request.data

    if dsn.hostname != SENTRY_HOST:
        raise Exception(f"Invalid Sentry host: {SENTRY_HOST}")

    project_id = dsn.path.strip("/")
    if project_id not in SENTRY_PROJECT_IDS:
        raise Exception(f"Invalid Project ID: {project_id}")

    url = f"https://{SENTRY_HOST}/api/{project_id}/envelope/"
    requests.post(
        url=url,
        data=envelope,
        headers={"Content-Type": "application/x-sentry-envelope"},
    )

    return Response()
