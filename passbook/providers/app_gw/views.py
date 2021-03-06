"""passbook app_gw views"""
import string
from random import SystemRandom

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from structlog import get_logger

from passbook import __version__
from passbook.providers.app_gw.models import ApplicationGatewayProvider

ORIGINAL_URL = "HTTP_X_ORIGINAL_URL"
LOGGER = get_logger()


def get_cookie_secret():
    """Generate random 50-character string for cookie-secret"""
    return "".join(
        SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50)
    )


class K8sManifestView(LoginRequiredMixin, View):
    """Generate K8s Deployment and SVC for gatekeeper"""

    def get(self, request: HttpRequest, provider: int) -> HttpResponse:
        """Render deployment template"""
        provider = get_object_or_404(ApplicationGatewayProvider, pk=provider)
        return render(
            request,
            "app_gw/k8s-manifest.yaml",
            {
                "provider": provider,
                "cookie_secret": get_cookie_secret(),
                "version": __version__,
            },
            content_type="text/yaml",
        )
