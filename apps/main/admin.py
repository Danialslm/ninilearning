from django.contrib import admin
from django.db.models import Count
from django.urls import resolve
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import CollectionForm
from .models import Slide, Collection


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('display_slide_img', 'title', 'display_referral_link', 'referral_link_text')

    @admin.display(description=_('slide image'))
    def display_slide_img(self, obj):
        return format_html(
            f'<img src={obj.desktop_image.url} alt={obj.title} '
            'style="width: 150px;border-radius: 5px" />'
        )

    @admin.display(description=_('referral link'))
    def display_referral_link(self, obj):
        return format_html(
            f'<a href={obj.referral_link}>{obj.referral_link}</a>'
        )


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'display_items_count')
    search_fields = ('title',)
    fields = ('title', 'slug', 'series', 'movies')
    form = CollectionForm

    def get_field_queryset(self, db, db_field, request):
        qs = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'movies' or db_field.name == 'series':
            qs = db_field.remote_field.model.objects.only('pe_name')
        return qs

    def get_queryset(self, request):
        qs = self.model.objects.all()
        url_name = resolve(request.path_info).url_name

        if url_name.endswith('changelist'):
            qs = qs.annotate(items_count=Count('contents'))

        return qs

    @admin.display(description=_('items count'))
    def display_items_count(self, obj):
        return obj.items_count
