import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from apps.content.models import Serial, Season, Episode, Movie
from apps.content.views import SerialDetailView, SeasonEpisodeListView, MovieDetailView

sample_image = tempfile.NamedTemporaryFile(suffix='.jpg').name
sample_video = tempfile.NamedTemporaryFile(suffix='.mp4').name
sample_subtitle = tempfile.NamedTemporaryFile(suffix='.srt').name


class SerialDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone_number='09000000000',
            password='test',
        )
        self.serial = Serial.objects.create(
            slug='test',
            small_poster=sample_image,
            large_poster=sample_image,
        )
        self.season = Season.objects.create(season_number=1, serial=self.serial)
        self.episode = Episode.objects.create(
            episode_number=1,
            season=self.season,
            is_vip=False,
            poster=sample_image,
        )
        self.url = reverse('content:serial_detail', kwargs={'slug': self.serial.slug})

        self.user.bookmarks.add(self.serial)
        self.serial.add_like(self.user)
        self.episode.add_dislike(self.user)

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            SerialDetailView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/detail/serial_detail.html')
        self.assertEqual(response.context.get('object'), self.serial)

    def test_extra_context_anonymous_user(self):
        response = self.client.get(self.url)

        self.assertIsNone(response.context.get('bookmarked'))
        self.assertIsNone(response.context.get('liked'))
        self.assertIsNone(response.context.get('disliked'))

    def test_extra_context_logged_in_user(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )
        response = self.client.get(self.url)
        self.assertTrue(response.context.get('bookmarked'))
        self.assertTrue(response.context.get('liked'))
        self.assertFalse(response.context.get('disliked'))

    def test_first_season_episodes_context(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )
        response = self.client.get(self.url)

        first_season_episodes = response.context.get('first_season_episodes')
        self.assertIsNotNone(first_season_episodes)
        self.assertEqual(
            list(first_season_episodes),
            list(self.serial.seasons.filter(season_number=1).get().episodes.all()),
        )
        self.assertFalse(first_season_episodes[0].is_liked)
        self.assertTrue(first_season_episodes[0].is_disliked)


class SeasonEpisodeListViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone_number='09000000000',
            password='test',
        )
        self.serial = Serial.objects.create(
            slug='test',
            small_poster=sample_image,
            large_poster=sample_image,
        )
        self.season = Season.objects.create(season_number=1, serial=self.serial)
        self.episode = Episode.objects.create(
            episode_number=1,
            season=self.season,
            is_vip=False,
            poster=sample_image,
        )
        self.episode.add_like(self.user)

        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )
        self.url = reverse(
            'content:season_episodes',
            kwargs={
                'slug': self.serial.slug,
                'season_number': self.season.season_number
            },
        )

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            SeasonEpisodeListView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/detail/episode_list.html')
        self.assertIsNotNone(response.context.get('episodes'))


class MovieDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone_number='09000000000',
            password='test',
        )
        self.movie = Movie.objects.create(
            slug='test',
            small_poster=sample_image,
            large_poster=sample_image,
        )
        self.url = reverse('content:movie_detail', kwargs={'slug': self.movie.slug})

        self.user.bookmarks.add(self.movie)
        self.movie.add_like(self.user)

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            MovieDetailView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/detail/movie_detail.html')
        self.assertEqual(response.context.get('object'), self.movie)

    def test_extra_context_anonymous_user(self):
        response = self.client.get(self.url)

        self.assertIsNone(response.context.get('bookmarked'))
        self.assertIsNone(response.context.get('liked'))
        self.assertIsNone(response.context.get('disliked'))

    def test_extra_context_logged_in_user(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )
        response = self.client.get(self.url)
        self.assertTrue(response.context.get('bookmarked'))
        self.assertTrue(response.context.get('liked'))
        self.assertFalse(response.context.get('disliked'))
