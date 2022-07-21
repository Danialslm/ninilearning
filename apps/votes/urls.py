from django.urls import include, path

app_name = 'votes'
urlpatterns = [
    path('', include('apps.votes.api.urls')),
]
