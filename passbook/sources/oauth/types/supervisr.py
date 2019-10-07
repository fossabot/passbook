"""Supervisr OAuth2 Views"""

import json

from requests.exceptions import RequestException
from structlog import get_logger

from passbook.sources.oauth.clients import OAuth2Client
from passbook.sources.oauth.types.manager import MANAGER, RequestKind
from passbook.sources.oauth.utils import user_get_or_create
from passbook.sources.oauth.views.core import OAuthCallback

LOGGER = get_logger()


class SupervisrOAuth2Client(OAuth2Client):
    """Supervisr OAuth2 Client"""

    def get_profile_info(self, raw_token):
        "Fetch user profile information."
        try:
            token = json.loads(raw_token)['access_token']
            headers = {
                'Authorization': 'Bearer:%s' % token
            }
            response = self.request('get', self.source.profile_url,
                                    token=raw_token, headers=headers)
            response.raise_for_status()
        except RequestException as exc:
            LOGGER.warning('Unable to fetch user profile: %s', exc)
            return None
        else:
            return response.json() or response.text


@MANAGER.source(kind=RequestKind.callback, name='supervisr')
class SupervisrOAuthCallback(OAuthCallback):
    """Supervisr OAuth2 Callback"""

    client_class = SupervisrOAuth2Client

    def get_user_id(self, source, info):
        return info['pk']

    def get_or_create_user(self, source, access, info):
        user_data = {
            'username': info.get('username'),
            'email': info.get('email', ''),
            'name': info.get('first_name'),
            'password': None,
        }
        sv_user = user_get_or_create(**user_data)
        return sv_user