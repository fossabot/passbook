"""passbook user view tests"""
import string
from random import SystemRandom

from django.shortcuts import reverse
from django.test import TestCase

from passbook.core.models import User


class TestOverviewViews(TestCase):
    """Test Overview Views"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="unittest user",
            email="unittest@example.com",
            password="".join(
                SystemRandom().choice(string.ascii_uppercase + string.digits)
                for _ in range(8)
            ),
        )
        self.client.force_login(self.user)

    def test_overview(self):
        """Test UserSettingsView"""
        self.assertEqual(
            self.client.get(reverse("passbook_core:overview")).status_code, 200
        )
