from django.contrib.auth import authenticate
from django.test import TestCase
from django.utils.translation import gettext as _
from apps.users.forms import LoginForm
from apps.users.models import User


class LoginFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09000000000',
            password='test',
        )

    def test_valid_credentials(self):
        form = LoginForm(data={
            'username': '09000000000',
            'password': 'test',
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_valid_format_invalid_credentials(self):
        form = LoginForm(data={
            'username': '09100000000',
            'password': 'test',
        })

        self.assertFalse(form.is_valid())
        self.assertIn(
            _(
                'Any user with this %(username)s and password not found. Note that password '
                'may be case-sensitive.'
            ) % {'username': _('phone number')},
            form.non_field_errors(),
        )

    def test_invalid_format(self):
        form = LoginForm(data={
            'username': '00000000000',
            'password': 'test',
        })

        self.assertFalse(form.is_valid())
        self.assertIn(
            _('The phone number is invalid. Note that use English numbers.'),
            form.errors['username'],
        )
