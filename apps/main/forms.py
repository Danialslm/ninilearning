from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from apps.content.models import Serial, Movie, Content
from .models import Collection


class CollectionForm(forms.ModelForm):
    series = forms.ModelMultipleChoiceField(
        queryset=Serial.objects.only('pe_name'),
        widget=FilteredSelectMultiple(_('serial'), False),
        required=False,
        label=_('series'),
    )
    movies = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.only('pe_name'),
        widget=FilteredSelectMultiple(_('movie'), False),
        required=False,
        label=_('movies'),
    )

    class Meta:
        model = Collection
        fields = ('title', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('initial') is None and kwargs.get('instance') is not None:
            self.fields['series'].initial = self.instance.contents \
                .filter(content_type=Content.ContentTypeChoices.SERIAL) \
                .only('pe_name')
            self.fields['movies'].initial = self.instance.contents \
                .filter(content_type=Content.ContentTypeChoices.MOVIE) \
                .only('pe_name')

    def clean(self):
        cleaned_data = super().clean()
        series = cleaned_data['series']
        movies = cleaned_data['movies']
        if not series.exists() and not movies.exists():
            self.add_error('__all__', _('The collection should have a serial or movie at least.'))
        return cleaned_data

    def save(self, *args, **kwargs):
        series = self.cleaned_data['series']
        movies = self.cleaned_data['movies']
        self.instance.contents.set([*series, *movies])
        return super().save(*args, **kwargs)
