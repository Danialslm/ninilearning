from django.contrib import admin
from django.db.models import Prefetch
from django.urls import reverse, resolve
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class EpisodeInline(admin.TabularInline):
    model = models.Episode
    extra = 1

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('season', 'season__serial')


class SeasonInline(admin.StackedInline):
    model = models.Season
    extra = 1
    show_change_link = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('serial').only('serial__id', 'season_number')


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('season_number', 'display_serial')
    exclude = ('serial',)
    search_fields = ('serial__pe_name', 'serial__en_name')
    inlines = [EpisodeInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('serial').only('serial__id', 'serial__pe_name', 'season_number')

    @admin.display(description=_('serial'))
    def display_serial(self, obj):
        url = reverse(
            'admin:{}_{}_change'.format(obj.serial._meta.app_label, obj.serial._meta.model_name),
            args=[obj.serial.id]
        )
        return format_html(
            f'<a href={url}>{obj.serial.pe_name}</a>'
        )

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class BaseModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('pe_name', 'en_name', 'slug')}),
        (_('Posters'), {'fields': ('small_poster', 'large_poster')}),
        (_('Further information'), {'fields': (
            'age_range', 'country', 'description',
            'duration', 'resolution', 'genres', 'suggestions',
        )}),
    )
    prepopulated_fields = {'slug': ('en_name',)}
    list_display = (
        'display_poster', 'pe_name', 'display_genres',
        'resolution', 'likes_count', 'dislikes_count',
    )
    search_fields = ('description', 'pe_name', 'en_name', 'country')
    list_filter = ('created_at',)
    filter_horizontal = ('suggestions',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('genres')

        # prefetch the suggestions and genres only in change view
        url_name = resolve(request.path_info).url_name
        if url_name.endswith('change'):
            suggestions_queryset = self.model.objects.only('pe_name')
            qs = qs.prefetch_related(
                Prefetch('suggestions', queryset=suggestions_queryset),
            )

        return qs

    def get_field_queryset(self, db, db_field, request):
        qs = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'suggestions':
            object_id = request.resolver_match.kwargs.get('object_id')
            qs = db_field.remote_field.model.objects.only('pe_name')
            if object_id:
                qs = qs.exclude(pk=object_id)
        return qs

    @admin.display(description=_('poster'))
    def display_poster(self, obj):
        return format_html(
            f'<img src={obj.small_poster.url} alt={obj.en_name} '
            'style="width: 150px;border-radius: 5px" />'
        )

    @admin.display(description=_('genres'))
    def display_genres(self, obj):
        return '، '.join(map(lambda x: x.genre, obj.genres.all()))


@admin.register(models.Serial)
class SerialAdmin(BaseModelAdmin):
    inlines = [SeasonInline]

    def save_model(self, request, obj, form, change):
        obj.content_type = models.Content.ContentTypeChoices.SERIAL
        obj.save()


@admin.register(models.Movie)
class MovieAdmin(BaseModelAdmin):
    fieldsets = (
        (None, {'fields': ('pe_name', 'en_name', 'slug', 'is_vip')}),
        (_('Posters'), {'fields': ('small_poster', 'large_poster')}),
        (_('Further information'), {'fields': (
            'age_range', 'country', 'description',
            'duration', 'resolution', 'genres', 'suggestions',
        )}),
        (_('Video'), {'fields': ('video', 'pe_subtitle', 'en_subtitle')}),
    )

    def save_model(self, request, obj, form, change):
        obj.content_type = models.Content.ContentTypeChoices.MOVIE
        obj.save()
