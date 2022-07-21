from django.urls import path, include

from . import views

app_name = 'content'
urlpatterns = [
    path('serial/<slug:slug>/', views.SerialDetailView.as_view(), name='serial_detail'),
    path('movie/<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path(
        'serial/<slug:slug>/season/<int:season_number>/episodes/',
        views.SeasonEpisodeListView.as_view(),
        name='season_episodes',
    ),
    path('', include('apps.content.api.urls')),
]
