import tempfile

from django.test import TestCase
from django.urls import resolve, reverse

from apps.content.models import Genre, Content
from apps.main import views
from apps.main.models import Collection

sample_image = tempfile.NamedTemporaryFile(suffix='.jpg').name


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('main:home')

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.HomeView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_view_has_contexts(self):
        response = self.client.get(self.url)

        self.assertIsNotNone(response.context.get('slides'))
        self.assertIsNotNone(response.context.get('popular'))
        self.assertIsNotNone(response.context.get('recent'))
        self.assertIsNotNone(response.context.get('collections'))


class CollectionListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('main:collections')

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.CollectionListView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/collection_list.html')


class CollectionContentListViewTestCase(TestCase):
    def setUp(self):
        collection = Collection.objects.create(title='test', slug='test')
        content = Content.objects.create(
            small_poster=sample_image,
        )
        collection.contents.add(content)

        self.url = reverse('main:collection', kwargs={'slug': collection.slug})

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.CollectionContentListView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/content_list/collection_content_list.html')


class RecentContentListViewTestCase(TestCase):
    def setUp(self):
        Content.objects.create(
            small_poster=sample_image,
        )
        self.url = reverse('main:recent')

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.RecentContentListView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/content_list/recent.html')


class PopularContentListViewTestCase(TestCase):
    def setUp(self):
        Content.objects.create(
            small_poster=sample_image,
            popularity=100,
        )
        self.url = reverse('main:popular')

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.PopularContentListView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/content_list/popular.html')


class GenreContentListViewTestCase(TestCase):
    def setUp(self):
        genre = Genre.objects.create(genre='test')
        content = Content.objects.create(
            small_poster=sample_image,
        )
        content.genres.add(genre)

        self.url = reverse('main:genre', kwargs={'genre': genre.genre})

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.GenreContentListView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/content_list/genre_content_list.html')


class SearchResultListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('main:search')

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.SearchResultListView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/search/form.html')

    def test_search_result(self):
        content = Content.objects.create(
            small_poster=sample_image,
            en_name='test',
        )
        response = self.client.get(self.url + '?query=test')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/search/results.html')
        self.assertContains(response, content.en_name)
