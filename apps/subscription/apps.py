from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subscription'
    verbose_name = _('subscription')
