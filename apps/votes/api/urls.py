from django.urls import path

from . import views

urlpatterns = [
    path('episode/<int:pk>/', views.EpisodeVoteAPIView.as_view(), name='episode_vote'),
    path('<slug:slug>/', views.ContentVoteAPIView.as_view(), name='vote'),
]
