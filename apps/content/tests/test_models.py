import tempfile

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.content.models import Genre, Content, Serial, Season, Episode

sample_image = tempfile.NamedTemporaryFile(suffix='.jpg').name
sample_video = tempfile.NamedTemporaryFile(suffix='.mp4').name
sample_subtitle = tempfile.NamedTemporaryFile(suffix='.srt').name

content_data = {
    'pe_name': 'test',
    'en_name': 'test',
    'slug': 'test',
    'age_range': 'test',
    'country': 'test',
    'description': 'test',
    'small_poster': sample_image,
    'large_poster': sample_image,
    'duration': 'test',
    'resolution': 'test',
}

movie_data = {
    **content_data,
    'video': sample_video,
    'pe_subtitle': sample_subtitle,
    'en_subtitle': sample_subtitle,
}


class GenreTestCase(TestCase):
    def test_object_creation(self):
        genre = Genre.objects.create(genre='test')
        self.assertEqual(genre.genre, 'test')


class ContentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create()

    def test_object_creation(self):
        content = Content.objects.create(**content_data)

        self.assertEqual(content.pe_name, 'test')
        self.assertEqual(content.en_name, 'test')
        self.assertEqual(content.slug, 'test')
        self.assertEqual(content.age_range, 'test')
        self.assertEqual(content.country, 'test')
        self.assertEqual(content.description, 'test')
        self.assertEqual(content.small_poster, sample_image)
        self.assertEqual(content.large_poster, sample_image)
        self.assertEqual(content.duration, 'test')
        self.assertEqual(content.resolution, 'test')
        self.assertEqual(content.popularity, 0)

    def test_popularity_calculation(self):
        content = Content.objects.create(likes_count=20, dislikes_count=5)

        self.assertEqual(content.popularity, 80)
        self.assertEqual(content.total_votes, 25)

    def test_user_vote_like(self):
        content = Content.objects.create()
        content.add_like(self.user)

        self.assertTrue(content.liked(self.user))
        self.assertEqual(content.likes_count, 1)
        self.assertEqual(content.popularity, 100)

        # test preventing likes count increment
        content.add_like(self.user)
        self.assertTrue(content.liked(self.user))
        self.assertEqual(content.likes_count, 1)
        self.assertEqual(content.popularity, 100)

    def test_user_vote_dislike(self):
        content = Content.objects.create()
        content.add_dislike(self.user)

        self.assertTrue(content.disliked(self.user))
        self.assertEqual(content.dislikes_count, 1)
        self.assertEqual(content.popularity, 0)

        # test preventing likes count increment
        content.add_dislike(self.user)
        self.assertTrue(content.disliked(self.user))
        self.assertEqual(content.dislikes_count, 1)
        self.assertEqual(content.popularity, 0)

    def test_change_vote(self):
        content = Content.objects.create()
        content.add_like(self.user)
        content.add_dislike(self.user)

        self.assertTrue(content.disliked(self.user))
        self.assertFalse(content.liked(self.user))
        self.assertEqual(content.dislikes_count, 1)
        self.assertEqual(content.likes_count, 0)
        self.assertEqual(content.popularity, 0)

        content.add_like(self.user)
        self.assertFalse(content.disliked(self.user))
        self.assertTrue(content.liked(self.user))
        self.assertEqual(content.dislikes_count, 0)
        self.assertEqual(content.likes_count, 1)
        self.assertEqual(content.popularity, 100)

    def test_delete_vote(self):
        content = Content.objects.create()
        content.add_like(self.user)
        content.delete_vote(self.user)

        self.assertEqual(content.likes_count, 0)

        content.add_dislike(self.user)
        content.delete_vote(self.user)

        self.assertEqual(content.dislikes_count, 0)


class SeasonTestCase(TestCase):
    def setUp(self):
        self.serial = Serial.objects.create()

    def test_object_creation(self):
        season = Season.objects.create(
            season_number=1,
            serial=self.serial
        )

        self.assertEqual(season.season_number, 1)
        self.assertIs(season.serial, self.serial)

    def test_duplicate_season(self):
        Season.objects.create(
            season_number=1,
            serial=self.serial
        )
        with self.assertRaises(IntegrityError):
            Season.objects.create(
                season_number=1,
                serial=self.serial
            )


class EpisodeTestCase(TestCase):
    def setUp(self):
        self.serial = Serial.objects.create()
        self.season = Season.objects.create(
            serial=self.serial,
            season_number=1,
        )

    def test_object_creation(self):
        episode = Episode.objects.create(
            title='test',
            poster=sample_image,
            video=sample_video,
            pe_subtitle=sample_subtitle,
            en_subtitle=sample_subtitle,
            episode_number=1,
            is_vip=True,
            season=self.season,
        )
        self.assertEqual(episode.title, 'test')
        self.assertEqual(episode.poster, sample_image)
        self.assertEqual(episode.video, sample_video)
        self.assertEqual(episode.pe_subtitle, sample_subtitle)
        self.assertEqual(episode.en_subtitle, sample_subtitle)
        self.assertEqual(episode.episode_number, 1)
        self.assertTrue(episode.is_vip)
        self.assertIs(episode.season, self.season)
        self.assertIs(episode.serial, self.serial)

    def test_duplicate_season(self):
        Episode.objects.create(episode_number=1, season=self.season, is_vip=False)
        with self.assertRaises(IntegrityError):
            Episode.objects.create(
                episode_number=1,
                season=self.season,
            )
