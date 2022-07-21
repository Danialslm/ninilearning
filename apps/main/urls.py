from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recent/', views.RecentContentListView.as_view(), name='recent'),
    path('popular/', views.PopularContentListView.as_view(), name='popular'),
    path('collections/', views.CollectionListView.as_view(), name='collections'),
    path('collections/<slug:slug>/', views.CollectionContentListView.as_view(), name='collection'),
    path('genres/<genre>/', views.GenreContentListView.as_view(), name='genre'),

    path('search/', views.SearchResultListView.as_view(), name='search'),
]
