from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.reverse import reverse

from apps.content.models import Content, Episode
from apps.votes.api.views import ContentVoteAPIView, EpisodeVoteAPIView


class ContentVoteAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone_number='09000000000',
            password='test',
        )
        self.content = Content.objects.create(slug='test')
        self.url = reverse('votes:vote', kwargs={'slug': self.content.slug})

    def login(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )

    def test_correct_view_class(self):
        view = resolve(self.url)

        self.assertIs(
            view.func.view_class,
            ContentVoteAPIView,
        )

    def test_vote_content_anonymously(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_without_querystring(self):
        self.login()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'detail': _('Please provide `vote` querystring with `like` or `dislike` value.')}
        )

    def test_like_content(self):
        self.login()
        response = self.client.post(self.url + '?vote=like')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.content.liked(self.user))

    def test_dislike_content(self):
        self.login()
        response = self.client.post(self.url + '?vote=dislike')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.content.disliked(self.user))


class EpisodeVoteAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone_number='09000000000',
            password='test',
        )
        self.episode = Episode.objects.create(is_vip=False)
        self.url = reverse('votes:episode_vote', kwargs={'pk': self.episode.pk})

    def login(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )

    def test_correct_view_class(self):
        view = resolve(self.url)

        self.assertIs(
            view.func.view_class,
            EpisodeVoteAPIView,
        )

    def test_vote_content_anonymously(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_without_querystring(self):
        self.login()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'detail': _('Please provide `vote` querystring with `like` or `dislike` value.')}
        )

    def test_like_content(self):
        self.login()
        response = self.client.post(self.url + '?vote=like')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.episode.liked(self.user))

    def test_dislike_content(self):
        self.login()
        response = self.client.post(self.url + '?vote=dislike')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.episode.disliked(self.user))
