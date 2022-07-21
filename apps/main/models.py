from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from apps.content.models import Content


class Slide(models.Model):
    title = models.CharField(_('slide title'), max_length=40)
    referral_link = models.URLField(_('referral link'))
    referral_link_text = models.CharField(_('referral link text'), max_length=30)
    desktop_image = models.ImageField(_('slide image (desktop)'), upload_to='slider')
    mobile_image = models.ImageField(_('slide image (mobile)'), upload_to='slider')
    intro_image = models.ImageField(_('slide image (intro)'), upload_to='slider', null=True, blank=True)

    class Meta:
        verbose_name = _('slide')
        verbose_name_plural = _('slides')

    def __str__(self):
        return self.title


class Collection(models.Model):
    title = models.CharField(_('title'), max_length=30, unique=True)
    slug = models.SlugField(_('slug'), unique=True)
    contents = models.ManyToManyField('content.Content', verbose_name=_('contents'), related_name='collections')

    class Meta:
        verbose_name = _('collection')
        verbose_name_plural = _('collections')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:collection', kwargs={'slug': self.slug})
