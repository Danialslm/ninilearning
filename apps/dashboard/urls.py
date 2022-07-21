from django.urls import path

from . import views
from apps.users.views import PasswordChangeView

app_name = 'dashboard'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('devices/', views.DeviceListView.as_view(), name='devices'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmarks'),
]
