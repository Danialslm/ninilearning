from django.test import TestCase

from apps.content.models import Serial, Movie
from apps.main.forms import CollectionForm
from apps.main.models import Collection
from django.utils.translation import gettext as _


class CollectionFormTestCase(TestCase):
    def setUp(self):
        self.serial = Serial.objects.create(pe_name='test serial', en_name='test serial')
        self.movie = Movie.objects.create(pe_name='test movie', en_name='test movie')
        self.collection = Collection.objects.create()

    def test_invalid_data(self):
        form = CollectionForm({}, instance=self.collection)
        self.assertFalse(form.is_valid())
        self.assertIn(_('The collection should have a serial or movie at least.'), form.errors.get('__all__'))

    def test_valid_data(self):
        form = CollectionForm(
            {
                'title': 'test',
                'slug': 'test',
                'series': [self.serial.pk],
                'movies': [self.movie.pk],
            },
            instance=self.collection,
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

        form.save()
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.title, 'test')
        self.assertEqual(self.collection.slug, 'test')
        self.assertTrue(self.collection.contents.contains(self.serial))
        self.assertTrue(self.collection.contents.contains(self.movie))

    def test_initial_value(self):
        self.collection.contents.add(self.serial, self.movie)
        form = CollectionForm({}, instance=self.collection)
        self.assertEqual(
            list(form.fields['movies'].initial),
            list(self.collection.contents.filter(pk=self.movie.pk)),
        )
        self.assertEqual(
            list(form.fields['series'].initial),
            list(self.collection.contents.filter(pk=self.serial.pk)),
        )
