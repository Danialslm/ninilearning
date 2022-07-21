import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext as _

from apps.content.models import Content
from apps.users.models import User, Device


class UserTestCase(TestCase):
    def test_user_model_set_correctly(self):
        self.assertIs(
            get_user_model(),
            User,
        )

    def test_phone_number_validator(self):
        with self.assertRaises(ValidationError) as e:
            # start with `09`
            User.phone_number_validator('01234567899')
            # length
            User.phone_number_validator('0912345678')
            User.phone_number_validator('091234567891')

        self.assertEqual(
            _('The phone number is invalid. Note that use English numbers.'),
            e.exception.message,
        )

    def test_create_normal_user(self):
        user = User.objects.create_user(
            phone_number='09000000000',
            password='test',
            first_name='test',
            last_name='test',
        )

        self.assertEqual(user.phone_number, '09000000000')
        self.assertTrue(user.check_password('test'))
        self.assertTrue(user.first_name, 'test')
        self.assertTrue(user.last_name, 'test')

    def test_create_superuser_user(self):
        user = User.objects.create_superuser(
            phone_number='09000000000',
            password='test',
            first_name='test',
            last_name='test',
        )

        self.assertEqual(user.phone_number, '09000000000')
        self.assertTrue(user.check_password('test'))
        self.assertTrue(user.first_name, 'test')
        self.assertTrue(user.last_name, 'test')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_vip(self):
        vip_date = datetime.date.today() + datetime.timedelta(days=10)
        user = User.objects.create(vip_date=vip_date)

        self.assertTrue(user.is_vip)
        self.assertEqual(user.vip_left, datetime.timedelta(days=10))

    def test_is_bookmarked(self):
        user = User.objects.create()
        content = Content.objects.create()
        user.bookmarks.add(content)

        self.assertTrue(user.is_bookmarked(content))

        user.bookmarks.remove(content)

        self.assertFalse(user.is_bookmarked(content))


class DeviceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create()

    def test_object_creation(self):
        last_login = datetime.datetime.now()
        device = Device.objects.create(
            user=self.user,
            ip_address='127.0.0.1',
            device_name='test',
            session_key='test',
            last_login=last_login
        )

        self.assertIs(device.user, self.user)
        self.assertEqual(device.ip_address, '127.0.0.1')
        self.assertEqual(device.device_name, 'test')
        self.assertEqual(device.session_key, 'test')
        self.assertEqual(device.last_login, last_login)
