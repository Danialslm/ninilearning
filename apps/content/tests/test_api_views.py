from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.reverse import reverse

from apps.content.api.views import BookmarkAPIView
from apps.content.models import Content


class BookmarkAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone_number='09000000000',
            password='test',
        )
        self.content = Content.objects.create(slug='test')
        self.url = reverse('content:bookmark', kwargs={'slug': self.content.slug})

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            BookmarkAPIView,
        )

    def test_bookmark_content_anonymously(self):
        post_response = self.client.post(self.url)
        delete_response = self.client.delete(self.url)

        self.assertEqual(post_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bookmark_content(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': _('The object is bookmarked.')})

        self.assertTrue(self.user.is_bookmarked(self.content))

    def test_delete_bookmark_content(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )
        self.user.bookmarks.add(self.content)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': _('The object bookmark deleted.')})

        self.assertFalse(self.user.is_bookmarked(self.content))
