"""SAMLProvider API Views"""
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from passbook.providers.saml.models import SAMLPropertyMapping, SAMLProvider


class SAMLProviderSerializer(ModelSerializer):
    """SAMLProvider Serializer"""

    class Meta:

        model = SAMLProvider
        fields = [
            "pk",
            "name",
            "processor_path",
            "acs_url",
            "audience",
            "issuer",
            "assertion_valid_not_before",
            "assertion_valid_not_on_or_after",
            "session_valid_not_on_or_after",
            "property_mappings",
            "digest_algorithm",
            "signature_algorithm",
            "signing",
            "signing_cert",
            "signing_key",
        ]


class SAMLProviderViewSet(ModelViewSet):
    """SAMLProvider Viewset"""

    queryset = SAMLProvider.objects.all()
    serializer_class = SAMLProviderSerializer


class SAMLPropertyMappingSerializer(ModelSerializer):
    """SAMLPropertyMapping Serializer"""

    class Meta:

        model = SAMLPropertyMapping
        fields = ["pk", "name", "saml_name", "friendly_name", "expression"]


class SAMLPropertyMappingViewSet(ModelViewSet):
    """SAMLPropertyMapping Viewset"""

    queryset = SAMLPropertyMapping.objects.all()
    serializer_class = SAMLPropertyMappingSerializer
