from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.translation import gettext as _

from apps.dashboard import views

UserModel = get_user_model()


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('dashboard:profile')

        self.user = UserModel.objects.create_user(
            phone_number='09000000000',
            first_name='test',
            last_name='test',
            password='test',
        )

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
            views.ProfileView,
        )

    def test_view_load_anonymously(self):
        get_response = self.client.get(self.url)
        post_response = self.client.post(self.url)

        self.assertRedirects(get_response, reverse('users:login') + f'?next={self.url}')
        self.assertRedirects(post_response, reverse('users:login') + f'?next={self.url}')

    def test_view_load(self):
        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/profile.html')

    def test_update_user_profile(self):
        self.login()
        response = self.client.post(
            self.url,
            {
                'first_name': 'updated',
                'last_name': 'updated',
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Your information updated successfully.'), status_code=200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'updated')
        self.assertEqual(self.user.last_name, 'updated')


class BookmarkListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('dashboard:bookmarks')

        self.user = UserModel.objects.create_user(
            phone_number='09000000000',
            first_name='test',
            last_name='test',
            password='test',
        )

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.BookmarkListView,
        )

    def test_view_load_anonymously(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('users:login') + f'?next={self.url}')

    def test_view_load(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/bookmark_list.html')


class DeviceListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('dashboard:devices')

        self.user = UserModel.objects.create_user(
            phone_number='09000000000',
            first_name='test',
            last_name='test',
            password='test',
        )

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            views.DeviceListView,
        )

    def test_view_load_anonymously(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('users:login') + f'?next={self.url}')

    def test_view_load(self):
        self.client.post(
            reverse('users:login'),
            {
                'username': self.user.phone_number,
                'password': 'test',
            }
        )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/device_list.html')
