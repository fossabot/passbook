"""passbook app_gw middleware"""
import mimetypes
from logging import getLogger
from urllib.parse import urlparse

import certifi
import urllib3
from django.core.cache import cache
from django.utils.http import urlencode
from revproxy.exceptions import InvalidUpstream
from revproxy.response import get_django_response
from revproxy.utils import encode_items, normalize_request_headers

from passbook.app_gw.models import ApplicationGatewayProvider
from passbook.app_gw.rewrite import Rewriter
from passbook.core.models import Application
from passbook.core.policies import PolicyEngine

IGNORED_HOSTNAMES_KEY = 'passbook_app_gw_ignored'
LOGGER = getLogger(__name__)
QUOTE_SAFE = r'<.;>\(}*+|~=-$/_:^@)[{]&\'!,"`'
ERRORS_MESSAGES = {
    'upstream-no-scheme': ("Upstream URL scheme must be either "
                           "'http' or 'https' (%s).")
}

# pylint: disable=too-many-instance-attributes
class ApplicationGatewayMiddleware:
    """Check if request should be proxied or handeled normally"""

    ignored_hosts = []
    request = None
    app_gw = None
    http = None
    http_no_verify = None
    host_header = ''

    _parsed_url = None
    _request_headers = None

    def __init__(self, get_response):
        self.get_response = get_response
        self.ignored_hosts = cache.get(IGNORED_HOSTNAMES_KEY, [])
        self.http_no_verify = urllib3.PoolManager()
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

    def precheck(self, request):
        """Check if a request should be proxied or forwarded to passbook"""
        # Check if hostname is in cached list of ignored hostnames
        # This saves us having to query the database on each request
        self.host_header = request.META.get('HTTP_HOST')
        if self.host_header in self.ignored_hosts:
            LOGGER.debug("%s is ignored", self.host_header)
            return True, None
        # Look through all ApplicationGatewayProviders and check hostnames
        matches = ApplicationGatewayProvider.objects.filter(
            server_name__contains=[self.host_header],
            enabled=True)
        if not matches.exists():
            # Mo matching Providers found, add host header to ignored list
            self.ignored_hosts.append(self.host_header)
            cache.set(IGNORED_HOSTNAMES_KEY, self.ignored_hosts)
            LOGGER.debug("Ignoring %s", self.host_header)
            return True, None
        # At this point we're certain there's a matching ApplicationGateway
        if len(matches) > 1:
            # TODO This should never happen
            raise ValueError
        app_gw = matches.first()
        try:
            # Check if ApplicationGateway is associcaited with application
            getattr(app_gw, 'application')
            return False, app_gw
        except Application.DoesNotExist:
            LOGGER.debug("ApplicationGateway not associated with Application")
            return True, None
        return True, None

    def __call__(self, request):
        forward, self.app_gw = self.precheck(request)
        if forward:
            return self.get_response(request)
        self.request = request
        return self.dispatch(request)

    def get_upstream(self):
        """Get upstream as parsed url"""
        # TODO: How to choose upstream?
        upstream = self.app_gw.upstream[0]

        if not getattr(self, '_parsed_url', None):
            self._parsed_url = urlparse(upstream)

        if self._parsed_url.scheme not in ('http', 'https'):
            raise InvalidUpstream(ERRORS_MESSAGES['upstream-no-scheme'] %
                                  upstream)

        return upstream

    def _format_path_to_redirect(self, request):
        LOGGER.debug("Path before: %s", request.get_full_path())
        rewriter = Rewriter(self.app_gw, request)
        after = rewriter.build()
        LOGGER.debug("Path after: %s", after)
        return after

    def get_proxy_request_headers(self, request):
        """Get normalized headers for the upstream
        Gets all headers from the original request and normalizes them.
        Normalization occurs by removing the prefix ``HTTP_`` and
        replacing and ``_`` by ``-``. Example: ``HTTP_ACCEPT_ENCODING``
        becames ``Accept-Encoding``.
        .. versionadded:: 0.9.1
        :param request:  The original HTTPRequest instance
        :returns:  Normalized headers for the upstream
        """
        return normalize_request_headers(request)

    def get_request_headers(self):
        """Return request headers that will be sent to upstream.
        The header REMOTE_USER is set to the current user
        if AuthenticationMiddleware is enabled and
        the view's add_remote_user property is True.
        .. versionadded:: 0.9.8
        """
        request_headers = self.get_proxy_request_headers(self.request)
        request_headers[self.app_gw.authentication_header] = self.request.user.get_username()
        LOGGER.info("%s set", self.app_gw.authentication_header)

        return request_headers

    def check_permission(self):
        """Check if user is authenticated and has permission to access app"""
        if not hasattr(self.request, 'user'):
            return False
        if not self.request.user.is_authenticated:
            return False
        policy_engine = PolicyEngine(self.app_gw.application.policies.all())
        policy_engine.for_user(self.request.user).with_request(self.request).build()
        passing, _messages = policy_engine.result

        return passing

    def get_encoded_query_params(self):
        """Return encoded query params to be used in proxied request"""
        get_data = encode_items(self.request.GET.lists())
        return urlencode(get_data)

    def _created_proxy_response(self, request, path):
        request_payload = request.body

        LOGGER.debug("Request headers: %s", self._request_headers)

        request_url = self.get_upstream() + path
        LOGGER.debug("Request URL: %s", request_url)

        if request.GET:
            request_url += '?' + self.get_encoded_query_params()
            LOGGER.debug("Request URL: %s", request_url)

        http = self.http
        if not self.app_gw.upstream_ssl_verification:
            http = self.http_no_verify

        try:
            proxy_response = http.urlopen(request.method,
                                          request_url,
                                          redirect=False,
                                          retries=None,
                                          headers=self._request_headers,
                                          body=request_payload,
                                          decode_content=False,
                                          preload_content=False)
            LOGGER.debug("Proxy response header: %s",
                         proxy_response.getheaders())
        except urllib3.exceptions.HTTPError as error:
            LOGGER.exception(error)
            raise

        return proxy_response

    def _replace_host_on_redirect_location(self, request, proxy_response):
        location = proxy_response.headers.get('Location')
        if location:
            if request.is_secure():
                scheme = 'https://'
            else:
                scheme = 'http://'
            request_host = scheme + self.host_header

            upstream_host_http = 'http://' + self._parsed_url.netloc
            upstream_host_https = 'https://' + self._parsed_url.netloc

            location = location.replace(upstream_host_http, request_host)
            location = location.replace(upstream_host_https, request_host)
            proxy_response.headers['Location'] = location
            LOGGER.debug("Proxy response LOCATION: %s",
                         proxy_response.headers['Location'])

    def _set_content_type(self, request, proxy_response):
        content_type = proxy_response.headers.get('Content-Type')
        if not content_type:
            content_type = (mimetypes.guess_type(request.path)[0] or
                            self.app_gw.default_content_type)
            proxy_response.headers['Content-Type'] = content_type
            LOGGER.debug("Proxy response CONTENT-TYPE: %s",
                         proxy_response.headers['Content-Type'])

    def dispatch(self, request):
        """Build proxied request and pass to upstream"""
        # if not self.check_permission():
        #     to_url = 'https://%s/?next=%s' % (CONFIG.get('domains')[0], request.get_full_path())
        #     return RedirectView.as_view(url=to_url)(request)

        self._request_headers = self.get_request_headers()

        path = self._format_path_to_redirect(request)
        proxy_response = self._created_proxy_response(request, path)

        self._replace_host_on_redirect_location(request, proxy_response)
        self._set_content_type(request, proxy_response)
        response = get_django_response(proxy_response, strict_cookies=False)

        LOGGER.debug("RESPONSE RETURNED: %s", response)
        return response