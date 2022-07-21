import tempfile

from django.test import TestCase

from apps.main.models import Slide, Collection


class SlideTestCase(TestCase):
    def test_slide_creation(self):
        desktop_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        mobile_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        intro_image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        slide = Slide.objects.create(
            title='test',
            referral_link='https://example.com',
            referral_link_text='test',
            desktop_image=desktop_image,
            mobile_image=mobile_image,
            intro_image=intro_image,
        )

        self.assertEqual(slide.title, 'test')
        self.assertEqual(slide.referral_link, 'https://example.com')
        self.assertEqual(slide.referral_link_text, 'test')
        self.assertEqual(slide.desktop_image, desktop_image)
        self.assertEqual(slide.desktop_image, desktop_image)
        self.assertEqual(slide.desktop_image, desktop_image)


class CollectionTestCase(TestCase):
    def test_collection_creation(self):
        collection = Collection.objects.create(
            title='test',
            slug='test',
        )

        self.assertEqual(collection.title, 'test')
        self.assertEqual(collection.slug, 'test')
