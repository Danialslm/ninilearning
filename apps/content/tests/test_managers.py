import datetime

from django.test import TestCase

from apps.content.models import Content, Serial, Movie


class ContentManagerTestCase(TestCase):
    def setUp(self):
        self.content = Content.objects.create(en_name='test')

    def test_popular_result(self):
        self.content.likes_count = 1
        self.content.save()

        self.assertTrue(Content.objects.popular().exists())
        self.content.likes_count = 0
        self.content.save()
        self.assertFalse(Content.objects.popular().exists())

    def test_recent_result(self):
        self.assertTrue(Content.objects.recent().exists())

        self.content.created_at = datetime.datetime.now() - datetime.timedelta(days=31)
        self.content.save()
        self.assertFalse(Content.objects.recent().exists())

    def test_search_result(self):
        self.assertTrue(Content.objects.search('test').exists())


class SerialManagerTestCase(TestCase):
    def setUp(self):
        self.serial = Serial.objects.create()

    def test_filter_content_type(self):
        self.assertEqual(
            Serial.objects.get().content_type,
            Content.ContentTypeChoices.SERIAL,
        )


class MovieManagerTestCase(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create()

    def test_filter_content_type(self):
        self.assertEqual(
            Movie.objects.get().content_type,
            Content.ContentTypeChoices.MOVIE,
        )
