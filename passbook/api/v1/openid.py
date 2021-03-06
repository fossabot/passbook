"""Passbook v1 OpenID API"""
from django.http import JsonResponse
from django.views import View
from oauth2_provider.views.mixins import ScopedResourceMixin


class OpenIDUserInfoView(ScopedResourceMixin, View):
    """Passbook v1 OpenID API"""

    required_scopes = ["openid:userinfo"]

    def get(self, request, *_, **__):
        """Passbook v1 OpenID API"""
        payload = {
            "sub": request.user.uuid.int,
            "name": request.user.get_full_name(),
            "given_name": request.user.name,
            "family_name": "",
            "preferred_username": request.user.username,
            "email": request.user.email,
        }
        return JsonResponse(payload)
