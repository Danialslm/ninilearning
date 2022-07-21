from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.content.managers import ContentManager, SerialManager, MovieManager
from apps.votes.models import VoteMixin


def poster_upload_path(instance, filename):
    if isinstance(instance, Serial):
        return f'series/{instance.en_name}/posters/{filename}'
    elif isinstance(instance, Episode):
        file_ext = filename.split('.')[-1]
        return f'series/{instance.serial.en_name}/episodes/poster.{file_ext}'
    elif isinstance(instance, Movie):
        return f'movies/{instance.en_name}/posters/{filename}'


def video_upload_path(instance, filename):
    if isinstance(instance, Episode):
        return 'series/{}/episodes/{}/{}'.format(
            instance.serial.en_name,
            instance.episode_number,
            filename,
        )
    elif isinstance(instance, Movie):
        return 'movies/{}/{}'.format(
            instance.en_name,
            filename,
        )


def subtitle_upload_path(instance, filename):
    if isinstance(instance, Episode):
        return 'series/{}/episodes/{}/subtitles/{}'.format(
            instance.serial.en_name,
            instance.episode_number,
            filename,
        )
    elif isinstance(instance, Movie):
        return 'movies/{}/subtitles/{}'.format(
            instance.en_name,
            filename,
        )


def video_format_validator(file):
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in settings.ALLOWED_VIDEO_FORMAT:
        raise ValidationError(
            _('Video format is invalid. the valid video formats are ') + '، '.join(
                settings.ALLOWED_VIDEO_FORMATS))


class Genre(models.Model):
    genre = models.CharField(_('genre'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return reverse('main:genre', kwargs={'genre': self.genre})


class Content(VoteMixin):
    class ContentTypeChoices(models.TextChoices):
        SERIAL = 'S', _('serial')
        MOVIE = 'M', _('movie')

    pe_name = models.CharField(_('persian name'), max_length=120, unique=True)
    en_name = models.CharField(_('english name'), max_length=120, unique=True)
    slug = models.SlugField(_('slug'))
    age_range = models.CharField(_('age range'), max_length=50)
    country = models.CharField(
        _('country'),
        max_length=20,
        help_text=_('Product of which country?'),
    )
    description = models.TextField(_('description'))
    small_poster = models.ImageField(_('small poster'), upload_to=poster_upload_path)
    large_poster = models.ImageField(_('large poster'), upload_to=poster_upload_path)
    duration = models.CharField(_('duration'), max_length=20)
    resolution = models.CharField(_('resolution'), max_length=20)
    suggestions = models.ManyToManyField('self', verbose_name=_('suggestions'), blank=True)
    genres = models.ManyToManyField(Genre, verbose_name=_('genre'), related_name='contents')
    content_type = models.CharField(
        _('content type'),
        choices=ContentTypeChoices.choices,
        max_length=1,
        db_index=True,
    )

    video = models.FileField(
        _('video'),
        upload_to=video_upload_path,
        validators=[video_format_validator],
        null=True
    )
    pe_subtitle = models.FileField(
        _('persian subtitle'),
        upload_to=subtitle_upload_path,
        blank=True,
        null=True,
    )
    en_subtitle = models.FileField(
        _('english subtitle'),
        upload_to=subtitle_upload_path,
        blank=True,
        null=True
    )
    is_vip = models.BooleanField(
        _('vip'),
        default=False,
    )
    created_at = models.DateTimeField(_('created date'), default=timezone.now, editable=False)

    objects = ContentManager()

    def __str__(self):
        return self.pe_name

    def get_absolute_url(self):
        if self.content_type == self.ContentTypeChoices.SERIAL:
            return reverse('content:serial_detail', kwargs={'slug': self.slug})
        elif self.content_type == self.ContentTypeChoices.MOVIE:
            return reverse('content:movie_detail', kwargs={'slug': self.slug})


class Serial(Content):
    class Meta:
        proxy = True
        verbose_name = _('serial')
        verbose_name_plural = _('series')

    objects = SerialManager()


class Season(models.Model):
    season_number = models.PositiveSmallIntegerField(verbose_name=_('season'))
    serial = models.ForeignKey(Serial, verbose_name=_('serial'), on_delete=models.CASCADE, related_name='seasons')

    class Meta:
        verbose_name = _('season')
        verbose_name_plural = _('seasons')
        unique_together = ('season_number', 'serial')

    def __str__(self):
        return '{} {} {}'.format(self.serial.pe_name, self._meta.verbose_name, self.season_number)


class Episode(VoteMixin):
    title = models.CharField(_('title'), max_length=50)
    poster = models.ImageField(_('poster'), upload_to=video_upload_path)
    video = models.FileField(_('video'), upload_to=video_upload_path, validators=[video_format_validator])
    pe_subtitle = models.FileField(_('persian subtitle'), upload_to=subtitle_upload_path, blank=True, null=True)
    en_subtitle = models.FileField(_('english subtitle'), upload_to=subtitle_upload_path, blank=True, null=True)
    episode_number = models.PositiveSmallIntegerField(default=1, verbose_name=_('episode number'))
    is_vip = models.BooleanField(_('vip'))
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, related_name='episodes')

    class Meta:
        verbose_name = _('episode')
        verbose_name_plural = _('episodes')
        ordering = ['episode_number']
        unique_together = ('season', 'episode_number')

    def __str__(self):
        return '{} {} {} {} {}'.format(
            self.serial.pe_name,
            self.season._meta.verbose_name,
            self.season.season_number,
            self._meta.verbose_name,
            self.episode_number,
        )

    @property
    def serial(self):
        return self.season.serial


class Movie(Content):
    class Meta:
        proxy = True
        verbose_name = _('movie')
        verbose_name_plural = _('movies')

    objects = MovieManager()
