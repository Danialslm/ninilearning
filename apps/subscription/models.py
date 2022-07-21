from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class Plan(models.Model):
    plan_time = models.PositiveSmallIntegerField(_('plan time'), help_text=_('Plan time (month)'))
    price = models.DecimalField(
        _('price'),
        max_digits=6,
        decimal_places=0,
        help_text=_('Enter price in toman.'),
    )
    discounted_price = models.DecimalField(
        _('discounted price'),
        max_digits=6,
        decimal_places=0,
        blank=True,
        null=True,
        help_text=_('Enter discounted price in toman.')
    )

    class Meta:
        verbose_name = _('plan')
        verbose_name_plural = _('plans')

    def __str__(self):
        return f'{self.plan_time} months {self.discounted_price or self.price}'


def discount_code_generator():
    return get_random_string(5)


class DiscountCode(models.Model):
    code = models.CharField(_('code'), max_length=5, unique=True, default=discount_code_generator())

    class Meta:
        verbose_name = _('discount code')
        verbose_name_plural = _('discount codes')

    def __str__(self):
        return self.code
