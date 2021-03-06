"""recovery tests"""
from io import StringIO

from django.core.management import call_command
from django.shortcuts import reverse
from django.test import TestCase

from passbook.core.models import Nonce, User


class TestRecovery(TestCase):
    """recovery tests"""

    def setUp(self):
        self.user = User.objects.create_user(username="recovery-test-user")

    def test_create_key(self):
        """Test creation of a new key"""
        out = StringIO()
        self.assertEqual(len(Nonce.objects.all()), 0)
        call_command("create_recovery_key", "1", self.user.username, stdout=out)
        self.assertIn("https://localhost/recovery/use-nonce/", out.getvalue())
        self.assertEqual(len(Nonce.objects.all()), 1)

    def test_recovery_view(self):
        """Test recovery view"""
        out = StringIO()
        call_command("create_recovery_key", "1", self.user.username, stdout=out)
        nonce = Nonce.objects.first()
        self.client.get(
            reverse("passbook_recovery:use-nonce", kwargs={"uuid": str(nonce.uuid)})
        )
        self.assertEqual(int(self.client.session["_auth_user_id"]), nonce.user.pk)
