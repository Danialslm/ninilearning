from django.urls import path

from . import views

urlpatterns = [
    path('bookmark/<slug:slug>/', views.BookmarkAPIView.as_view(), name='bookmark'),
]
