import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = None

    phone_number_validator = RegexValidator(
        regex=r'^[0][9][0-9]{9}$',
        message=_('The phone number is invalid. Note that use English numbers.'),
    )

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    phone_number = models.CharField(
        _('phone number'),
        max_length=11,
        unique=True,
        validators=[phone_number_validator],
    )
    vip_date = models.DateField(_('vip date'), blank=True, null=True)
    bookmarks = models.ManyToManyField(
        'content.Content',
        verbose_name=_('bookmarks'),
        related_name='users_bookmark',
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    @property
    def is_vip(self):
        if self.vip_date:
            return self.vip_date > datetime.date.today()
        return False

    @property
    def vip_left(self):
        return self.vip_date - datetime.date.today()

    def is_bookmarked(self, content):
        return self.bookmarks.filter(pk=content.pk).exists()


class Device(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='logged_in_devices',
    )
    ip_address = models.GenericIPAddressField(_('ip address'))
    device_name = models.CharField(_('device'), max_length=150)
    session_key = models.CharField(max_length=33, editable=False)
    last_login = models.DateTimeField(_('last login'), default=timezone.now)

    def __str__(self):
        return f'{self.user} - {self.device_name}'

    class Meta:
        verbose_name = _('device')
        verbose_name_plural = _('devices')
